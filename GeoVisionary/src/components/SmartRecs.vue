<template>
  <!--  首页  -->
  <section>
    <!--  加载背景  -->
    <div class="loading-background" id="particles-background"></div>
    <img src="@/assets/mountain-fffdf3.svg" alt="logo" class="loading-logo" />
    <!--  正文  -->
    <div class="container section1">
      <el-carousel indicator-position="outside" height="100vh" :pause-on-hover="false" :interval="4000" class="carousel">
        <el-carousel-item v-for="item in data.carouselItems" :key="item">
          <img :src="item" alt="智荐学堂" loading="lazy" style="object-fit: fill;width: 100%;height: 100%;">
        </el-carousel-item>
      </el-carousel>
      <div class="section1-title">
        智荐学堂
      </div>
      <div class="section1-subtitle">
        在这里，智慧如星辰般璀璨，指引着你穿越地理的奥秘。每一次推荐都是心灵的启迪，揭开世界之书的一页页神奇篇章，引领探索者在知识的海洋中航行。
      </div>
    </div>
  </section>
  <!--  推荐页  -->
  <section>
    <div class="container section2">
      <div style="position:absolute;top: 20%;left: 20%;font-size: 32px;font-weight: bold;color: #0d0f1a;width: 500px;">此处展示推荐内容</div>
    </div>
  </section>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import ph1 from '@/assets/test/Rec-test-1.jpeg';
import ph2 from '@/assets/test/Rec-test-2.jpeg';
import ph3 from '@/assets/test/Rec-test-3.jpeg';
import ph4 from '@/assets/test/Rec-test-4.jpeg';
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { gsap } from "gsap";
import {enableScroll,disableScroll} from '@/store/usefulFunction.js'
gsap.registerPlugin(ScrollTrigger)

const data = reactive({
  carouselItems:[ph1,ph2,ph3,ph4],
})
let saveScrollPosition;

onMounted(() => {
  // 视差滚动
  gsap.fromTo('.carousel',{
    y: `-${window.innerHeight / 2}px`
  },{
    y:`${window.innerHeight / 2}px`,
    ease:'none',
    scrollTrigger: {
      trigger: '.section1',
      start: 'top bottom',
      end: 'bottom top',
      scrub:true,
    }
  });

  // 保存当前滚动位置
  saveScrollPosition = () => {
    localStorage.setItem('scrollPosition', window.scrollY);
  };
  window.addEventListener('beforeunload', saveScrollPosition);

  // 加载动画
  if(localStorage.getItem('scrollPosition') === '0'){
    (async function () {
      // 禁用滚动
      disableScroll()

      // 粒子背景消逝，主页出现
      particlesJS("particles-background", {
        particles: {
          number: { value: 60 },
          size: { value: 2 },
          move: { speed: 2 },
          opacity: { anim: { enable: true, speed: 0.5 } },
        },
      });
      const t = gsap.timeline()
      t.to("#particles-background", {opacity:0,duration:1.3,delay:0.7})
          .set('#particles-background', {zIndex:-10})

      // 主标题上升，副标题变上升变出现
      t.from(['.section1-title','.section1-subtitle'], {opacity:0,y:'+=100',duration:1.6},1)

      // logo移动至与导航栏重合并消失
      t.to('.loading-logo',{left:105,top:45,duration:1.1,width:50},0.7)
      // 重启滚动
      await t.set('.loading-logo',{display:'none',delay:0.4})
      enableScroll();
    })();
  } else {
    gsap.set(['.loading-logo','#particles-background'], {display:'none'});
  }
});
</script>

<style scoped>
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

/* 加载动画背景 */
.loading-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 90;
  background-color: #0d0f1a;
}

/* 加载背景logo */
.loading-logo {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 13%;
  height: auto;
  transform: translate(-50%, -50%);
  z-index: 91;
}

/* 首页大标题 */
.section1-title {
  font-size: 64px;
  font-weight: bold;
  text-align: center;
  position: absolute;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.6);
}

/* 首页副标题 */
.section1-subtitle {
  font-size: 20px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ddd;
  background: rgba(0, 0, 0, 0.5);
  padding: 10px 20px;
  border-radius: 8px;
  max-width: 60%;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}
</style>