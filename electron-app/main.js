const { app, BrowserWindow, ipcMain, shell} = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const url = require('url');
const os = require('os');

let mainWindow;
let backendProcess;
let frontendServer;

// 创建日志函数
function logMessage(message) {
  const logPath = path.join(os.tmpdir(), 'agent-analytics-log.txt');
  const timestamp = new Date().toISOString();
  const fullMessage = `[${timestamp}] [PID:${process.pid}] ${message}\n`;
  fs.appendFileSync(logPath, fullMessage);
}

// 简单的HTTP服务器来服务前端文件，支持前端路由
function startFrontendServer() {
  return new Promise((resolve, reject) => {
    // console.log('开始启动前端服务器...');
    const distPath = path.join(__dirname, 'frontend', 'dist');
    // console.log(`前端资源路径: ${distPath}`);
    
    if (!fs.existsSync(distPath)) {
      // console.error(`前端资源目录不存在: ${distPath}`);
      reject(new Error(`前端资源目录不存在: ${distPath}`));
      return;
    }
    
    frontendServer = http.createServer((req, res) => {
      const filePath = path.join(distPath, req.url);
      
      // 检查请求路径是否包含文件扩展名，如果没有则返回index.html（支持前端路由）
      const extname = path.extname(filePath);
      let contentType = 'text/html';
      
      if (extname === '.js') contentType = 'text/javascript';
      else if (extname === '.css') contentType = 'text/css';
      else if (extname === '.json') contentType = 'application/json';
      else if (extname === '.png') contentType = 'image/png';
      else if (extname === '.jpg') contentType = 'image/jpg';
      else if (extname === '.gif') contentType = 'image/gif';
      else if (extname === '.svg') contentType = 'image/svg+xml';
      else if (extname === '.wav') contentType = 'audio/wav';
      else if (extname === '.mp4') contentType = 'video/mp4';
      else if (extname === '.woff') contentType = 'application/font-woff';
      else if (extname === '.ttf') contentType = 'application/font-ttf';
      else if (extname === '.eot') contentType = 'application/vnd.ms-fontobject';
      
      // 如果是API请求或包含文件扩展名的资源，则尝试从文件系统加载
      if (extname && fs.existsSync(filePath)) {
        fs.readFile(filePath, (err, content) => {
          if (err) {
            res.writeHead(500);
            res.end(`Error: ${err}`);
          } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
          }
        });
      } else {
        // 对于没有文件扩展名的请求（如前端路由），返回index.html
        const indexPath = path.join(distPath, 'index.html');
        fs.readFile(indexPath, (err, content) => {
          if (err) {
            res.writeHead(500);
            res.end(`Error loading index.html: ${err}`);
          } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content, 'utf-8');
          }
        });
      }
    });
    
    frontendServer.listen(3000, '127.0.0.1', () => {
      // console.log('前端文件服务器启动在 http://127.0.0.1:3000');
      resolve();
    });
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      // 启用 webSecurity 以确保安全，但确保不影响正常的输入功能
      webSecurity: true,
      // 启用实验性功能以支持现代Web特性
      enableRemoteModule: false,
      // 允许输入框和其他交互元素正常工作
      spellcheck: false // 关闭拼写检查以避免潜在的输入问题
    },
    icon: fs.existsSync(path.join(__dirname, 'icon.png')) ? path.join(__dirname, 'icon.png') : null
  });


  mainWindow.loadURL('http://127.0.0.1:3000'); // 使用内置前端服务器


  // 在生产环境中不打开开发者工具

  // 设置自定义菜单
  const { Menu } = require('electron');
  const template = [
    {
      label: '导航',
      submenu: [
        {
          label: '刷新',
          click: () => {
            mainWindow.webContents.reload();
          }
        },
        { type: 'separator' },
        {
          label: '开发者工具',
          click: () => mainWindow.webContents.openDevTools()
        }
      ]
    },
    {
      label: '帮助',
      submenu: [
        {
          label: '关于',
          click: () => {
            const { dialog, shell } = require('electron');
            const detailMessage = '内测版本 0.2.0\n数据分析系统桌面应用\n·后端启动的比较慢，大概半分钟，在完全启动前上传文件报错是很正常的，耐心等待即可。\n·后端使用Qwen-plus模型的LLM服务实现Agent功能，使用前请先配置环境变量DASHSCOPE_API_KEY\n获取环境变量请参考官网：';
            
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: '关于',
              message: 'Agent Analytics',
              detail: detailMessage,
              buttons: ['前往仓库', '打开链接', '关闭'],
              defaultId: 2
            }).then(result => {
              if (result.response === 0) { // 前往仓库
                shell.openExternal('https://github.com/746505972/agent-analytics');
              } else if (result.response === 1) { // 打开链接
                shell.openExternal('https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.253f7b08WPebcH&tab=api#/api/?type=model&url=2803795');
              }
            });
          }
        }
      ]
    }
  ];
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}



// 获取后端可执行文件路径
function getBackendExecutablePath() {
  // 在生产环境中，后端可执行文件应该在 resources/backend-server/ 目录中
  // 但有时安装后路径结构可能有所不同，我们需要尝试多个可能的位置
  const resourcePath = process.resourcesPath;
  const exeName = process.platform === 'win32' ? 'backend-server.exe' : 'backend-server';
  
  // console.log('开始查找后端可执行文件...');
  // logMessage('开始查找后端可执行文件...');
  
  // 尝试标准路径 - process.resourcesPath 指向 Electron 应用的 resources 目录
  // 对于多文件打包，可执行文件在 backend-server 目录下
  const standardPath = path.join(resourcePath, 'backend-server', exeName);
  // console.log(`标准后端路径: ${standardPath}`);
  // logMessage(`标准后端路径: ${standardPath}`);
  
  if (fs.existsSync(standardPath)) {
    // console.log('在标准路径找到后端可执行文件');
    // logMessage('在标准路径找到后端可执行文件');
    return standardPath;
  }
  
  // 检查资源目录下所有文件
  if (resourcePath && fs.existsSync(resourcePath)) {
    const resourceFiles = fs.readdirSync(resourcePath);
    // console.log('资源目录内容:', resourceFiles);
    // logMessage(`资源目录内容: ${resourceFiles.join(',')}`);
    
    // 查找包含 backend-server 的目录
    for (const file of resourceFiles) {
      if (file.toLowerCase().includes('backend') && fs.statSync(path.join(resourcePath, file)).isDirectory()) {
        const potentialPath = path.join(resourcePath, file, exeName);
        // console.log(`检查潜在路径: ${potentialPath}`);
        // logMessage(`检查潜在路径: ${potentialPath}`);
        
        if (fs.existsSync(potentialPath)) {
          // console.log(`在资源子目录找到后端可执行文件: ${file}`);
          // logMessage(`在资源子目录找到后端可执行文件: ${file}`);
          return potentialPath;
        }
      }
    }
  }
  
  // 尝试检查应用目录结构
  const appDir = path.dirname(app.getPath('exe'));
  // console.log(`应用目录: ${appDir}`);
  // logMessage(`应用目录: ${appDir}`);
  
  if (fs.existsSync(appDir)) {
    const appDirFiles = fs.readdirSync(appDir);
    // console.log('应用目录内容:', appDirFiles);
    // logMessage(`应用目录内容: ${appDirFiles.join(',')}`);
    
    // 检查是否有 resources 目录
    const resourcesPath = path.join(appDir, 'resources');
    if (fs.existsSync(resourcesPath)) {
      const resourcesFiles = fs.readdirSync(resourcesPath);
      // console.log('Resources目录内容:', resourcesFiles);
      // logMessage(`Resources目录内容: ${resourcesFiles.join(',')}`);
      
      for (const file of resourcesFiles) {
        if (file.toLowerCase().includes('backend') && fs.statSync(path.join(resourcesPath, file)).isDirectory()) {
          const potentialPath = path.join(resourcesPath, file, exeName);
          // console.log(`检查Resources子目录路径: ${potentialPath}`);
          // logMessage(`检查Resources子目录路径: ${potentialPath}`);
          
          if (fs.existsSync(potentialPath)) {
            // console.log(`在Resources子目录找到后端可执行文件: ${file}`);
            // logMessage(`在Resources子目录找到后端可执行文件: ${file}`);
            return potentialPath;
          }
        }
      }
    }
  }
  
  // 如果所有路径都不存在，返回标准路径供错误处理
  // console.log('未找到后端可执行文件，返回标准路径');
  // logMessage('未找到后端可执行文件，返回标准路径');
  return standardPath;
}

// 启动后端服务器
async function startBackend() {
  try {
    // console.log('开始启动后端服务...');
    
    // 准备环境变量，确保包含DASHSCOPE_API_KEY
    const env = {
      ...process.env,
      // 从系统环境变量中获取DASHSCOPE_API_KEY
      DASHSCOPE_API_KEY: process.env.DASHSCOPE_API_KEY || '',
      // 确保后端能正确处理中文路径
      PYTHONIOENCODING: 'utf-8',
      LANG: 'zh_CN.UTF-8'
    };

    // 生产环境：使用打包的可执行文件
    const backendExe = getBackendExecutablePath();
    // console.log(`尝试启动后端可执行文件: ${backendExe}`);
    // logMessage(`尝试启动后端可执行文件: ${backendExe}`);
    
    if (!fs.existsSync(backendExe)) {
      // console.error(`后端可执行文件不存在: ${backendExe}`);
      // logMessage(`错误：后端可执行文件不存在: ${backendExe}`);
      
      // 作为备选方案，尝试在当前目录的上级目录查找
      const fallbackPath = path.join(__dirname, '..', 'backend-server', 'backend-server.exe');
      // console.log(`尝试备选路径: ${fallbackPath}`);
      // logMessage(`尝试备选路径: ${fallbackPath}`);
      
      if (fs.existsSync(fallbackPath)) {
        // console.log('在备选路径找到后端可执行文件');
        // logMessage('在备选路径找到后端可执行文件');
        backendProcess = spawn(fallbackPath, [], {
          env: env,
          stdio: 'pipe',
          detached: false
        });
      } else {
        // console.error('所有后端可执行文件路径都不存在');
        // logMessage('所有后端可执行文件路径都不存在');
        return;
      }
    } else {
      backendProcess = spawn(backendExe, [], {
        env: env,
        stdio: 'pipe',  // 确保能够捕获输出
        detached: false  // 确保子进程不会分离
      });
    }
    
    // console.log('后端进程已创建，正在监听输出...');
    // logMessage('后端进程已创建，正在监听输出...');

    backendProcess.stdout.on('data', (data) => {
      const output = data.toString();
      // console.log(`Backend stdout: ${output}`);
      
      // 检查是否后端服务已完全启动
      if (output.includes('Uvicorn running on')) {
        // console.log('后端服务已成功启动');
        // logMessage('后端服务已成功启动');
      }
    });

    backendProcess.stderr.on('data', (data) => {
      // console.error(`Backend stderr: ${data}`);
      // logMessage(`Backend stderr: ${data}`);
    });

    backendProcess.on('close', (code) => {
      // console.log(`Backend process exited with code ${code}`);
      // logMessage(`后端进程退出，退出码: ${code}`);
      
      // 如果后端意外退出，可以选择重启
      // setTimeout(() => startBackend(), 2000);
    });
    
    backendProcess.on('error', (err) => {
      // console.error(`Backend process error: ${err}`);
      // logMessage(`后端进程错误: ${err}`);
    });
    
    // console.log('后端服务启动命令已发出');
  } catch (error) {
    // console.error('启动后端服务失败:', error);
    // logMessage(`启动后端服务失败: ${error}`);
  }
}

// 检查后端服务是否完全启动
// function waitForBackend() {
//   return new Promise((resolve, reject) => {
//     const startTime = Date.now();
//     const timeout = 30000; // 30秒超时
//
//     // 定期检查后端是否启动
//     const checkInterval = setInterval(() => {
//       // 尝试连接后端服务
//       const http = require('http');
//
//       const request = http.request({
//         hostname: '127.0.0.1',
//         port: 8000,
//         path: '/',
//         method: 'GET',
//         timeout: 5000
//       }, (res) => {
//         console.log(`后端服务响应状态: ${res.statusCode}`);
//         if (res.statusCode === 200) {
//           clearInterval(checkInterval);
//           console.log('后端服务已完全启动并响应请求');
//           logMessage('后端服务已完全启动并响应请求');
//           resolve(true);
//         }
//       });
//
//       request.on('error', (e) => {
//         // 如果连接失败，继续等待
//         console.log('尝试连接后端服务失败，继续等待...');
//       });
//
//       request.on('timeout', () => {
//         request.destroy();
//         console.log('连接后端服务超时，继续等待...');
//       });
//
//       request.end();
//
//       // 检查是否超时
//       if (Date.now() - startTime > timeout) {
//         clearInterval(checkInterval);
//         console.error('等待后端启动超时');
//         logMessage('等待后端启动超时');
//         reject(new Error('后端服务启动超时'));
//       }
//     }, 1000); // 每秒检查一次
//   });
// }

// 当Electron完成初始化时
app.whenReady().then(async () => {
  // logMessage('应用开始初始化');
  // console.log('应用开始初始化，当前工作目录:', process.cwd());
  // console.log('应用可执行文件路径:', app.getPath('exe'));
  // console.log('资源路径:', process.resourcesPath);
  // console.log('应用目录:', path.dirname(app.getPath('exe')));
  //
  // logMessage(`当前工作目录: ${process.cwd()}`);
  // logMessage(`应用可执行文件路径: ${app.getPath('exe')}`);
  // logMessage(`资源路径: ${process.resourcesPath}`);
  // logMessage(`应用目录: ${path.dirname(app.getPath('exe'))}`);
  

  
  await startBackend(); // 启动后端服务器

  await startFrontendServer(); // 启动前端服务器
  
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
  
  // 关闭前端服务器
  if (frontendServer) {
    frontendServer.close();
  }
  
  if (process.platform !== 'darwin') app.quit();
});

// IPC处理
ipcMain.handle('get-backend-url', () => {
  // 返回后端API的基础URL
  // 确保后端服务在正确的端口上运行
  return 'http://127.0.0.1:8000';
});