const { contextBridge, ipcRenderer } = require('electron');

// 安全地将API暴露给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  getBackendUrl: () => ipcRenderer.invoke('get-backend-url')
});