<template>
  <div>
    <div style="margin-bottom: 20px">
      <el-button type="primary" @click="router.back()">返回主页</el-button>
    </div>
    <div style="font-size: 20px;font-weight: bold;color: red;text-decoration: underline;font-style: italic;margin-bottom: 20px;">
      欢迎
    </div>

    <div style="font-size: 30px">
      <!--      此处尝试Vue3基础语法 -->
      {{ a }} {{ b }}
    </div>

    <div style="margin-bottom: 20px">
      {{ data.a }}
      {{ data.b }}
    </div>

    <div style = "margin-bottom: 20px">
      <input v-model = "data.a" />
    </div>

    <div style="margin-bottom: 20px">
      <span style="color: red" v-if = "data.name === '凤雏'">卧龙凤雏</span>
      <span style="color: aqua" v-if = "data.name === '元直'">水镜元直</span>
      <span style="color: pink" v-else>abcd</span>
    </div>

    <div style="display: flex">
      <div style="width: 300px;height: 300px;text-align: center;
      line-height: 300px;font-size: 30px;margin: 10px;
      background-color: green" v-for="item in data.arr">{{ item }}</div>
    </div>

    <div>
      <select style="width: 200px">
        <option v-for="item in data.arr">{{ item }}</option>
      </select>
    </div>

    <div style="margin-bottom: 20px">
      <button @click="click()">点我！</button>
    </div>

    <div style="margin-bottom: 20px">
      <div :style="data.box"></div>
      <div>
        <img :src="data.img">
      </div>
    </div>

    <div style="margin: 30px">
      <el-button @click="clickData" color="#41b883" :style="{ 'color':'red' }" :loading="data.loading">启动</el-button>
      <el-button type="primary">Primary</el-button>
      <el-button type="success">Success</el-button>
      <el-button type="info">Info</el-button>
      <el-button type="warning">Warning</el-button>
      <el-button type="danger">Danger</el-button>
    </div>

    <div style="margin: 30px">
      <el-icon :size="20">
        <Edit />
      </el-icon>
      <span style="margin: 30px">
      <el-icon :size="15" style="top: 2px">
        <View />
      </el-icon>100
      </span>
      <el-input
          v-model="data.a"
          style="width: 240px"
          placeholder="Type something"
          :prefix-icon="Search"
      />
    </div>

    <div>
      <el-input v-model="data.input" style="width: 240px" placeholder="Please input" />
    </div>

  </div>
</template>

<script setup>
import {reactive, ref,onMounted} from "vue";
import {Search} from "@element-plus/icons-vue";
import router from "@/router/index.js";

const a = ref(1)
const b = ref("测试用字符串")
/* 推荐以下reactive渲染数据，一次性完成多个渲染 */
const data = reactive({
  id:router.currentRoute.value.query.id,
  name:router.currentRoute.value.query.name,
  a:123,
  b:"A String",
  // name: '元直3',
  loading:false,
  arr: ['苹果','香蕉','橘子'],
  box: {
    width: '100px',
    height: '100px',
    backgroundColor: 'red'
  },
  img :'https://www.runoob.com/wp-content/uploads/2017/01/vue.png',
  input:'',
})

console.log('获取到传递过来的id=' + data.id + ',name=' + data.name)

onMounted(() => {
  console.log('页面加载完成')
})
const click = () => {
  alert("好运+1")
}

const clickData = async () => {
  data.loading = true
  try {
    // 模拟一个异步操作，例如 API 请求
    await new Promise((resolve) => setTimeout(resolve, 2000));
  } catch (error) {
    console.error(error);
  } finally {
    data.loading = false; // 操作完成后将 loading 设置为 false
  }
}

</script>
