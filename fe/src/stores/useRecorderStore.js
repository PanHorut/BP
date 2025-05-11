/**
 * ================================================================================
 * File: useRecorderStore.js
 * Description:
 *       Pinia store for managing the audio recording state and WebSocket communication
 *       for user answers by voice.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

import { defineStore } from "pinia";
import { ref, onUnmounted } from "vue";
import { useLanguageStore } from "./useLanguageStore";

export const useRecorderStore = defineStore("recorder", () => {

  let ws = null;

  // Control recording
  const isRecording = ref(false);

  // Metadata for the audio answer evaluation
  const student_id = ref(null);
  const example_id = ref(null);
  const input_type = ref(null); 
  const record_date = ref(null);

  // Result of evaluation data
  const isCorrect = ref(null);
  const continueWithNext = ref(null);
  const student_answer = ref(null);

  // User allowed his voice to be recorded
  const allowedRecording = ref(false);

  // Survey metadata
  const question_text = ref(null);
  const skillsList = ref(null);

  // Audio processing variables
  let audioContext = null;
  let source = null;
  let stream = null;
  let workletNode = null;

  let emitFunction = null;

  const setEmitFunction = (emit) => {
    emitFunction = emit;
  };

  // AudioWorklet processor code as a string
  const processorCode = `
    class PCMProcessor extends AudioWorkletProcessor {
      constructor() {
        super();
        this.bufferSize = 4096;
        this.buffer = new Float32Array(this.bufferSize);
        this.bufferIndex = 0;
      }
      
      process(inputs, outputs, parameters) {
        const input = inputs[0][0];
        if (!input) return true;
        
        // Fill buffer with incoming audio data
        for (let i = 0; i < input.length; i++) {
          this.buffer[this.bufferIndex++] = input[i];
          
          // When buffer is full, send it to main thread and reset
          if (this.bufferIndex >= this.bufferSize) {
            // Convert to Int16 before sending
            const int16Buffer = new Int16Array(this.bufferSize);
            for (let j = 0; j < this.bufferSize; j++) {
              const s = Math.max(-1, Math.min(1, this.buffer[j]));
              int16Buffer[j] = s < 0 ? s * 0x8000 : s * 0x7FFF;
            }
            
            this.port.postMessage(int16Buffer.buffer, [int16Buffer.buffer]);
            this.buffer = new Float32Array(this.bufferSize);
            this.bufferIndex = 0;
          }
        }
        return true;
      }
    }
    registerProcessor('pcm-processor', PCMProcessor);
  `;

  // Start the recording process and initiate WebSocket connection
  const startRecording = async (isSurvey) => {
    try {
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        let wsurl = isSurvey ? "ws://localhost:8000/ws/survey/" : "ws://localhost:8000/ws/speech/"; // POZOR NA DEPLOY
        ws = new WebSocket(wsurl); //   "wss://drillovacka.applikuapp.com/ws/survey/" : "wss://drillovacka.applikuapp.com/ws/speech/"
        ws.onopen = () => {
          console.log("WebSocket connection opened.");

          // Send metadata
          if (isSurvey) { 
            // For survey answer
            sendSurveyQuestionData();
          } else{
            // For example answer
            sendExampleData();
          }

          // Set ASR language
          const langStore = useLanguageStore();
          if(langStore.language === 'en') {
            changeASRLanguage('en-US');
          } else {
            changeASRLanguage('cs-CZ');
          } 
        };

        // Handle incoming WebSocket messages - answer evaluation results
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          // User skipped the question by voice
          if(data.skipped == true){
            // Update ExampleView
            if (emitFunction) {
              emitFunction("skipped", {skipped: true});
            }
          
          // User terminated practice by voice
          } else if(data.finished == true){
            // Update ExampleView
            if (emitFunction) {
              emitFunction("finished");
            }
          
          // User answered the question by voice
          } else {
            isCorrect.value = data.isCorrect;
            continueWithNext.value = data.continue_with_next;
            student_answer.value = data.student_answer;

            // Update ExampleView
            if (emitFunction) {
              emitFunction("answerSent", {
                isCorrect: data.isCorrect,
                nextExample: data.continue_with_next,
                studentAnswer: data.student_answer,
              });
            }
          }
        };
      }

      // Initialize audio context and stream
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContext = new AudioContext({ sampleRate: 16000 }); // 16kHz sample rate
      source = audioContext.createMediaStreamSource(stream);
      
      // Create AudioWorklet for processing audio
      const blob = new Blob([processorCode], { type: 'application/javascript' });
      const workletUrl = URL.createObjectURL(blob);
      await audioContext.audioWorklet.addModule(workletUrl);
      
      workletNode = new AudioWorkletNode(audioContext, 'pcm-processor');
      
      // Handle processed audio data from the worklet
      workletNode.port.onmessage = (event) => {
        if (ws?.readyState === WebSocket.OPEN) {
          ws.send(event.data); // Send processed audio data to server
        }
      };
      
      // Connect the audio processing pipeline
      source.connect(workletNode);
      workletNode.connect(audioContext.destination);
      
      isRecording.value = true;

    } catch (error) {
      console.error("Error starting recording:", error);
    }
  };
  // Stop the recording and clean up
  const stopRecording = () => {
    if (workletNode) {
      workletNode.disconnect();
      workletNode = null;
    }
    
    if (source) {
      source.disconnect();
      source = null;
    }
    
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      stream = null;
    }
    
    if (audioContext) {
      audioContext.close().catch(err => console.error("Error closing AudioContext:", err));
      audioContext = null;
    }
    
    closeWebSocket();
    isRecording.value = false;
  };

  // Send metadata about current example
  const sendExampleData = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ 
        student_id: student_id.value, 
        example_id: example_id.value, 
        record_date: record_date.value, 
        input_type: input_type.value,
        format: "pcm"
      }));
    }
  };
  // Update metadata about practiced example and example record
  const updateExampleData = (studentId, exampleId, inputType, recordDate) => {
    student_id.value = studentId;
    example_id.value = exampleId;
    input_type.value = inputType;
    record_date.value = recordDate;
    sendExampleData();
  };

  // Send metadata about survey question
  const sendSurveyQuestionData = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ 
        question_text: question_text.value, 
        question_type: 'open-question',
        skills: JSON.parse(JSON.stringify(skillsList.value)), 
        format: "pcm"
      }));
      }
  };

  // Update metadata about survey question
  const updateSurveyQuestionData = (questionText, skills) => {
    question_text.value = questionText;
    skillsList.value = skills;
    sendSurveyQuestionData();
  };

  // Change ASR language
  const changeASRLanguage = (language) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ language }));
    }
  };

  // Allow recording
  const allowRecording = () => {
    allowedRecording.value = true;
  };

  // Close Websocket connection
  const closeWebSocket = () => {
    if (ws) {
      ws.close();
      ws = null;
      isRecording.value = false;
      console.log("WebSocket connection closed.");
    }
  };

  // Cleanup when the component is unmounted
  onUnmounted(() => {
    console.log("Component unmounted, closing WebSocket...");
    allowedRecording.value = false;
    stopRecording();
    closeWebSocket();
  });

  return {
    isRecording,
    startRecording,
    stopRecording,
    updateExampleData,
    updateSurveyQuestionData,
    allowRecording,
    allowedRecording,
    isCorrect,
    continueWithNext,
    student_answer,
    setEmitFunction,
    changeASRLanguage,
  };
});