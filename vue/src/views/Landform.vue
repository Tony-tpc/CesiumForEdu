<template>
  <section>
    <div class="video-background">
      <video src="@/assets/Cesium-test.mp4" loop autoplay muted loading="lazy" class="video1"></video>
    </div>
  </section>
</template>

<script setup>

</script>

<style scoped>
.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
}

.video1 {
  width: 100%;
  height: 100%;
  object-fit: fill;
}
</style>