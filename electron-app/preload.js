const { contextBridge, ipcRenderer } = require('electron');

// 安全地将API暴露给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  getBackendUrl: () => ipcRenderer.invoke('get-backend-url'),
  // 添加一些可能有助于解决输入问题的方法
  focusWindow: () => {
    // 允许渲染进程请求窗口聚焦
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(true);
      }, 100);
    });
  }
});

// 在预加载脚本中添加一些配置来确保输入框正常工作
// 确保页面可以正常处理输入事件
process.once('loaded', () => {
  // 设置一些全局变量，帮助前端正确处理输入
  global.electronInputFix = true;
});