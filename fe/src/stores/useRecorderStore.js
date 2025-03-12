import { defineStore } from "pinia";
import { ref, onUnmounted } from "vue";

export const useRecorderStore = defineStore("recorder", () => {
  const isRecording = ref(false);
  let mediaRecorder = null;
  let ws = null;
  const student_id = ref(null);
  const example_id = ref(null);
  const input_type = ref(null); 
  const record_date = ref(null);

  // Store result from WebSocket
  const isCorrect = ref(null);
  const continueWithNext = ref(null);
  const student_answer = ref(null);

  const allowedRecording = ref(false);

  let emitFunction = null; // Store emit function reference

  const setEmitFunction = (emit) => {
    emitFunction = emit;
  };

  const startRecording = async () => {
    try {
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        ws = new WebSocket("wss://drillovacka.applikuapp.com/ws/speech/"); //    "ws://localhost:8000/ws/speech/"
        ws.onopen = () => {
          console.log("WebSocket connection opened.");
          sendExampleData();
        };
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          // Store values

          if(data.skipped == true){
            if (emitFunction) {
              emitFunction("skipped",{skipped: true});
            }
          
          } else if(data.finished == true){
            if (emitFunction) {
              emitFunction("finished");
            }

          }else{
            isCorrect.value = data.isCorrect;
            continueWithNext.value = data.continue_with_next;
            student_answer.value = data.student_answer;
            if (emitFunction) {
              emitFunction("answerSent", {
                isCorrect: data.isCorrect,
                nextExample: data.continue_with_next,
                studentAnswer: data.student_answer,
              });
            }
          }
          console.log("WebSocket message received:", data);

          
        };
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0 && ws?.readyState === WebSocket.OPEN) {
          const reader = new FileReader();
          reader.onloadend = () => ws?.send(reader.result);
          reader.readAsArrayBuffer(e.data);
        }
      };

      mediaRecorder.start(100);
      isRecording.value = true;
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach((track) => track.stop());
    }
    closeWebSocket();
    isRecording.value = false;
  };

  const sendExampleData = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ student_id: student_id.value, example_id: example_id.value, record_date: record_date.value, input_type: input_type.value }));
    }
  };

  const updateExampleData = (studentId, exampleId, inputType, recordDate) => {
    student_id.value = studentId;
    example_id.value = exampleId;
    input_type.value = inputType;
    record_date.value = recordDate;
    sendExampleData();
  };

  const allowRecording = () => {
    allowedRecording.value = true;
  };

  const closeWebSocket = () => {
    if (ws) {
      ws.close();
      ws = null;
      isRecording.value = false;
      console.log("WebSocket connection closed.");
    }
  };

  onUnmounted(() => {
    console.log("Component unmounted, closing WebSocket...");
    allowedRecording.value = false;
    closeWebSocket();
  });

  return {
    isRecording,
    startRecording,
    stopRecording,
    updateExampleData,
    allowRecording,
    allowedRecording,
    isCorrect,
    continueWithNext,
    student_answer,
    setEmitFunction,
  };
});
