<template>
  <SwitchButton v-model="isDarkMode" :className="'my-menu'"/>
</template>

<script setup>
import { ref } from 'vue';
const isDarkMode = ref(false);
</script>

<style scoped>
.my-menu {
  font-size: 15px;
  line-height: 27px;
  img {
    width: 15px;
    height: 15px;
  }
}
</style>