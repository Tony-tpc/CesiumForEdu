<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <el-carousel height="500px" style="width: 700px">
      <el-carousel-item v-for="item in data.imgs" :key="item">
        <img style="height: 500px;width:700px" :src="item" alt="展示">
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup>
import { reactive} from "vue";
import ph1 from "@/assets/地形.jpeg"
import ph2 from "@/assets/月相.jpeg"
import ph3 from "@/assets/气候.jpeg"
import ph4 from "@/assets/人文.jpg"

const data = reactive({
  imgs:[ph1,ph2,ph3,ph4],
})
</script>