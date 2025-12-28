// apiConfig.js - API配置文件
let backendBaseUrl = 'http://localhost:8000'; // 默认后端地址

// 检查是否在Electron环境中运行
if (window && window.electronAPI) {
  // 在Electron环境中，使用API获取后端URL
  if (window.electronAPI.getBackendUrl) {
    window.electronAPI.getBackendUrl().then(url => {
      backendBaseUrl = url;
    }).catch(err => {
      console.warn('无法从Electron获取后端URL，使用默认URL:', err);
    });
  }
}

export { backendBaseUrl };