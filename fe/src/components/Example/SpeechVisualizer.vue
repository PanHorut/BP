<!--
================================================================================
 Component: SpeechVisualizer.vue
 Description:
        Visualizes the audio input so user sees that his voice is recorded.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRecorderStore } from "@/stores/useRecorderStore";

const props = defineProps({
  backgroundColor: {
    type: String,
    default: "#f1faee"
  },
  barColor: {
    type: String,
    default: "#4ade80"
  },
  height: {
    type: Number,
    default: 100
  },
  width: {
    type: Number,
    default: 300
  },
  barWidth: {
    type: Number,
    default: 4
  },
  barGap: {
    type: Number,
    default: 2
  },
  barCount: {
    type: Number,
    default: 40
  }
});

const recorderStore = useRecorderStore();
const canvasRef = ref(null);
const analyser = ref(null);
const dataArray = ref(null);
const animationId = ref(null);

// Watch for recording state changes
watch(() => recorderStore.isRecording, (isRecording) => {
  if (isRecording) {
    setupAnalyser();
  } else {
    stopVisualization();
  }
});

onMounted(() => {

  if (recorderStore.isRecording) {
    setupAnalyser();
  } else {
    
    drawEmptyState();
  }
});

onUnmounted(() => {
  stopVisualization();
});

// Draw an empty or idle state on a canvas
const drawEmptyState = () => {
  if (!canvasRef.value) return;
  
  // Get canvas and drawing context
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  
  ctx.fillStyle = props.backgroundColor;
  ctx.fillRect(0, 0, width, height);
  
  const totalWidth = props.barCount * (props.barWidth + props.barGap);
  const startX = (width - totalWidth) / 2;
  
  ctx.fillStyle = props.barColor;
  
  // Draw each small vertical bar
  for (let i = 0; i < props.barCount; i++) {
    const barHeight = 2; // Small height for idle state
    const x = startX + i * (props.barWidth + props.barGap);
    const y = height / 2 - barHeight / 2; // Center vertically
    
    ctx.fillRect(x, y, props.barWidth, barHeight);
  }
};

// Set up an audio analyser for visualizing microphone input
const setupAnalyser = async () => {
  try {
    // Get the audio stream
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(stream);
    
    // Create an analyser node to get frequency/time data from the audio stream
    analyser.value = audioContext.createAnalyser();
    analyser.value.fftSize = 256;
    
    source.connect(analyser.value);
    
    // Set up array to store the frequency data 
    const bufferLength = analyser.value.frequencyBinCount;
    dataArray.value = new Uint8Array(bufferLength);
    
    // Start visualization
    startVisualization();

  } catch (error) {
    console.error("Error setting up audio visualizer:", error);
  }
};

// Start visualizing the audio input on a canvas
const startVisualization = () => {
  if (!canvasRef.value || !analyser.value || !dataArray.value) return;
  
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  const activeColor = recorderStore.isRecording ? '#457b9d' : props.barColor;
  
  // Drawing loop
  const draw = () => {
    
    if (!recorderStore.isRecording) {
      cancelAnimationFrame(animationId.value);
      drawEmptyState();
      return;
    }
    
    // Schedule the next animation frame
    animationId.value = requestAnimationFrame(draw);
    
    // Get current frequency data from the analyser
    analyser.value.getByteFrequencyData(dataArray.value);
    
    ctx.fillStyle = props.backgroundColor;
    ctx.fillRect(0, 0, width, height);
    
    // Calculate layout
    const numberOfBars = props.barCount;
    const totalBarWidth = numberOfBars * (props.barWidth + props.barGap);
    const startX = (width - totalBarWidth) / 2;
    const centerY = height / 2;
    
    // Determine how to sample the frequency data
    const step = Math.floor(dataArray.value.length / numberOfBars);
    
    // Draw each bar
    for (let i = 0; i < numberOfBars; i++) {
      const dataIndex = i * step;
      const barHeight = (dataArray.value[dataIndex] / 255) * (height / 2);
      const x = startX + i * (props.barWidth + props.barGap);
      const borderRadius = props.barWidth / 2; // Rounded corners

      ctx.fillStyle = activeColor;

      // Top half - rounded only on top
      ctx.beginPath();
      ctx.roundRect(x, centerY - barHeight, props.barWidth, barHeight, [borderRadius, borderRadius, 0, 0]);
      ctx.fill();

      // Bottom half - rounded only on bottom
      ctx.beginPath();
      ctx.roundRect(x, centerY, props.barWidth, barHeight, [0, 0, borderRadius, borderRadius]);
      ctx.fill();
    }
  };

  // Draw first frame
  draw();
};
// Stop the audio visualization and display the idle state
const stopVisualization = () => {
  if (animationId.value) {
    cancelAnimationFrame(animationId.value);
    animationId.value = null;
  }
  
  drawEmptyState();
};
</script>

<template>

  <div class="my-4 flex justify-center">
    
    <canvas 
      ref="canvasRef" 
      :width="width" 
      :height="height"
    ></canvas>

  </div>
  
</template>

