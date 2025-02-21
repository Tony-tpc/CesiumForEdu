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
  return DOMPurify.sanitize(marked.parse(props.content));
});

// 响应式变量
const pos = reactive({ x: 0, y: 0 });
const contentRef = ref(null);

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

<style scoped>
/* markdown内容 */
.markdown-body {
  background: inherit;
  line-height: 2;
  font-family: 'Roboto Mono',serif;
  color: #0d0f1a;
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