import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path:'/', redirect:'/navigator/home' },
    { path:'/manager', component: () => import('../views/test/Manager.vue'),children:[
        { path: 'home', name: 'home1', meta:{ title:'主页' }, component: () => import('../views/test/Home.vue'), },
        { path: 'test', name: 'test', meta:{ title:'测试数据页面' }, component: () => import('../views/test/Test.vue'), },
        { path: 'data', name: 'data', meta:{ title:'数据展示页面' }, component: () => import('../views/test/Data.vue'), },
    ]},
    { path: '/navigator', name: 'navigator',meta:{ title:'智绘山河' }, component: () => import('../views/Navigator.vue'),children:[
        { path: 'home', name: 'home', meta:{ title:'智绘山河' }, component: () => import('../views/Home.vue'), },
        { path: 'landform', name: 'landform', meta:{ title:'地形 | 智绘山河' }, component: () => import('../views/Landform.vue'), },
        { path: 'moonPhase', name: 'moonPhase', meta:{ title:'月相 | 智绘山河' }, component: () => import('../views/MoonPhase.vue'), },
        { path: 'climate', name: 'climate', meta:{ title:'气候 | 智绘山河' }, component: () => import('../views/Climate.vue'), },
        { path: 'humanity', name: 'humanity', meta:{ title:'人文 | 智绘山河' }, component: () => import('../views/Humanity.vue'), },
        { path: 'quizzes', name: 'quizzes', meta:{ title:'测试 | 智绘山河' }, component: () => import('../views/Quizzes.vue'), },

    ]},
    { path: '/register-login', name: 'register-login', meta:{ title:'登录 | 智绘山河' }, component: () => import('../views/Register-Login.vue'), },
    { path: '/404', name: '404',meta:{ title:'该页面不存在' }, component: () => import('../views/404.vue'),},
    { path:'/:pathMatch(.*)', redirect:'/404' }
  ],
})

// beforeEach表示跳转之前的一些操作
router.beforeEach((to,from,next) => {
    document.title = to.meta.title;
    next()  // 必须调用这个函数实现跳转
})

export default router
