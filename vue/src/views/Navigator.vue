<template>
<!--  导航栏开始-->
  <el-container>
    <el-header style="padding: 0">
      <div>
        <el-affix :offset="0">
          <div style="padding: 10px 200px;
                      text-align: right;
                      align-items: center;
                      justify-content: space-between;
                      background-color: transparent;
          ">
            <el-button link :icon="User">
              <span class="user-fonts" @click="router.push('/register-login')">注册</span>
            </el-button>
            <el-button link>
              <span class="user-fonts" @click="router.push('/register-login')">登录</span>
            </el-button>
          </div>
          <div style="padding-left: 200px">
            <el-menu
                class="menu-no-border"
                mode="horizontal"
                :ellipsis="false"
                @select="handleSelect"
                :default-active="router.currentRoute.value.path"
                router
                unique-opened
                :default-openeds="['/navigator']"
                style="background-color: transparent"
            >
              <div>
                <el-link href="/navigator/home"
                         :underline="false"
                >
                  <img
                      style="width: 120px"
                      src="@/assets/logo(AI-Generated).png"
                      alt="智绘山河logo"
                  />
                </el-link>
              </div>
              <div class="menu-items">
                <el-menu-item index="/navigator/landform"
                              :class="{ 'active-item-1': data.activeIndex === '/navigator/landform' }"
                >
                  <span class="menu-fonts">地形</span>
                </el-menu-item>
                <el-menu-item index="/navigator/moonPhase"
                              :class="{ 'active-item-2': data.activeIndex === '/navigator/moonPhase' }"
                >
                  <span class="menu-fonts">月相</span>
                </el-menu-item>
                <el-menu-item index="/navigator/climate"
                              :class="{ 'active-item-3': data.activeIndex === '/navigator/climate' }"
                >
                  <span class="menu-fonts">气候</span>
                </el-menu-item>
                <el-menu-item index="/navigator/humanity"
                              :class="{ 'active-item-4': data.activeIndex === '/navigator/humanity' }"
                >
                  <span class="menu-fonts">人文</span>
                </el-menu-item>
                <el-menu-item index="/navigator/quizzes"
                              :class="{ 'active-item-5': data.activeIndex === '/navigator/quizzes' }"
                >
                  <span class="menu-fonts">测试</span>
                </el-menu-item>
                <el-button text style="align-items: center;height: 55px">
                  <el-icon size="30px"><Search /></el-icon>
                </el-button>
              </div>
            </el-menu>
          </div>
        </el-affix>
      </div>
    </el-header>
  <!--  导航栏结束-->
  <!--  主体区域-->
    <el-main style="margin-top:30px">

      <div style="padding: 15px">
        <RouterView />
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { reactive } from "vue"
import { User } from "@element-plus/icons-vue";
import router from "@/router/index.js";

const data = reactive({
  activeIndex: router.currentRoute.value.path,

})

const handleSelect = (index) => {
  data.activeIndex = index
}

const savedIndex = localStorage.getItem('activeIndex')
if (savedIndex) {
  data.activeIndex = savedIndex
}

</script>

<style scoped>
.menu-no-border {
  border-bottom: none !important; /* 去掉菜单项之间的分界线 */
  display: flex;
  justify-content: space-between; /* 左右分开 */
  align-items: center; /* 垂直居中对齐 */
}

/*由菜单项选中颜色和菜单项文本颜色组成*/
.active-item-1 {
  background-color: #0066bc !important;
  color: white !important;
}

.active-item-2 {
  background-color: #46b61f !important;
  color: white !important;
}

.active-item-3 {
  background-color: #ffad00 !important;
  color: #015399 !important;
}

.active-item-4 {
  background-color: #e52f2f !important;
  color: white !important;
}

.active-item-5 {
  background-color: #5e41b8 !important;
  color: white !important;
}

.menu-items {
  display: flex; /* 让菜单项也使用 Flexbox */
  margin-right: 150px;
}

.menu-fonts {
  font-size: 18px;
  font-weight: bold;
}

.user-fonts {
  font-size: 14px;
}

</style>