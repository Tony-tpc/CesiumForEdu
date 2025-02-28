<template>
  <div
      class="day-night-switch-container"
      :style="style"
      :class="className"
      ref="container"
  >
    <div class="components"
         @click="toggleTheme"
         @mouseout="handleComponentsMouseOut"
         @mousemove="handleComponentsMouseMove"
    >
      <div class="main-button"></div>
      <div class="moon"></div>
      <div class="moon"></div>
      <div class="moon"></div>
      <div class="daytime-background"></div>
      <div class="daytime-background"></div>
      <div class="daytime-background"></div>
      <div class="cloud">
        <div
            v-for="i in 12"
            :key="i"
            class="cloud-son"
        ></div>
      </div>
      <div class="cloud-light"></div>
      <div class="stars">
        <div
            v-for="(star, index) in stars"
            :key="index"
            class="star"
            :class="star.size"
        >
          <div class="star-son"></div>
          <div class="star-son"></div>
          <div class="star-son"></div>
          <div class="star-son"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  modelValue: Boolean,
  style: Object,
  className: String
});

const emit = defineEmits(['update:modelValue']);

const isClicked = ref(false);
const isDark = ref(false);

// DOM 引用
const container = ref(null);
const mainButton = ref(null);
const daytimeBackground = ref([]);
const cloud = ref(null);
const cloudList = ref([]);
const cloudLight = ref(null);
const components = ref(null);
const moon = ref([]);
const starsConfig = [
  { size: 'big' },
  { size: 'medium' },
  { size: 'small' },
  { size: 'medium' },
  { size: 'small' },
  { size: 'medium' }
];
const star = ref([]);
const stars = ref(starsConfig); // 直接使用配置数据

onMounted(() => {
  isDark.value = props.modelValue;
  mainButton.value = container.value.querySelector('.main-button');
  daytimeBackground.value = container.value.querySelectorAll('.daytime-background');
  cloud.value = container.value.querySelector('.cloud');
  cloudList.value = container.value.querySelectorAll('.cloud-son');
  cloudLight.value = container.value.querySelector('.cloud-light');
  components.value = container.value.querySelector('.components');
  moon.value = container.value.querySelectorAll('.moon');
  stars.value = container.value.querySelector('.stars');
  star.value = container.value.querySelectorAll('.star');

  handleComponentsClick(props.modelValue ? 'light' : 'dark');
});

// 修改 watch 逻辑
watch(() => props.modelValue, (newVal) => {
  isDark.value = newVal; // 同步外部状态
  handleComponentsClick(newVal ? 'light' : 'dark');
});

// 修正切换逻辑
const toggleTheme = () => {
  const newTheme = !props.modelValue;
  isDark.value = newTheme; // 更新内部状态
  emit('update:modelValue', newTheme); // 触发外部更新
};

const handleComponentsClick = (targetTheme) => {
  if (targetTheme === 'light') {
    applyLightTheme();
    emit('update:modelValue', true);
  } else {
    applyDarkTheme();
    emit('update:modelValue', false);
  }

  isClicked.value = true;
  setTimeout(() => isClicked.value = false, 500);
};

const applyLightTheme = () => {
  mainButton.value.style.transform = "translateX(0)";
  mainButton.value.style.backgroundColor = "rgba(255, 195, 35,1)";
  mainButton.value.style.boxShadow =
      "3px 3px 5px rgba(0, 0, 0, 0.5), inset  -3px -5px 3px -3px rgba(0, 0, 0, 0.5), inset  4px 5px 2px -2px rgba(255, 230, 80,1)";

  daytimeBackground.value[0].style.transform = "translateX(0)";
  daytimeBackground.value[1].style.transform = "translateX(0)";
  daytimeBackground.value[2].style.transform = "translateX(0)";

  cloud.value.style.transform = "translateY(10px)";
  cloudLight.value.style.transform = "translateY(10px)";
  components.value.style.backgroundColor = "rgba(70, 133, 192,1)";

  moon.value.forEach(m => m.style.opacity = "0");
  stars.value.style.transform = "translateY(-125px)";
  stars.value.style.opacity = "0";
};

const applyDarkTheme = () => {
  mainButton.value.style.transform = "translateX(110px)";
  mainButton.value.style.backgroundColor = "rgba(195, 200,210,1)";
  mainButton.value.style.boxShadow =
      "3px 3px 5px rgba(0, 0, 0, 0.5), inset  -3px -5px 3px -3px rgba(0, 0, 0, 0.5), inset  4px 5px 2px -2px rgba(255, 255, 210,1)";

  daytimeBackground.value[0].style.transform = "translateX(110px)";
  daytimeBackground.value[1].style.transform = "translateX(80px)";
  daytimeBackground.value[2].style.transform = "translateX(50px)";

  cloud.value.style.transform = "translateY(80px)";
  cloudLight.value.style.transform = "translateY(80px)";
  components.value.style.backgroundColor = "rgba(25,30,50,1)";

  moon.value.forEach(m => m.style.opacity = "1");
  stars.value.style.transform = "translateY(-62.5px)";
  stars.value.style.opacity = "1";
};

const handleComponentsMouseOut = () => {
  if (isClicked.value) return;

  const starPositions = isDark.value ? [
    { top: "11px", left: "39px" },
    { top: "39px", left: "91px" },
    { top: "26px", left: "19px" },
    { top: "37px", left: "66px" },
    { top: "21px", left: "75px" },
    { top: "51px", left: "38px" }
  ] : [
    { top: "10px", left: "35px" },
    { top: "30px", left: "85px" },
    { top: "20px", left: "15px" },
    { top: "33px", left: "60px" },
    { top: "18px", left: "70px" },
    { top: "50px", left: "30px" }
  ];

  star.value.forEach((s, i) => {
    s.style.top = starPositions[i].top;
    s.style.left = starPositions[i].left;
  });

  if (!isDark.value) {
    mainButton.value.style.transform = "translateX(110px)";
    daytimeBackground.value[0].style.transform = "translateX(110px)";
    daytimeBackground.value[1].style.transform = "translateX(80px)";
    daytimeBackground.value[2].style.transform = "translateX(50px)";
  } else {
    mainButton.value.style.transform = "translateX(0)";
    daytimeBackground.value[0].style.transform = "translateX(0)";
    daytimeBackground.value[1].style.transform = "translateX(0)";
    daytimeBackground.value[2].style.transform = "translateX(0)";
  }

    // 设置云朵位置
    const cloudPositions = [
      { right: "-20px", bottom: "10px" },
      { right: "-10px", bottom: "-25px" },
      { right: "20px", bottom: "-40px" },
      { right: "50px", bottom: "-35px" },
      { right: "75px", bottom: "-60px" },
      { right: "110px", bottom: "-50px" },
      { right: "-20px", bottom: "10px" },
      { right: "-10px", bottom: "-25px" },
      { right: "20px", bottom: "-40px" },
      { right: "50px", bottom: "-35px" },
      { right: "75px", bottom: "-60px" },
      { right: "110px", bottom: "-50px" }
    ];
    cloudList.value.forEach((c, i) => {
      c.style.right = cloudPositions[i].right;
      c.style.bottom = cloudPositions[i].bottom;
    });
};

const handleComponentsMouseMove = () => {
  if (isClicked.value) return;

  const starPositions = isDark.value ? [
    { top: "10px", left: "36px" },
    { top: "40px", left: "87px" },
    { top: "25px", left: "16px" },
    { top: "35px", left: "63px" },
    { top: "18px", left: "72px" },
    { top: "50px", left: "35px" }
  ] : [
    { top: "12px", left: "40px" },
    { top: "42px", left: "90px" },
    { top: "28px", left: "18px" },
    { top: "40px", left: "65px" },
    { top: "22px", left: "75px" },
    { top: "55px", left: "40px" }
  ];

  star.value.forEach((s, i) => {
    s.style.top = starPositions[i].top;
    s.style.left = starPositions[i].left;
  });

  if (!isDark.value) {
    mainButton.value.style.transform = "translateX(100px)";
    daytimeBackground.value[0].style.transform = "translateX(100px)";
    daytimeBackground.value[1].style.transform = "translateX(73px)";
    daytimeBackground.value[2].style.transform = "translateX(46px)";
  } else {
    mainButton.value.style.transform = "translateX(10px)";
    daytimeBackground.value[0].style.transform = "translateX(10px)";
    daytimeBackground.value[1].style.transform = "translateX(7px)";
    daytimeBackground.value[2].style.transform = "translateX(4px)";
  }

    // 微调云朵位置
    cloudList.value.forEach((c, i) => {
      const randomX = Math.random() * 10 - 5;
      const randomY = Math.random() * 10 - 5;
      c.style.transform = `translate(${randomX}px, ${randomY}px)`;
    });
};
</script>


<style scoped>
.day-night-switch-container {
  width: 180px;
  height: 70px;
}

.day-night-switch-container .components {
  position: fixed;
  width: 180px;
  height: 70px;
  background-color: rgba(70, 133, 192, 1);
  border-radius: 100px;
  box-shadow: inset 0 0 5px 3px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  transition: 0.7s;
  transition-timing-function: cubic-bezier(0, 0.5, 1, 1);
  cursor: pointer;
}


.day-night-switch-container .components .main-button {
  margin: 7.5px 0 0 7.5px;
  width: 55px;
  height: 55px;
  background-color: rgba(255, 195, 35, 1);
  border-radius: 50%;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5), inset -3px -5px 3px -3px rgba(0, 0, 0, 0.5), inset 4px 5px 2px -2px rgba(255, 230, 80, 1);
  transition: 1.0s;
  transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00);
}
.day-night-switch-container .components .moon {
  position: absolute;
  background-color: rgba(150, 160, 180, 1);
  box-shadow: inset 0 0 1px 1px rgba(0, 0, 0, 0.3);
  border-radius: 50% ;
  transition: 0.5s;
  opacity: 0;
}
.day-night-switch-container .components .moon:nth-child(1) {
  top: 7.5px;
  left: 25px;
  width: 12.5px;
  height: 12.5px;
}
.day-night-switch-container .components .moon:nth-child(2) {
  top: 20px;
  left: 7.5px;
  width: 20px;
  height: 20px;
}
.day-night-switch-container .components .moon:nth-child(3) {
  top: 32.5px;
  left: 32.5px;
  width: 12.5px;
  height: 12.5px;
}
.day-night-switch-container .components .daytime-background {
  position: absolute;
  border-radius: 50%;
  transition: 1.0s;
  transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00);
}
.day-night-switch-container .components .daytime-background:nth-child(4) {
  top: -20px;
  left: -20px;
  width: 110px;
  height:110px;
  background-color: rgba(255, 255, 255,0.2);
  z-index: -2;
}
.day-night-switch-container .components .daytime-background:nth-child(5) {
  top: -32.5px;
  left: -17.5px;
  width: 135px;
  height:135px;
  background-color: rgba(255, 255, 255,0.1);
  z-index: -3;
}
.day-night-switch-container .components .daytime-background:nth-child(6) {
  top: -45px;
  left: -15px;
  width: 160px;
  height:160px;
  background-color: rgba(255, 255, 255,0.05);
  z-index: -4;
}
.day-night-switch-container .components  .cloud,.cloud-light {
  transform: translateY(10px);
  transition: 1.0s;
  transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00);
}

.day-night-switch-container .components .cloud-son {
  position: absolute;
  background-color: #fff;
  border-radius: 50%;
  z-index: -1;
  transition: transform 0.3s ease; /* 添加平滑过渡 */
}

.day-night-switch-container .components .cloud-son:nth-child(6n+1){
  right: -20px;
  bottom: 10px;
  width: 50px;
  height: 50px;
}
.day-night-switch-container .components .cloud-son:nth-child(6n+2) {
  right: -10px;
  bottom: -25px;
  width: 60px;
  height: 60px;
}
.day-night-switch-container .components .cloud-son:nth-child(6n+3) {
  right: 20px;
  bottom: -40px;
  width: 60px;
  height: 60px;
}
.day-night-switch-container .components .cloud-son:nth-child(6n+4) {
  right: 50px;
  bottom: -35px;
  width: 60px;
  height: 60px;
}
.day-night-switch-container .components .cloud-son:nth-child(6n+5) {
  right: 75px;
  bottom: -60px;
  width: 75px;
  height: 75px;
}
.day-night-switch-container .components .cloud-son:nth-child(6n+6) {
  right: 110px;
  bottom: -50px;
  width: 60px;
  height: 60px;
}
.day-night-switch-container .components .cloud{
  z-index: -2;
}
.day-night-switch-container .components .cloud-light{
  position: absolute;
  right: 0;
  bottom: 25px;
  opacity: 0.5;
  z-index: -3; /*transform: rotate(-5deg);*/
}
.day-night-switch-container .components .stars{
  transform: translateY(-125px);
  z-index: 1 !important;
  transition: 1.0s;
  transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00);
}

.day-night-switch-container .components .big { --size: 7.5px; }
.day-night-switch-container .components .medium { --size: 5px; }
.day-night-switch-container .components .small { --size: 3px; }
.day-night-switch-container .components .star {
  position: absolute;
  width: calc(2*var(--size));
  height: calc(2*var(--size));
}
.day-night-switch-container .components .star:nth-child(1){
  top: 11px;
  left: 39px;
  animation-name: dayNightStart;
  animation-duration: 3.5s;
}
.day-night-switch-container .components .star:nth-child(2){
  top: 39px;
  left: 91px;
  animation-name: dayNightStart;
  animation-duration: 4.1s;
}
.day-night-switch-container .components .star:nth-child(3){
  top: 26px;
  left: 19px;
  animation-name: dayNightStart;
  animation-duration: 4.9s;
}
.day-night-switch-container .components .star:nth-child(4){
  top: 37px;
  left: 66px;
  animation-name: dayNightStart;
  animation-duration: 5.3s;
}
.day-night-switch-container .components .star:nth-child(5){
  top: 21px;
  left: 75px;
  animation-name: dayNightStart;
  animation-duration: 3s;
}
.day-night-switch-container .components .star:nth-child(6){
  top: 51px;
  left: 38px;
  animation-name: dayNightStart;
  animation-duration: 2.2s;
}
@keyframes dayNightStart {
  0%,20%{transform: scale(0);}
  20%,100% {transform: scale(1);}
}
.day-night-switch-container .components  .star-son{
  float: left;
}
.day-night-switch-container .components  .star-son:nth-child(1) { --pos: left 0; }
.day-night-switch-container .components  .star-son:nth-child(2) { --pos: right 0; }
.day-night-switch-container .components  .star-son:nth-child(3) { --pos: 0 bottom; }
.day-night-switch-container .components  .star-son:nth-child(4) { --pos: right bottom; }
.day-night-switch-container .components  .star-son { width: var(--size); height: var(--size); background-image:radial-gradient(circle var(--size) at var(--pos), transparent var(--size), #fff); }
.day-night-switch-container .components  .star{ transform: scale(1); transition-timing-function: cubic-bezier(0.56, 1.35, 0.52, 1.00); transition: 1s; animation-iteration-count:infinite; animation-direction: alternate; animation-timing-function: linear; }
.day-night-switch-container .components  .twinkle { transform: scale(0); }
</style>