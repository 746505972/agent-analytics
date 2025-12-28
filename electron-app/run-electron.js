const { spawn } = require('child_process');
const path = require('path');

// 设置环境变量以处理中文路径
process.env.NODE_ENV = 'production';
process.env.ELECTRON_DISABLE_SECURITY_WARNINGS = 'true';

// 启动Electron应用
const electronPath = require('electron');
const appPath = path.join(__dirname, 'main.js');

const electronProcess = spawn(electronPath, [appPath], {
  env: {
    ...process.env,
    // 确保正确的字符编码
    LANG: 'zh-CN.UTF-8',
    LC_ALL: 'zh-CN.UTF-8'
  },
  stdio: 'inherit'
});

electronProcess.on('close', (code) => {
  console.log(`Electron应用退出，退出码: ${code}`);
  process.exit(code);
});