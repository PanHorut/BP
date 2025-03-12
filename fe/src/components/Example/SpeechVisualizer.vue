// AudioVisualizer.vue
<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRecorderStore } from "@/stores/useRecorderStore";

const props = defineProps({
  backgroundColor: {
    type: String,
    default: "#f1faee" // Light background color
  },
  barColor: {
    type: String,
    default: "#4ade80" // Green color that matches your start button
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
    // Draw empty state
    drawEmptyState();
  }
});

onUnmounted(() => {
  stopVisualization();
});

const drawEmptyState = () => {
  if (!canvasRef.value) return;
  
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  
  // Clear canvas
  ctx.fillStyle = props.backgroundColor;
  ctx.fillRect(0, 0, width, height);
  
  // Draw small vertical bars
  const totalWidth = props.barCount * (props.barWidth + props.barGap);
  const startX = (width - totalWidth) / 2;
  
  ctx.fillStyle = props.barColor;
  
  for (let i = 0; i < props.barCount; i++) {
    const barHeight = 2; // Tiny height for idle state
    const x = startX + i * (props.barWidth + props.barGap);
    const y = height / 2 - barHeight / 2; // Center vertically
    
    ctx.fillRect(x, y, props.barWidth, barHeight);
  }
};

const setupAnalyser = async () => {
  try {
    // Get the audio stream
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // Create audio context
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(stream);
    
    // Create analyser
    analyser.value = audioContext.createAnalyser();
    analyser.value.fftSize = 256;
    
    // Connect source to analyser
    source.connect(analyser.value);
    
    // Set up data array
    const bufferLength = analyser.value.frequencyBinCount;
    dataArray.value = new Uint8Array(bufferLength);
    
    // Start visualization
    startVisualization();
  } catch (error) {
    console.error("Error setting up audio visualizer:", error);
  }
};

const startVisualization = () => {
  if (!canvasRef.value || !analyser.value || !dataArray.value) return;
  
  const canvas = canvasRef.value;
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  const activeColor = recorderStore.isRecording ? '#457b9d' : props.barColor;
  
  const draw = () => {
    // Only continue if still recording
    if (!recorderStore.isRecording) {
      cancelAnimationFrame(animationId.value);
      drawEmptyState();
      return;
    }
    
    animationId.value = requestAnimationFrame(draw);
    
    // Get frequency data
    analyser.value.getByteFrequencyData(dataArray.value);
    
    // Clear canvas with background color
    ctx.fillStyle = props.backgroundColor;
    ctx.fillRect(0, 0, width, height);
    
    // Calculate how many data points to use and where to start
    const numberOfBars = props.barCount;
    const totalBarWidth = numberOfBars * (props.barWidth + props.barGap);
    const startX = (width - totalBarWidth) / 2;
    const centerY = height / 2;
    
    // Choose a subset of frequency data for visualization
    const step = Math.floor(dataArray.value.length / numberOfBars);
    
    for (let i = 0; i < numberOfBars; i++) {
      const dataIndex = i * step;
      const barHeight = (dataArray.value[dataIndex] / 255) * (height / 2);
      const x = startX + i * (props.barWidth + props.barGap);
      const borderRadius = props.barWidth / 2; // Rounded corners

      ctx.fillStyle = activeColor;

      // Top half (rounded only on top)
      ctx.beginPath();
      ctx.roundRect(x, centerY - barHeight, props.barWidth, barHeight, [borderRadius, borderRadius, 0, 0]);
      ctx.fill();

      // Bottom half (rounded only on bottom)
      ctx.beginPath();
      ctx.roundRect(x, centerY, props.barWidth, barHeight, [0, 0, borderRadius, borderRadius]);
      ctx.fill();
    }

  };
  
  draw();
};

const stopVisualization = () => {
  if (animationId.value) {
    cancelAnimationFrame(animationId.value);
    animationId.value = null;
  }
  
  // Draw empty state
  drawEmptyState();
};
</script>

<template>
  <div class="audio-visualizer-container">
    <canvas 
      ref="canvasRef" 
      :width="width" 
      :height="height"
    ></canvas>
  </div>
</template>

<style scoped>
.audio-visualizer-container {
  margin: 1rem 0;
  display: flex;
  justify-content: center;
}
</style>