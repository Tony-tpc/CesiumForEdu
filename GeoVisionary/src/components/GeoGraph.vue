<template>
  <section>
    <!--  加载背景  -->
    <Loading title=".section1-title" subtitle=".section1-subtitle"></Loading>
  </section>
  <section>
    <div>
      <!--  Live2D -->
      <canvas ref="canvas" class="live2Dmodel" @click="changeDisplay"></canvas>
      <div class="LLM-input-output">
        <el-alert title="请注意，输入不能为空" type="error" center show-icon class="warning-alert" :closable="false"/>
        <div>
          <el-input
              v-model="data.textInput"
              :rows="2"
              type="textarea"
              resize="none"
              :autosize="{minRows: 1, maxRows: 4}"
              placeholder="您可以在这里输入您想和小助教对话的内容！"
              class="inputArea"
              @keydown="handleKeydown"
          />
          <el-button v-if="!isGenerating" type="primary" @click="handleChatWithLocalLLM" class="submit-btn" :disabled="data.isDisabled">
            <el-icon  ><Top /></el-icon>
          </el-button>
          <el-button v-else type="primary" @click="handleStopLLMGeneration" class="stop-btn">
            <el-icon  ><Close /></el-icon>
          </el-button>
        </div>
        <div class="outputArea" @click="changeOutputArea">
          <ChatContent :showCursor="showCursor" :content="content"></ChatContent>
        </div>
      </div>
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
    <ScrollButton sectionName="#section2" style="z-index: 9"></ScrollButton>
  </section>
  <!--  图谱展示页  -->
  <section>
    <div class="container section2" id="section2">
      <div style="position:absolute;top: 20%;left: 20%;font-size: 32px;font-weight: bold;color: #0d0f1a;width: 500px;">此处展示知识图谱</div>
    </div>
  </section>
</template>

<script setup>
import * as PIXI from 'pixi.js';
import { Live2DModel } from 'pixi-live2d-display/cubism4';
import { ref, onMounted, onUnmounted, reactive } from 'vue';
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

window.PIXI = PIXI;

const data = reactive({
  textInput:"",
  changeArea:false,
  displayEverything:false,
  isDisabled:false,
})

const canvas = ref(null);
const app = ref(null);
const model = ref(null);
const content = ref('');
const showCursor = ref(false);
const isGenerating = ref(false); // 控制加载状态
let controller = new AbortController();  // 用于控制请求
let reader = null;  // 读取流

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
    model.value.x = -120;

    console.log("Live2D 模型加载成功");
  } catch (error) {
    console.error("加载失败", error);
  }
}

// 更新live2D位置
const updatePosition = () => {
  model.value.x = -0.05 * window.innerWidth;
};

const chatHistory = ref([
  { role: "system", content: "你是一位经验丰富的地理老师，你的学生目前遇到了一些地理问题，你需要耐心地帮助他解决问题，并通俗易懂地讲解。如果他输入的是其他方面的问题，也请像个老师一样耐心教导他。记住，你只能用中文思考和回答。" }
]);

// 向本地LLM发送流式请求
const chatWithLocalLLM = async () => {
  content.value = ""; // 清空历史内容
  isGenerating.value = true; // 进入生成状态
  showCursor.value = true; // 显示光标

  // 创建新的控制器
  controller = new AbortController();
  const signal = controller.signal;

  if(data.textInput) {
    // 把用户输入添加到历史记录
    chatHistory.value.push({ role: "user", content: data.textInput });
    try {
      const response = await fetch("http://localhost:1234/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "deepseek-r1-distill-qwen-14b", // phi-4 deepseek-r1-distill-llama-8b deepseek-r1-distill-qwen-14b
          messages: chatHistory.value,
          temperature: 0.6,
          max_tokens: 8192,
          stream: true, // 启用流式返回
        }),
        signal, // 绑定信号
      });

      if (!response.ok || !response.body) throw new Error("LLM 请求失败");

      // 获取可读流
      reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // 先解码成字符串
        const chunk = decoder.decode(value, { stream: true });

        // 解析 JSON，提取内容
        const lines = chunk.split("\n"); // API 可能返回多行
        for (const line of lines) {
          if (line.trim().startsWith("data:")) {
            try {
              const json = JSON.parse(line.replace("data: ", ""));
              if (json.choices && json.choices[0].delta.content) {
                content.value += json.choices[0].delta.content; // 追加生成的文本
              }
            } catch (err) {
              console.error("解析错误:", err);
            }
          }
        }
      }
      // 生成完成后，把 LLM 的回复也加入历史记录
      chatHistory.value.push({ role: "assistant", content: content.value });
      console.log(chatHistory.value);
    } catch (error) {
      if (error.name === "AbortError") {
        console.log("LLM 请求已被取消");
      } else {
        console.error("LLM 生成错误:", error);
      }
    } finally {
      isGenerating.value = false; // 结束生成状态
      showCursor.value = false; // 隐藏光标
    }
  }
};

// 中断LLM生成函数
const stopLLMGeneration = () => {
  if (isGenerating.value) {
    controller.abort();  // 终止 fetch 请求
    if (reader) reader.cancel();  // 终止流读取
    isGenerating.value = false;
    console.log("LLM 输出已中断");
  }
};

// 点击交互按钮
const handleChatWithLocalLLM = () => {
  if (data.textInput) {
    chatWithLocalLLM();
    data.textInput = "";
  } else  {
    data.isDisabled = true;
    gsap.to('.warning-alert',{y:'+=20',opacity:1,duration:0.7,pointerEvents:'auto',ease:'none'});
    setTimeout( async () => {
      await gsap.to('.warning-alert',{y:'-=20',opacity:0,duration:0.7,pointerEvents:'none',ease:'none'});
      data.isDisabled = false;
    },3000)
  }
}

// 点击终止按钮
const handleStopLLMGeneration = () => {
  stopLLMGeneration();
  setTimeout(() => {
    const submitBtn = document.querySelector('.submit-btn');
    if (!submitBtn) {
      console.warn("按钮不存在，无法设置样式");
      return;
    }
    submitBtn.style.display = "block";
    submitBtn.style.opacity = "1";
  }, 40);  // 让浏览器有时间渲染 `.submit-btn`
}

// 点击回车交互
const handleKeydown = (e) => {
  if (e.key === "Enter") {
    if (!e.shiftKey) {
      e.preventDefault();
      handleChatWithLocalLLM();
    }
  } else if (e.key === "Escape" && isGenerating.value) {
    handleStopLLMGeneration();
  }
}

// 放大输出结果
const changeOutputArea = () => {
  if (!data.changeArea) {
    gsap.timeline()
        .to('.outputArea',{top:'10%',height:'55%'})
    data.changeArea = true;
  } else {
    gsap.timeline()
        .to('.outputArea',{top:'20%',height:'30%'})
    data.changeArea = false;
  }
}

// 显示/隐藏输入/输出/提交按钮
const changeDisplay = () => {
  if (data.displayEverything) {
    gsap.timeline()
        .to(['.outputArea','.inputArea','.submit-btn'],{opacity:0,ease:'power2.out'})
        .set(['.outputArea','.inputArea','.submit-btn'],{display:'none'})
    data.displayEverything = false;
  } else {
    gsap.set(['.outputArea','.inputArea','.submit-btn'],{display:'block'});
    gsap.to(['.outputArea','.inputArea','.submit-btn'],{opacity:1,ease:'power2.in'});
    data.displayEverything = true;
  }
}

onMounted(() => {
  window.addEventListener('resize', updatePosition);
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

// 组件卸载时销毁 WebGL 资源，停止对话
onUnmounted(() => {
  if (app.value) {
    app.value.destroy(true);
    app.value = null;
    model.value = null;
  }
  window.removeEventListener('resize', updatePosition);
  stopLLMGeneration();
});

</script>

<style scoped>
/* 用户输入框 */
:deep(.el-textarea__inner) {
  border-radius: 12px !important;
  line-height: 1.8 !important;
  padding-bottom: 30px;
}
.inputArea {
  position: fixed;
  bottom: 10%;
  left: 25%;
  width: 52%;
  font-size: 16px;
  border-radius: 50px !important;
  z-index: 11;
  display: none;
  opacity: 0;
}

/* 输入按钮 */
.submit-btn,.stop-btn {
  position: fixed;
  bottom: 11%;
  right: 24%;
  width: 30px;
  height: 30px;
  border-radius: 100%;
  margin: 0;
  padding: 7px 0;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  z-index: 12;
  display: none;
  opacity: 0;
}

.stop-btn {
  display: block;
  opacity: 1;
}

/* 空输入提示 */
.warning-alert {
  position: fixed;
  top: 9%;
  right: 25%;
  width: 24%;
  transform: translateX(-50%);
  border-radius: 20px;
  opacity: 0;
  pointer-events: none;
  z-index: 15;
}

/* LLM输出框 */
.outputArea {
  position: fixed;
  top: 20%;
  left: 25%;
  width: 50%;
  height: 30%;
  color: #0d0f1a;
  border: 1px solid #0d0f1a;
  border-radius: 30px;
  padding: 15px;
  font-size: 16px;
  overflow-y: auto;
  overflow-x: hidden;
  line-height: 1.8;
  z-index: 11;
  display: none;
  opacity: 0;
  background-color: rgba(0,0,0,.8);
}

/* Live2D */
canvas {
  position: fixed;
  top: 40%;
  right: -35%;
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