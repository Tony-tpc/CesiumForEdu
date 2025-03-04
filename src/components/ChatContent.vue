<script setup>
import 'github-markdown-css/github-markdown-dark.css';
import { marked } from 'marked'
import DOMPurify from "dompurify";
import { computed, ref, reactive, onMounted, onUpdated, watch, onUnmounted } from "vue";
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
  },
  isFolded: {
    type: Boolean,
    default: false,
  },
  index: {
    type: Number,
    required: true
  }
});

// 新增响应式状态
const startTime = ref(null)
const endTime = ref(null) // 新增结束时间戳
const displayDuration = ref(0)
const timer = ref(null)

const isExpanded = ref(!props.isFolded);
const isThinking = ref(false);
const handleFoldButton = (identifier) => {
  isExpanded.value = !isExpanded.value;
  // 设置展示
  const thinkingDetail = document.querySelector(identifier);

  if (isExpanded.value) {
    thinkingDetail.style.height = 'auto';
    const { height } = thinkingDetail.getBoundingClientRect();
    thinkingDetail.style.height = '0';
    thinkingDetail.getBoundingClientRect();
    thinkingDetail.style.padding = '12px 10px';
    if (isThinking.value) {
      thinkingDetail.style.height = 'auto';
    } else {
      thinkingDetail.style.height = (height + 24) + 'px';
    }
  } else {
    thinkingDetail.getBoundingClientRect();
    thinkingDetail.style.height = '0';
    thinkingDetail.style.padding = '0 10px';
  }
}

// 设置代码属性
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  }
});

marked.setOptions({
  gfm: true,        // 启用GitHub风格
  tables: true,     // 明确启用表格
  breaks: true      // 将换行符转为<br>
});

// 内容解析计算属性
const parsedContent = computed(() => {
  const result = {
    hasThinking: false,
    thinking: '',
    main: props.content
  }
  if (!props.content.includes('<think>')) return result

  try {
    const cleaned = props.content.replace('<think>', '')
    const splitIndex = cleaned.indexOf('</think>')
    console.log(`cleaned = ${cleaned},splitIndex = ${splitIndex}`)

    if (splitIndex === -1) {
      isThinking.value = true
      result.hasThinking = true
      result.thinking = cleaned
      result.main = ''
    } else {
      isThinking.value = false
      result.hasThinking = true
      result.thinking = cleaned.slice(0, splitIndex)
      result.main = cleaned.slice(splitIndex + ''.length)
    }
  } catch (e) {
    console.error('解析错误:', e)
  }
  console.log(result.thinking)
  return result
})

// 处理markdown格式文本
const processedContent = computed(() => ({
  thinking: DOMPurify.sanitize(marked.parse(parsedContent.value.thinking)),
  main: DOMPurify.sanitize(marked.parse(parsedContent.value.main))
}))

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
  const thinkDom = document.getElementById(`thinking${props.index}`);
  if (thinkDom && parsedContent.value.main) {
    pos.y = rect.top - domRect.top + thinkDom.getBoundingClientRect().height + 62;
  } else if (thinkDom) {
    pos.y = rect.top - domRect.top + 45;
  } else {
    pos.y = rect.top - domRect.top - 4;
    pos.x = rect.left - domRect.left + 82;
  }
  textNode.remove();
};
onMounted(updateCursor);
onUpdated(updateCursor);

// 修改后的监听逻辑
watch(() => props.content, (newVal) => {
  if (!newVal) return

  // 检测结束标记
  if (newVal.includes('</think>')) {
    handleContentEnd()
    return
  }

  // 仅在未结束时检测起始
  if (!endTime.value) {
    const isValidStart = /[^\s]/.test(newVal) || newVal.includes('<think>')

    if (!startTime.value && isValidStart) {
      startTimer()
    }
  }
})

// 启动计时逻辑拆分
const startTimer = () => {
  startTime.value = performance.now()
  endTime.value = null // 重置结束时间
  timer.value = setInterval(() => {
    // 优先使用结束时间计算
    const end = endTime.value || performance.now()
    displayDuration.value = end - startTime.value
  }, 100)
}

// 处理结束标记
const handleContentEnd = () => {
  if (!endTime.value) {
    endTime.value = performance.now()
    clearInterval(timer.value)
    timer.value = null
  }
}

// 格式化显示使用最终时间
const formatDuration = (ms) => {
  if (endTime.value) { // 结束时锁定显示
    const finalMs = endTime.value - startTime.value
    return finalMs < 1000 ?
        `${Math.round(finalMs)}ms` :
        `${(finalMs/1000).toFixed(1)}s`
  }
  return ms < 1000 ?
      `${Math.round(ms)}ms` :
      `${(ms/1000).toFixed(1)}s`
}

// 清理定时器
onUnmounted(() => {
  clearInterval(timer.value)
  timer.value = null
})
</script>

<template>
  <div class="chat-content-container">
    <div class="markdown-body">
      <div v-if="!parsedContent.hasThinking && !props.content">
        正在加载中
      </div>
      <template v-if="parsedContent.hasThinking">
        <div class="thinking-container">
          <el-button type="primary" class="fold-button" @click="handleFoldButton(`#thinking${props.index}`)">
            <span style="font-size: 16px">{{ isExpanded ? '收起思考过程' : '展开思考过程' }}</span>
            <span v-if="displayDuration > 0" class="time-badge">
              （{{ formatDuration(displayDuration) }}）
            </span>
            <el-icon :class="['arrow-down-icon', { rotated: isExpanded }]">
              <ArrowDown/>
            </el-icon>
          </el-button>
          <div class="thinking-container">
            <div :class="['thinking-detail','think']" :id="`thinking${props.index}`" ref="contentRef">
              <div v-html="processedContent.thinking"></div>
            </div>
          </div>
          <div v-if="parsedContent.main"
               v-html="processedContent.main"
               ref="contentRef"></div>
        </div>
      </template>
      <div v-else v-html="processedContent.main" ref="contentRef"></div>
      <div v-show="showCursor" class="cursor"></div>
    </div>
  </div>
</template>

<style>
/* 新增时间标记样式 */
.time-badge {
  margin-left: 8px;
  font-size: 0.85em;
  color: #666;
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  transition: opacity 0.2s;
}

/* 修改边距 */
.markdown-body p {
  margin-bottom: 0;
}
.think p {
  margin-bottom: 1em;
}

/* 修改表格背景色 */
.markdown-body table th, .markdown-body table td {
  background-color: antiquewhite;
}

/* 保证关闭时不显示任何内容 */
.thinking-container {
  overflow: hidden;
  transition: 0.5s ease;
}

/* 思考内容 */
.thinking-detail {
  padding: 12px 10px;
  box-sizing: border-box; /* 确保padding计入高度 */
  transition: all 0.5s ease;
}

/* 自定义think标签 */
.think {
  display: block;
  margin: 16px 0;
  padding: 12px 10px;
  background: rgba(138, 99, 210, 0.1);
  border-left: 4px solid #8a63d2;
  color: #6c4298;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  width: inherit;
  left: inherit;
}

.think::before {
  content: "💡 思考中...";
  font-weight: bold;
  color: #8a63d2;
  display: block;
  font-style: italic;
}

.think.active {
  height: auto;
  padding: 12px 10px;
  opacity: 1;
}

/* 折叠按钮 */
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
  margin-left: 8px;
}

.arrow-down-icon.rotated {
  transform: rotate(180deg);
}

/* markdown内容 */
.markdown-body {
  background: inherit;
  line-height: 2;
  font-family: 'Roboto Mono',serif;
  color: #000; /* 调亮正常文本颜色 */
  margin-bottom: 0;
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