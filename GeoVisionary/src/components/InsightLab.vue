<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <!--   背景图   -->
      <img src="@/assets/test/Quiz-test.jpg" alt="探知问学" loading="lazy" class="background-photo"/>
      <!--   标题   -->
      <div class="section1-title">
        探知问学
      </div>
      <div class="section1-subtitle">
        在这片智慧的天地里，每一道问题都是通往大自然奥秘的钥匙。通过测试与解析，你将踏上心灵之旅，深挖地理的千丝万缕，揭开知识的面纱。
      </div>
      <!--   排行榜   -->
      <div class="leaderboard">
        <h3 class="leaderboard-title">🏆 排行榜</h3>
        <ul class="leaderboard-list">
          <li class="leaderboard-item first">🥇 张三 - 98分</li>
          <li class="leaderboard-item second">🥈 李四 - 95分</li>
          <li class="leaderboard-item third">🥉 王五 - 92分</li>
          <li class="leaderboard-item">赵六 - 88分</li>
          <li class="leaderboard-item">孙七 - 85分</li>
        </ul>
      </div>
      <!--  引导图片  -->
      <div class="continue-div">
        <el-button class="continue-button" @click="scrollToSection2">
          <img src="@/assets/continue.svg" alt="继续" loading="lazy" class="continue-photo"/>
        </el-button>
      </div>
    </div>
  </section>
  <!--  测试 + 解析 -->
  <section>
    <div class="container section2" id="section2">
      <div style="position:absolute;top: 20%;left: 20%;font-size: 32px;font-weight: bold;color: #0d0f1a;width: 500px;">此处展示测试内容</div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from "vue";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
import { gsap } from "gsap";
gsap.registerPlugin(ScrollTrigger,ScrollToPlugin);

const scrollToSection2 = () => {
  gsap.to(window,{
    scrollTo:"#section2",
    duration:0.8,
  })
};

onMounted(() => {
  // 第一屏
  (function () {
    // 展示模型动画
    ScrollTrigger.create({
      trigger:'.section1',
      start:'top+=100 top',
      end:'+=300',
      scrub:true,
      animation:
          gsap.timeline()
              .from('.section2',{opacity:0})
    });

    // 引导动画
    gsap.timeline({repeat:-1})
        .from('.continue-photo',{y:'-=30',opacity:0,duration:0.9,ease:'none'})
        .to('.continue-photo',{y:'+=30',opacity:0,duration:0.9,ease:'none'})
  })();

  // 视差滚动
    gsap.fromTo('.background-photo',
        { y: `-${window.innerHeight / 2}px` }, // 起始位置
        { y: `${window.innerHeight / 2}px`,
          ease: "none",
          scrollTrigger: {
            trigger: '.section1',
            start: "top bottom",
            end: "bottom top",
            scrub: true,
          }
        }
    );


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
  font-family: cursive;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
}

/* 首页副标题 */
.section1-subtitle {
  font-size: 20px;
  font-weight: normal;
  text-align: center;
  position: absolute;
  top: 49%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-family: cursive;
  padding: 8px 10px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* 背景图 */
.background-photo {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 排行榜 */
.leaderboard {
  position: absolute;
  top: 20%;
  right: 2%;
  width: 300px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3); /* 半透明黑板质感 */
  border-radius: 10px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
}

.leaderboard-title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  color: #fff;
  font-family: "Chalkduster", "Comic Sans MS", cursive;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.leaderboard-list {
  list-style: none;
  padding: 0;
  margin: 10px 0 0;
}

.leaderboard-item {
  font-size: 20px;
  font-family: "Chalkduster", "Comic Sans MS", cursive;
  color: #fff;
  padding: 10px;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.5);
  transition: transform 0.2s ease-in-out;
}

.leaderboard-item:hover {
  transform: scale(1.05);
}

/* 前三名颜色 */
.first {
  color: gold;
}
.second {
  color: silver;
}
.third {
  color: #cd7f32;
}

/* 引导背景 */
.continue-div {
  position: absolute;
  bottom: 5%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  align-items: center;
  justify-content: center;
  border-radius: 100%;
  background-color: #fffdf3;
  z-index: 3;
}

/* 引导按钮 */
.continue-button {
  width: 100%;
  height: 100%;
  background-color: transparent;
  border: none;
  border-radius: 100%;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}
</style>