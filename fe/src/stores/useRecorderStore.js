import { defineStore } from "pinia";
import { ref, onUnmounted } from "vue";

export const useRecorderStore = defineStore("recorder", () => {
  const isRecording = ref(false);
  let mediaRecorder = null;
  let ws = null;
  const student_id = ref(null);
  const example_id = ref(null);
  const record_date = ref(null);

  // Store result from WebSocket
  const isCorrect = ref(null);
  const continueWithNext = ref(null);

  let emitFunction = null; // Store emit function reference

  const setEmitFunction = (emit) => {
    emitFunction = emit;
  };

  const startRecording = async () => {
    try {
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        ws = new WebSocket("ws://localhost:8000/ws/speech/");
        ws.onopen = () => {
          console.log("WebSocket connection opened.");
          sendExampleData();
        };
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          // Store values
          isCorrect.value = data.isCorrect;
          continueWithNext.value = data.continue_with_next;

          console.log("Answer Correct:", data.isCorrect);
          console.log("Continue with Next:", data.continue_with_next);

          // 🔹 Emit event to parent component
          if (emitFunction) {
            emitFunction("answerSent", {
              isCorrect: data.isCorrect,
              nextExample: data.continue_with_next,
            });
          }
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
      ws.send(JSON.stringify({ student_id: student_id.value, example_id: example_id.value, record_date: record_date.value }));
    }
  };

  const updateExampleData = (studentId, exampleId, recordDate) => {
    student_id.value = studentId;
    example_id.value = exampleId;
    record_date.value = recordDate;
    sendExampleData();
  };

  const closeWebSocket = () => {
    if (ws) {
      ws.close();
      ws = null;
      isRecording.value = false;
      console.log("WebSocket connection closed.");
    }
  };

  // Ensure WebSocket closes when navigating away
  onUnmounted(() => {
    console.log("Component unmounted, closing WebSocket...");
    closeWebSocket();
  });

  return {
    isRecording,
    startRecording,
    stopRecording,
    updateExampleData,
    isCorrect,
    continueWithNext,
    setEmitFunction, // Expose this function
  };
});
