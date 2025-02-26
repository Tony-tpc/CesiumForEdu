<template>
  <!--  首页 -->
  <section>
    <!--  加载背景  -->
    <Loading title=".section1-title" subtitle=".section1-subtitle"></Loading>
    <!--  正文  -->
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
      <!--  引导图片  -->
      <ScrollButton sectionName="#section2"></ScrollButton>
    </div>
  </section>
  <!--  测试 + 解析 -->
  <section>
    <div class="container section2" id="section2">
      <el-col :span="6" class="menu-column">
        <h2>试题分类</h2>
        <el-menu
            :unique-opened="true"
        >
          <el-sub-menu index="1">
            <template #title>
              <el-icon><Calendar /></el-icon>
              <span>年份</span>
            </template>
            <el-menu-item index="1-1">2024</el-menu-item>
            <el-menu-item index="1-2">2023</el-menu-item>
            <el-menu-item index="1-3">2022</el-menu-item>
            <el-menu-item index="1-4">2021</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="2">
            <template #title>
              <el-icon><Aim /></el-icon>
              <span>难易程度</span>
            </template>
            <el-menu-item index="2-1">困难</el-menu-item>
            <el-menu-item index="2-2">中等</el-menu-item>
            <el-menu-item index="2-3">简单</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="3">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>来源</span>
            </template>
            <el-menu-item index="3-1">新课标 I 卷</el-menu-item>
            <el-menu-item index="3-2">新课标 II 卷</el-menu-item>
            <el-menu-item index="3-3">全国甲卷</el-menu-item>
            <el-menu-item index="3-4">自主命题</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-col>
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
    </div>
  </section>
</template>

<script setup>
import { onMounted } from "vue";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { gsap } from "gsap";
gsap.registerPlugin(ScrollTrigger);

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

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}

/* 整个菜单栏外框 */
.menu-column {
  position: absolute;
  top: 8%;
  left: 0;
  height: 90%;
  width: 250px;
  background: var(--bg-color); /* 适配你的主题色 */
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 轻微阴影，增加立体感 */
  transition: all 0.3s ease-in-out;
}

/* 试题分类标题 */
.menu-column h2 {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-color);
  text-align: center;
  margin-bottom: 10px;
}

/* 侧边栏菜单 */
.el-menu {
  background: transparent !important; /* 让菜单栏背景透明 */
  border: none;
}

/* 每个子菜单（如年份 / 难度 / 来源） */
.el-sub-menu__title {
  font-size: 16px;
  font-weight: bold;
  color: var(--text-color);
  padding: 12px;
  transition: all 0.3s ease-in-out;
}

/* 子菜单悬停效果 */
.el-sub-menu__title:hover {
  background: rgba(0, 0, 0, 0.05) !important;
  border-radius: 8px;
}

/* 菜单项 */
.el-menu-item {
  font-size: 14px;
  color: var(--text-color);
  padding: 10px 16px;
  transition: all 0.3s ease-in-out;
}

/* 子菜单项悬停 */
.el-menu-item:hover {
  background: rgba(0, 0, 0, 0.1) !important;
  border-radius: 8px;
}

/* 选中状态 */
.el-menu-item.is-active {
  background: #40a2f6 !important; /* 适配你的主题色 */
  color: white !important;
  border-radius: 8px;
  font-weight: bold;
}

/* 图标 */
.el-icon {
  color: #0d0f1a;
  margin-right: 6px;
}


/* 排行榜 */
.leaderboard {
  position: absolute;
  top: 20%;
  right: 20%;
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

</style>