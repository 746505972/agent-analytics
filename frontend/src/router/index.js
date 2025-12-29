import { createRouter, createWebHistory } from 'vue-router'
import Upload from '@/views/Upload.vue'
import Dashboard from '@/views/Dashboard.vue'
import Preview from '@/views/Preview.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/upload',
    name: 'Upload',
    component: Upload
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/preview',
    name: 'Preview',
    component: Preview
  },
]

const router = createRouter({
  history: createWebHistory('./'),  // 修改为相对路径
  routes
})

// 添加路由守卫来处理返回dashboard时的状态恢复
router.beforeEach((to, from, next) => {
  // 当从Analysis页面返回Dashboard页面时，不清除状态
  if (from.name === 'Analysis' && to.name === 'Dashboard') {
    // 可以在这里添加特殊的处理逻辑
  }
  next();
});

export default router