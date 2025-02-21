<template>
  <!--  Live2D -->
  <section>
    <div>
      <canvas ref="canvas" class="live2Dmodel"></canvas>
    </div>
  </section>
  <!--  首页背景图及标题 -->
  <section>
    <div class="container section1">
      <img src="@/assets/Full-Graph-test-1.png" alt="知象图谱" loading="lazy" class="image1">
      <img src="@/assets/Full-Graph-test-2.jpg" alt="知象图谱" loading="lazy" class="image2">
    </div>
    <div class="section1-title">
      知象图谱
    </div>
    <div class="section1-subtitle">
      在这里，大自然的智慧以线条与节点的形式呈现，连接着山川、星辰及气候的宏伟交响。每一次探索都是心灵之旅，带你穿越知识的海洋，领略地理之美的无限可能。
    </div>
  </section>
  <!--  图谱展示页  -->
  <section>
    <div class="container section2">
      <div style="position:absolute;top: 20%;left: 20%;font-size: 32px;font-weight: bold;color: #0d0f1a;width: 500px;">此处展示知识图谱</div>
    </div>
  </section>
</template>

<script setup>
import * as PIXI from 'pixi.js';
import { Live2DModel } from 'pixi-live2d-display/cubism4';
import { ref, onMounted, onUnmounted } from 'vue';
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

window.PIXI = PIXI;

const canvas = ref(null);
const app = ref(null);
const model = ref(null);

// 封装 Live2D 加载逻辑
const loadLive2D = async () => {
  try {
    // 如果存在 PIXI 实例，便销毁
    if (app.value) {
      console.log("销毁旧的 PIXI 应用");
      app.value.destroy(true); // 彻底销毁 PIXI
      app.value = null;
      model.value = null;
    }

    // 初始化 PIXI 应用
    app.value = new PIXI.Application({
      view: canvas.value,
      autoStart: true,
      x: 0,
      y: 0,
      backgroundAlpha: 0,
      autoDensity: true,
      antialias: true,
      resolution: window.devicePixelRatio,
    });

    // 加载 Live2D 模型
    // "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json"
    // "/maolili/mailili.model3.json"
    model.value = await Live2DModel.from("https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json");
    app.value.stage.addChild(model.value);

    // 调整模型大小
    model.value.scale.set(0.2);

    console.log("Live2D 模型加载成功");
  } catch (error) {
    console.error("加载失败", error);
  }
}

onMounted(() => {
  // 页面轮播图动画
  gsap.timeline({repeat:-1})
      .to('.image1',{opacity:1,scale:1,duration:3,ease:'none'})
      .to('.image1',{opacity:0,scale:0.75,duration:3,ease:'none'})
      .to('.image2',{opacity:1,scale:1,duration:3,ease:'none'})
      .to('.image2',{opacity:0,scale:0.75,duration:3,ease:'none'})

  // 加载 Live2D
  loadLive2D();

  // 展示模型动画
  ScrollTrigger.create({
    trigger:'.section2',
    start:'top-=400 top',
    end:'+=200',
    scrub:true,
    animation:
        gsap.timeline()
            .to('.section1',{y:'-=100',opacity:0})
            .from('.section2',{y:'+=100',opacity:0},"<")
  })
});

// 组件卸载时销毁 WebGL 资源
onUnmounted(() => {
  if (app.value) {
    app.value.destroy(true);
    app.value = null;
    model.value = null;
  }
});

</script>

<style scoped>
/* Live2D */
canvas {
  position: fixed;
  top: 40%;
  right: -25%;
  border: none;
  z-index: 100;
}

/* 公共容器 */
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* 第一屏 */
.section1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 5;
  overflow-x: hidden;
}

/* 轮播图图片 */
.image1,.image2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  scale: 1.25;
  z-index: 1;
}

/* 首页大标题 */
.section1-title {
  position: absolute;
  top: 35%;
  left: 50%;
  font-size: 64px;
  font-weight: bold;
  text-align: center;
  transform: translate(-50%, -50%);
  color: #33aaeb; /* 深蓝青色，增强对白色背景的对比度 */
  text-shadow: 0 0 8px rgba(29, 168, 202, 0.6),
  0 0 16px rgba(31, 139, 166, 0.4); /* 适度光晕，减少眩光感 */
  z-index: 10;
}

/* 首页副标题 */
.section1-subtitle {
  font-size: 18px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #d6f5ff;
  background: rgba(0, 0, 0, 0.5);
  padding: 10px 20px;
  border-radius: 6px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  z-index: 10;
}


/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}
</style>