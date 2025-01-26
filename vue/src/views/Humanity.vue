<template>
  <div class="box"></div>
</template>

<script setup>
import { onMounted } from 'vue';
import { gsap } from 'gsap';

onMounted(() => {
  gsap.to(".box", {
    x: 500,
    y: 500,
    duration: 3,
  });
});
</script>

<style scoped>
.box {
  height: 50px;
  width: 50px;
  background-color: pink;
}
</style>