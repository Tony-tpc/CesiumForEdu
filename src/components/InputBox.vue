<script setup>
import { ref } from 'vue'
const props = defineProps({
  input: {
    type: String,
    default: '',
  },
  top: {
    type: Number,
    default: 0,
  },
  left: {
    type: Number,
    default: 0,
  }
})

let textInput = ref(props.input);
const handleCloseInputBox = () => {
  textInput.value = '';
}

</script>

<template>
  <div v-if="textInput" class="input-box-container">
    <span class="content">{{ textInput }}
      <el-button type="primary" @click="handleCloseInputBox" class="close-input-box">
        <el-icon  ><Close /></el-icon>
      </el-button>
    </span>
  </div>
</template>

<style scoped>
.input-box-container {
  display: inline-block;
  position: absolute;
  top: calc(v-bind('props.top') * 1px);
  left: calc(v-bind('props.left') * 1px);
  min-width: 20px;
  max-width: 80vw; /* 最大宽度限制 */
  margin-left: 10px;
}

.content {
  display: inline-block;
  font-size: 16px;
  line-height: 30px;
  padding: 0 10px;
  background-color: #5fc6ff;
  color: #0d0f1a;
  border-radius: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.close-input-box,.close-input-box:hover {
  background-color: transparent;
  border: none;
  padding: 0;
}
</style>