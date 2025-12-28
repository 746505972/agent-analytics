const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');

// 使用动态导入处理ES模块
let isDev;
async function initializeIsDev() {
  const isDevModule = await import('electron-is-dev');
  isDev = isDevModule.default;
}

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: fs.existsSync(path.join(__dirname, 'icon.png')) ? path.join(__dirname, 'icon.png') : null
  });

  // 在开发环境中使用Vite服务器，生产环境中使用构建后的文件
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173'); // Vite默认开发端口
  } else {
    mainWindow.loadFile(path.join(__dirname, 'frontend', 'dist', 'index.html'));
  }

  // 打开开发者工具（仅在开发环境中）
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
}

// 检查Python是否可用（开发环境）
function checkPython() {
  return new Promise((resolve, reject) => {
    exec('python --version', (error, stdout, stderr) => {
      if (error) {
        // 尝试使用 python3
        exec('python3 --version', (error2, stdout2, stderr2) => {
          if (error2) {
            console.error('未找到Python，请确保已安装Python并添加到系统PATH');
            reject('未找到Python');
          } else {
            console.log(`Python3版本: ${stdout2}`);
            resolve('python3');
          }
        });
      } else {
        console.log(`Python版本: ${stdout}`);
        resolve('python');
      }
    });
  });
}

// 获取后端可执行文件路径
function getBackendExecutablePath() {
  const resourcePath = isDev ? path.join(__dirname, '..', 'backend') : process.resourcesPath;
  const exeName = process.platform === 'win32' ? 'backend-server.exe' : 'backend-server';
  return path.join(resourcePath, 'backend-server', exeName);
}

// 启动后端服务器
async function startBackend() {
  try {
    // 准备环境变量，确保包含DASHSCOPE_API_KEY
    const env = {
      ...process.env,
      // 从系统环境变量中获取DASHSCOPE_API_KEY
      DASHSCOPE_API_KEY: process.env.DASHSCOPE_API_KEY || '',
      // 确保后端能正确处理中文路径
      PYTHONIOENCODING: 'utf-8',
      LANG: 'zh_CN.UTF-8'
    };

    if (isDev) {
      // 开发环境：使用Python直接运行
      const pythonCmd = await checkPython();
      const backendPath = path.join(__dirname, '..', 'backend');
      const mainPyPath = path.join(backendPath, 'main.py');
      
      // 检查后端文件是否存在
      if (!fs.existsSync(mainPyPath)) {
        console.error(`后端文件不存在: ${mainPyPath}`);
        return;
      }
      
      // 使用Python运行后端服务器
      backendProcess = spawn(pythonCmd, [mainPyPath], {
        cwd: backendPath,
        env: {
          ...env,
          PYTHONPATH: backendPath
        }
      });
    } else {
      // 生产环境：使用打包的可执行文件
      const backendExe = getBackendExecutablePath();
      
      if (!fs.existsSync(backendExe)) {
        console.error(`后端可执行文件不存在: ${backendExe}`);
        return;
      }
      
      backendProcess = spawn(backendExe, [], {
        env: env
      });
    }

    backendProcess.stdout.on('data', (data) => {
      console.log(`Backend stdout: ${data}`);
    });

    backendProcess.stderr.on('data', (data) => {
      console.error(`Backend stderr: ${data}`);
    });

    backendProcess.on('close', (code) => {
      console.log(`Backend process exited with code ${code}`);
      // 如果后端意外退出，可以选择重启
      // setTimeout(() => startBackend(), 2000);
    });
    
    backendProcess.on('error', (err) => {
      console.error(`Backend process error: ${err}`);
    });
  } catch (error) {
    console.error('启动后端服务失败:', error);
  }
}

// 当Electron完成初始化时
app.whenReady().then(async () => {
  await initializeIsDev(); // 初始化isDev变量
  await startBackend(); // 启动后端服务器
  createWindow(); // 创建浏览器窗口

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// 当所有窗口关闭时
app.on('window-all-closed', function () {
  // 终止后端进程
  if (backendProcess) {
    backendProcess.kill();
  }
  
  if (process.platform !== 'darwin') app.quit();
});

// IPC处理
ipcMain.handle('get-backend-url', () => {
  // 返回后端API的基础URL
  return isDev ? 'http://localhost:8000' : 'http://localhost:8000';
});