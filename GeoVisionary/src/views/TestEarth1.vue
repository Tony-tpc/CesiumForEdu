<template>
  <div class="LLM-input-output">
    <el-alert title="请注意，输入不能为空" type="error" center show-icon class="warning-alert" :closable="false"/>
    <div>
      <el-input
        v-model="data.textInput"
        :rows="2"
        type="textarea"
        resize="none"
        :autosize="{minRows: 1, maxRows: 6}"
        placeholder="您可以在这里输入您想和模型对话的内容！"
        class="inputArea"
      />
      <el-button v-if="!isGenerating" type="primary" @click="handleChatWithLocalLLM" class="submit-btn" :disabled="data.isDisabled">
        <el-icon  ><Top /></el-icon>
      </el-button>
      <el-button v-else type="primary" @click="handleStopLLMGeneration" class="submit-btn">
        <el-icon  ><Close /></el-icon>
      </el-button>
    </div>
    <div class="outputArea" @click="changeOutputArea">
      <ChatContent :showCursor="showCursor" :content="content"></ChatContent>
    </div>
  </div>
  <div class="live2Dmodel" @click="changeDisplay"></div>
<!--  <img src="@/assets/2k_earth_daymap.jpg" style="position: absolute;top: 0;left: 0;z-index: -10;" />-->
<!--  <div id="video-particles" class="particles-container"></div>-->
  <!--  <div class="test-fixed">我是测试 Fixed</div>-->
<!--  <div class="page2" id="earth-background">-->
<!--    <el-button type="primary" style="position: absolute;top: 250px;left: 300px">基本按钮</el-button>-->
<!--  </div>-->
<!--  <div class="page3">-->
<!--    <div style="position: absolute;top: 2000px;left: 100px;font-weight: bold;font-size: 30px">THIS IS MY WORLD!</div>-->
<!--  </div>-->
<!--  <div class="page4" id="star-background">-->

<!--  </div>-->

</template>

<script setup>
import {onBeforeUnmount, onMounted, reactive, ref, onUpdated} from "vue";
import { marked } from "marked";
import  DOMPurify from "dompurify";
import {userState} from "@/store/userStore.js"
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
// import MeteorClass from "@/classes/meteor.js";
// import * as THREE from "three";
import {gsap} from "gsap";
import {ScrollTrigger} from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger)

// let resize

const data = reactive({
  percentage:0,
  textInput:"",
  changeArea:false,
  displayEverything:true,
  isDisabled:false,
  x:0,
  y:0,
})

const content = ref('');
const showCursor = ref(false);
// const responseText = ref(""); // 逐步存放 LLM 生成的内容
// const responseHTML = ref(""); // 存储解析后的 HTML
const isGenerating = ref(false); // 控制加载状态
const outputArea = ref(null);
let controller = new AbortController();  // 用于控制请求
let reader = null;  // 读取流

// 找到最后一个非空的文本结点
const getLastTextNode = (dom) => {
  const children = dom.childNodes;
  for(let i = children.length - 1; i >= 0; i--) {
    const node = children[i];
    if(node.nodeType === Node.TEXT_NODE && /\S/.test(node.nodeValue)) {
      node.nodeValue = node.nodeValue.replace(/\s+$/,"");
      return node;
    } else if(node.nodeType === Node.ELEMENT_NODE) {
      const last = getLastTextNode(node);
      if (last) {
        return last;
      }
    }
  }
  return null;
}

// 更新光标
const updateCursor = () => {
  const outputAreaDom = outputArea.value;
  const lastText = getLastTextNode(outputAreaDom);
  const textNode = document.createTextNode('\u200b');
  if (lastText) {
    lastText.parentElement.appendChild(textNode);
  } else {
    outputAreaDom.appendChild(textNode);
  }
  const domRect = outputAreaDom.getBoundingClientRect();
  const range = document.createRange();
  range.setStart(textNode,0);
  range.setEnd(textNode,0);
  const rect = range.getBoundingClientRect();
  data.x = rect.left - domRect.left;
  data.y = rect.top - domRect.top;
  textNode.remove();
};

const chatHistory = ref([
  { role: "system", content: "你是一位地理老师，你的学生目前遇到了一些地理问题，你需要耐心且详尽地帮助他解决问题，并通俗易懂地讲解。如果他输入的是其他方面的问题，也请像个老师一样耐心教导他。" }
]);

// 向本地LLM发送流式请求
const chatWithLocalLLM = async () => {
  content.value = ""; // 清空历史内容
  isGenerating.value = true; // 进入生成状态
  showCursor.value = true; // 显示光标

  // 检验localStorage，需删除！！！
  localStorage.setItem("text", '我向本地LLM发送了请求');

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
}

// 放大输出结果
const changeOutputArea = () => {
  if (!data.changeArea) {
    gsap.timeline()
        .to('.outputArea',{top:'10%',height:'48%'})
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
    gsap.timeline()
        .set(['.outputArea','.inputArea','.submit-btn'],{display:'block'})
        .to(['.outputArea','.inputArea','.submit-btn'],{opacity:1,ease:'power2.in'})
    data.displayEverything = true;
  }
}

onMounted(() => {
  /* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
  // particlesJS("video-particles", {
  //   particles: {
  //     number: { value: 60 },
  //     size: { value: 2 },
  //     move: { speed: 2 },
  //     opacity: { anim: { enable: true, speed: 0.5 } },
  //   },
  // });



// // 地球
//   const textureLoader = new THREE.TextureLoader();
//   const earthTexture = textureLoader.load('/src/assets/2k_earth_daymap.jpg');
//   const earthGeometry = new THREE.SphereGeometry(1, 32, 32);
//   const earthMaterial = new THREE.MeshStandardMaterial({ map: earthTexture });
//   const earth = new THREE.Mesh(earthGeometry, earthMaterial);
//   scene.add(earth);
//
// // 光源
//   const ambientLight = new THREE.AmbientLight(0x404040);
//   scene.add(ambientLight);
//
//   const pointLight = new THREE.PointLight(0xffffff, 50);
//   pointLight.position.set(5, 5, 5);
//   scene.add(pointLight);
//
// // 星空
//   const starsGeometry = new THREE.SphereGeometry(50, 64, 64);
//   const starsMaterial = new THREE.MeshBasicMaterial({
//     map: textureLoader.load('https://api.allorigins.win/get?url=' + encodeURIComponent('https://example.com/stars_texture.jpg')),
//     side: THREE.BackSide,
//   });
//   const stars = new THREE.Mesh(starsGeometry, starsMaterial);
//   scene.add(stars);
//
// // 动画
//   function animate() {
//     requestAnimationFrame(animate);
//     earth.rotation.y += 0.005;
//     controls.update();
//     renderer.render(scene, camera);
//   }
//
//   animate();

  // // 创建星空部分
  // (function (){
  //   const starScene = new THREE.Scene();
  //   const starCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
  //   const starRenderer = new THREE.WebGLRenderer({ alpha: true });
  //   starRenderer.setSize(
  //       document.getElementById('star-background').offsetWidth,
  //       document.getElementById('star-background').offsetHeight
  //   );
  //   starRenderer.setClearColor(0x0d0f1a)
  //   document.getElementById('star-background').appendChild(starRenderer.domElement);
  //   // 创建星空粒子
  //   const starsGeometry = new THREE.BufferGeometry();
  //   const starsVertices = [];
  //   for (let i = 0; i < 800; i++) {  // 800 颗星星
  //     let x = (Math.random() - 0.5) * 2000;
  //     let y = (Math.random() - 0.5) * 2000;
  //     let z = (Math.random() - 0.5) * 2000;
  //     starsVertices.push(x, y, z);
  //   }
  //   starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
  //   const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
  //   const starField = new THREE.Points(starsGeometry, starsMaterial);
  //   starScene.add(starField);
  //
  //   const meteors = []; // 用于存储流星实例
  //
  //   const meteorConfigs = [
  //     { color: { left: new THREE.Color("#0000ff"), right: new THREE.Color("#00ffff") }, duration: 1.2, hideDuration: 1, position: new THREE.Vector3(25,  25, -150), target: new THREE.Vector3(250,30, -150) }, // 左侧
  //     { color: { left: new THREE.Color("#00aaff"), right: new THREE.Color("#ffffff") }, duration: 1.8, hideDuration: 0.6, position: new THREE.Vector3(50,  17, 0),  target: new THREE.Vector3(430,430, 0) }, // 中间
  //     { color: { left: new THREE.Color("#ffffff"), right: new THREE.Color("#0000ff") }, duration: 1.9, hideDuration: 0.7, position: new THREE.Vector3(60,  -6, 0),  target: new THREE.Vector3(400, 400, 0) } // 右侧
  //   ];
  //
  //   meteorConfigs.forEach(config => {
  //     const meteor = new MeteorClass(
  //         1000,
  //         config.target, // 目的地
  //         config.color, // 颜色
  //         1,
  //         config.duration, // 飞行时长
  //         config.hideDuration, // 消失时长
  //     );
  //     starScene.add(meteor.group);
  //     // 将流星组的位置设置为配置中的位置
  //     meteor.group.position.set(config.position.x, config.position.y, config.position.z);
  //     // 旋转流星组
  //     meteor.group.rotateZ(Math.PI / 0.9);
  //     meteors.push(meteor);
  //   });
  //
  //   starCamera.position.z = 50;
  //   function starAnimate() {
  //     requestAnimationFrame(starAnimate);
  //     starField.rotation.y += 0.0002;  // 缓慢旋转
  //     meteors.forEach(meteor => meteor.update()); // 更新所有流星
  //     starRenderer.render(starScene, starCamera);
  //   }
  //   starAnimate();
  //
  //   // 添加 resize 事件监听器以及时调整窗口大小
  //   resize = () => {
  //     const width = document.getElementById('star-background').offsetWidth;
  //     const height = document.getElementById('star-background').offsetHeight;
  //
  //     starRenderer.setSize(width, height);
  //     starCamera.aspect = width / height;
  //     starCamera.updateProjectionMatrix();
  //   };
  //   window.addEventListener('resize', resize);
  //   resize(starRenderer,starCamera);
  //
  // })();
})
onBeforeUnmount( () => {
  // window.removeEventListener('resize',resize);
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
  position: absolute;
  bottom: 10%;
  left: 25%;
  width: 52%;
  font-size: 16px;
  border-radius: 50px !important;
  z-index: 1;
}

/* 输入按钮 */
.submit-btn {
  position: absolute;
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
  z-index: 1;
}

/* 空输入提示 */
.warning-alert {
  position: absolute;
  top: 9%;
  right: 25%;
  width: 24%;
  transform: translateX(-50%);
  border-radius: 20px;
  opacity: 0;
  pointer-events: none;
}

/* LLM输出框 */
.outputArea {
  position: absolute;
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
}


/* live2D模型 */
.live2Dmodel {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20%;
  height: 60%;
  background-color: #0d0f1a;
}

.background {
  position: absolute;
  display: block;
  top: 0;
  left: 0;
  z-index: 0;
}


.page2 {
  position: absolute;
  width: 100%;
  height: 100vh;
  top: 100vh;
}


/* 第二部分，根据需要加长 */
.section2 {
  position: absolute;
  top: 100vh;
  height: 170vh;
}
/* 过渡文字 */
.transition-words {
  position: absolute;
  top: 12%;
  left: 35%;
  height: auto;
  font-size: 48px;
  font-weight: bold;
  color: rgba(0,0,0,0.5);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
}
/* 过渡文字中需要强调的文字 */
.c1,.c2,.c5 {
  color: #f94604;
}
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: var(--bg-color);
  overflow: hidden;
}
/* 进度条 */
.progress {
  position: absolute;
  top: 50%;
  left: 15%;
  width: 75%;
  height: auto;
  z-index: 5;
}

.step-indicator {
  display: inline-block;
  padding: 6px 16px;
  background: var(--secondary-color);
  color: white;
  font-size: 16px;
  font-weight: bold;
  border-radius: 20px;
}
.section-content {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  max-width: 600px;
  line-height: 1.6;
  text-align: left;
  transform: translateY(20px);
}
.section-subtitle {
  font-size: 24px;
  font-weight: 400;
  color: #e0e0e0;
  transform: translateY(20px);
}
.section-title {
  font-size: 48px;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
}

.page2,.page3,.page4,.page5 {
  position: absolute;
  top: 45px;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: #333333;
  z-index: 0;
}
.page3 {
  background-color: #999999;
}
.page4 {
  background-color: red;
}
.page5 {
  background-color: blue;
}
.test-fixed {
  position: fixed;
  top: 50px;
  left: 50px;
  background: red;
  color: white;
  padding: 10px;
  z-index: 9999;
}
</style>
