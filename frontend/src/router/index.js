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
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('@/views/Dashboard.vue') // 占位符，后续替换为实际分析页面
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router