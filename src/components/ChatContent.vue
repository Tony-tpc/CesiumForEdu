<script setup>
import 'github-markdown-css/github-markdown-dark.css';
import { marked } from 'marked'
import DOMPurify from "dompurify";
import { computed, ref, reactive, onMounted, onUpdated } from "vue";
import hljs from 'highlight.js'
import 'highlight.js/styles/dark.css'

// 参数
const props = defineProps({
  content: {
    type: String,
    required: true,
  },
  showCursor: {
    type: Boolean,
    default: false,
  }
});

const isRotated = ref(false);
const handleFoldButton = () => {
  // 旋转icon
  const arrowIcon = document.querySelector('.arrow-down-icon');

  if (!isRotated.value) {
    arrowIcon.style.transform = 'rotate(180deg)';
    isRotated.value = true;
  } else {
    arrowIcon.style.transform = 'rotate(0deg)';
    isRotated.value = false;
  }

  // 设置展示
  const thinkingDetail = document.querySelector('.thinking-detail');

  if (isRotated.value) {
    thinkingDetail.style.height = 'auto';
    const { height } = thinkingDetail.getBoundingClientRect();
    thinkingDetail.style.height = 0;
    thinkingDetail.style.transition = '0.5s';
    thinkingDetail.getBoundingClientRect();
    thinkingDetail.style.padding = '12px 10px';
    thinkingDetail.style.height = height + 'px';
  } else {
    thinkingDetail.style.height = 0;
    thinkingDetail.style.padding = '0 10px';
  }
}

// 允许 think 标签
DOMPurify.addHook('uponSanitizeElement', (node, data) => {
  if (data.tagName === 'think') {
    data.allowed = true;
  }
});

// 设置代码属性
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  }
});

// 处理markdown格式文本
const markdownContent = computed(() => {
  if (props.content) {
    if (props.content.includes("<think>")) {
      const reducedContent = props.content.replace('<think>','');
      if (reducedContent.includes("</think>")) {
        const resArr = reducedContent.split("</think>")
        const thinkingStr = `
      <div style="position: relative;top: 0;left: 0;width: 100%;height: 100%;">
          <div>
            <el-button type="primary" class="fold-button"
            @click="handleFoldButton">点击展开&nbsp;&nbsp;
            <el-icon class="arrow-down-icon"><ArrowDown/></el-icon>
          </el-button>
         </div>
         <div class="thinking-container">
              <think class="thinking-detail">${resArr[0]}</think>
         </div>
      </div>`
        console.log(`thinkingStr: ${thinkingStr}`);
        return thinkingStr + DOMPurify.sanitize(marked.parse(resArr[1]));
      } else {
        const thinkingStr = `
      <div>
        <think class="thinking-detail">${reducedContent}</think>
      </div>`

        return thinkingStr;
      }
    } else {
      return DOMPurify.sanitize(marked.parse(props.content));
    }
  }
});

// 响应式光标
const pos = reactive({x: 0, y: 0});
const contentRef = ref(null);

// 找到最后一个非空的文本结点
const getLastTextNode = (dom) => {
  const children = dom.childNodes;
  for (let i = children.length - 1; i >= 0; i--) {
    const node = children[i];
    if (node.nodeType === Node.TEXT_NODE && /\S/.test(node.nodeValue)) {
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
  const contentDom = contentRef.value;
  const lastText = getLastTextNode(contentDom);
  const textNode = document.createTextNode('\u200b');
  if (lastText) {
    lastText.parentElement.appendChild(textNode);
  } else {
    contentDom.appendChild(textNode);
  }
  const domRect = contentDom.getBoundingClientRect();
  const range = document.createRange();
  range.setStart(textNode,0);
  range.setEnd(textNode,0);
  const rect = range.getBoundingClientRect();
  pos.x = rect.left - domRect.left;
  pos.y = rect.top - domRect.top - 4;
  textNode.remove();
};
onMounted(updateCursor);
onUpdated(updateCursor);
</script>

<template>
  <div class="chat-content-container">
    <div class="markdown-body" v-html="markdownContent" ref="contentRef"></div>
    <div v-show="showCursor" class="cursor"></div>
  </div>
</template>

<style>
/* 新增样式 */
.thinking-container {
  overflow: hidden;
  transition: 0.5s ease;
}

.thinking-detail {
  padding: 12px 10px;
  box-sizing: border-box; /* 确保padding计入高度 */
}

.fold-button,.fold-button:hover {
  background: transparent;
  border: none;
  color: rgba(0,0,0,0.8);
}
.fold-button:hover {
  color: rgba(0,0,0,0.5);
}
.arrow-down-icon {
  transition: transform 0.3s ease;
}

/* markdown内容 */
.markdown-body {
  background: inherit;
  line-height: 2;
  font-family: 'Roboto Mono',serif;
  color: #000; /* 调亮正常文本颜色 */
  font-weight: bold;
}

/* 调整思考内容中的代码块 */
.think-content pre {
  background: rgba(0, 0, 0, 0.25) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 父级容器 */
.chat-content-container {
  position: relative;
}

/* 光标 */
.cursor {
  content: '';
  position: absolute;
  width: 3px;
  height: 20px;
  background: #0d0f1a;
  animation: toggle 0.8s infinite;
  opacity: 0;
  transform:translateY(3px);
  left: calc(v-bind('pos.x') * 1px);
  top: calc(v-bind('pos.y') * 1px);
}
@keyframes toggle {
  30% {
    opacity: 1;
  }
}
</style>