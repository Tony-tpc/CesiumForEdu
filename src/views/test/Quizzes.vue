<script setup>
import { ref } from 'vue';

const text = ref('');
const audioUrl = ref('');
const loading = ref(false);

function generateSpeech() {
  if (!text.value) {
    alert('请输入文本内容');
    return;
  }
  loading.value = true;
  audioUrl.value = '';

  // 创建 WebSocket 连接
  const ws = new WebSocket('ws://127.0.0.1:8080');

  ws.onopen = () => {
    ws.send(text.value);  // 发送文本
  };

  ws.onmessage = (event) => {
    // 将二进制音频数据转换为 Blob URL
    const audioBlob = new Blob([event.data], { type: 'audio/wav' });
    audioUrl.value = URL.createObjectURL(audioBlob);
    loading.value = false;
    ws.close();  // 关闭连接
  };

  ws.onerror = (error) => {
    console.error('WebSocket 错误:', error);
    alert('生成失败，请检查服务是否正常运行');
    loading.value = false;
  };
}
</script>

<template>
  <div class="tts-container">
    <h2>CosyVoice 测试</h2>
    <textarea v-model="text" placeholder="请输入文本"></textarea>
    <button @click="generateSpeech" :disabled="loading">生成语音</button>

    <audio v-if="audioUrl" :src="audioUrl" controls></audio>
    <p v-if="loading">音频生成中，请稍等...</p>
  </div>
</template>


<style scoped>
.tts-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

textarea {
  width: 400px;
  height: 100px;
  padding: 10px;
}

button {
  padding: 10px 20px;
  background: #0d534b;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
}
</style>
