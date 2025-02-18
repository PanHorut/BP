<template>
    <div>
      <button @click="startRecording">Start Recording</button>
      <button @click="stopRecording">Stop Recording</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const isRecording = ref(false);
  const audioStream = ref(null);
  const mediaRecorder = ref(null);
  const websocket = ref(null);
  const audioChunks = ref([]);
  let sendInterval = null;
  
  // Start recording audio
  const startRecording = async () => {
    isRecording.value = true;
    audioChunks.value = [];
  
    // Start recording audio
    audioStream.value = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });
  
    mediaRecorder.value = new MediaRecorder(audioStream.value);
  
    mediaRecorder.value.ondataavailable = (event) => {
      console.log("Audio data available:", event.data);
      audioChunks.value.push(event.data);
    };
  
    // Create WebSocket connection to the backend
    websocket.value = new WebSocket('ws://localhost:8000/ws/audio/');
  
    websocket.value.onopen = () => {
      console.log('WebSocket connection established.');
    };
  
  
    mediaRecorder.value.start(2000); // Collect data every 1 second
    
    // Send audio chunks every 1 second
    sendInterval = setInterval(async () => {
      if (audioChunks.value.length > 0) {
        await sendAudioChunks();
      }
    }, 2000);
  };
  
  // Stop recording audio
  const stopRecording = () => {
    if (isRecording.value && mediaRecorder.value) {
      mediaRecorder.value.stop();
      audioStream.value.getTracks().forEach((track) => track.stop());
      isRecording.value = false;
      clearInterval(sendInterval); // Stop sending data
    }
  };
  
  const sendAudioChunks = async () => {
    // Only send the latest chunk
    const latestChunk = audioChunks.value.pop();
    audioChunks.value = []; // Clear after sending
  
    if (latestChunk) {
      const audioBlob = new Blob([latestChunk], { type: 'audio/webm' });
      const audioArrayBuffer = await audioBlob.arrayBuffer();
  
      console.log("Sending 1-second audio chunk:", audioArrayBuffer);
  
      if (websocket.value && websocket.value.readyState === WebSocket.OPEN) {
        websocket.value.send(audioArrayBuffer); // Send audio data as binary
      }
    }
  };
  </script>
  