<template>
  <div style="position:absolute;top: 0; left: 43%;width: 52%;height: 100%">
    <div>
      <el-button type="primary" class="fold-button" @click="handleFoldButton">点击展开&nbsp;&nbsp;
        <el-icon class="arrow-down-icon"><ArrowDown /></el-icon>
      </el-button>
    </div>
    <think class="thinking-detail">这里是think标签</think>
  </div>
</template>

<script setup>
import {ref} from "vue";

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
</script>

<style scoped>
/* 自定义 think 标签样式 */


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
</style>