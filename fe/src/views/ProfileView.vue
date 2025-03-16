<script setup>
import Signup from '@/components/Profile/Signup.vue';
import Login from '@/components/Profile/Login.vue';
import { useAuthStore } from '@/stores/useAuthStore';
import { RouterLink } from 'vue-router';
import { ref, reactive, onMounted } from 'vue';
import { getChartData } from '@/api/apiClient';

const authStore = useAuthStore();
const showLogin = ref(true);

const toggleLogin = () => {
  showLogin.value = !showLogin.value;
};

// Chart options with dual Y-axes
const chartOptions = reactive({
  chart: {
    id: 'performance-over-time',
    toolbar: { show: false }
  },
  xaxis: {
    categories: []
  },
  dataLabels: { enabled: false },
  colors: ['#008FFB', '#FF4560'], // Blue for duration, Red for counted examples
  stroke: { curve: 'smooth' },
  yaxis: [
    {
      title: { text: 'Průměrný čas počítání příkladu (ms)' },
      opposite: false // Left Y-axis
    },
    {
      title: { text: 'Spočítaných příkladů za den' },
      opposite: true 
    }
  ]
});

const chartSeries = ref([]);

const fetchData = async () => {
  try {
    const studentId = 1;
    const avgDurationData = await getChartData(studentId, "duration");
    const countedExamplesData = await getChartData(studentId, "examples");

    chartOptions.xaxis.categories = avgDurationData.categories;
    chartSeries.value = [
      { name: "Průměrný čas počítání", data: avgDurationData.series[0].data, type: "line", yAxisIndex: 0 },
      { name: "Spočítaných příkladů", data: countedExamplesData.series[0].data, type: "line", yAxisIndex: 1 }
    ];
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

onMounted(fetchData);
</script>

<template>
  <div v-if="authStore.isAuthenticated" class="w-full text-4xl text-primary flex flex-col items-center justify-center font-bold pt-12">
    <p>Ahoj {{ authStore.name }}!</p>
    <!---
    <div class="w-full max-w-5xl px-4"> 
      <apexchart type="line" height="400" :options="chartOptions" :series="chartSeries"></apexchart>
    </div> -->
  </div>

  <div v-else>
    <Login v-if="showLogin" />
    <Signup v-else />

    <button @click="toggleLogin" class="underline w-full text-secondary text-lg">
      {{ showLogin ? "Ještě nemám účet - registrovat se" : "Už mám účet - přihlásit se" }}
    </button>
    <RouterLink to="/admin" class="underline w-full text-secondary text-lg mt-12 flex justify-center">
      Jsem administrátor aplikace
    </RouterLink>
  </div>
</template>

