<!--
================================================================================
 Component: Spinner.vue
 Description:
        Spinner to signal loading state of page or component.
 Author: Dominik Horut (xhorut01)
================================================================================
-->

<template>
    <div class="flex items-center justify-center space-x-8 my-8">
      <span class="w-5 h-5 bg-primary rounded-full animate-bounce duration-1000 ease-in-out"></span>
      <span class="w-5 h-5 bg-primary rounded-full animate-bounce duration-1000 ease-in-out [animation-delay:200ms]"></span>
      <span class="w-5 h-5 bg-primary rounded-full animate-bounce duration-1000 ease-in-out [animation-delay:400ms]"></span>
    </div>
</template>
  
<style scoped>
  @keyframes bounce {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-12px);
    }
  }
</style>
  
  