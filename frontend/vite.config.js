import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    host: "0.0.0.0",
    allowedHosts: ["all","20b44786cfa0.ngrok-free.app"],
    proxy: {
      '/upload': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/user': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/chat': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/data': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})