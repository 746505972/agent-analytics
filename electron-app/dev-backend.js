const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const http = require('http');

let backendProcess;

// 创建日志函数
function logMessage(message) {
  const logPath = path.join(__dirname, 'backend-dev-log.txt');
  const timestamp = new Date().toISOString();
  const fullMessage = `[${timestamp}] ${message}\n`;
  fs.appendFileSync(logPath, fullMessage);
}

// 启动后端服务器
function startBackend() {
  return new Promise((resolve, reject) => {
    console.log('开始启动后端服务...');
    logMessage('开始启动后端服务...');

    const backendDir = path.join(__dirname, '..', 'backend');
    
    // 使用Python直接运行，而不是打包后的可执行文件
    backendProcess = spawn('python', ['main.py'], {
      cwd: backendDir,
      stdio: 'pipe',
      env: {
        ...process.env,
        DASHSCOPE_API_KEY: process.env.DASHSCOPE_API_KEY || '',
        PYTHONIOENCODING: 'utf-8',
        LANG: 'zh_CN.UTF-8'
      }
    });

    backendProcess.stdout.on('data', (data) => {
      const output = data.toString();
      console.log(`Backend stdout: ${output}`);
      logMessage(`Backend stdout: ${output}`);
      
      // 检查是否后端服务已完全启动
      if (output.includes('Uvicorn running on')) {
        console.log('后端服务已启动，等待完全就绪...');
        logMessage('后端服务已启动，等待完全就绪...');
      }
    });

    backendProcess.stderr.on('data', (data) => {
      console.error(`Backend stderr: ${data}`);
      logMessage(`Backend stderr: ${data}`);
    });

    backendProcess.on('close', (code) => {
      console.log(`Backend process exited with code ${code}`);
      logMessage(`后端进程退出，退出码: ${code}`);
    });
    
    backendProcess.on('error', (err) => {
      console.error(`Backend process error: ${err}`);
      logMessage(`后端进程错误: ${err}`);
      reject(err);
    });
    
    console.log('后端服务启动命令已发出');
    resolve();
  });
}

// 检查后端服务是否完全启动
function waitForBackend() {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    const timeout = 30000; // 30秒超时
    
    console.log('等待后端服务完全启动...');
    
    // 定期检查后端是否启动
    const checkInterval = setInterval(() => {
      const request = http.request({
        hostname: '127.0.0.1',
        port: 8000,
        path: '/',
        method: 'GET',
        timeout: 5000
      }, (res) => {
        console.log(`后端服务响应状态: ${res.statusCode}`);
        if (res.statusCode === 200) {
          clearInterval(checkInterval);
          console.log('后端服务已完全启动并响应请求');
          logMessage('后端服务已完全启动并响应请求');
          resolve(true);
        }
      });
      
      request.on('error', (e) => {
        // 如果连接失败，继续等待
        console.log('尝试连接后端服务失败，继续等待...');
      });
      
      request.on('timeout', () => {
        request.destroy();
        console.log('连接后端服务超时，继续等待...');
      });
      
      request.end();
      
      // 检查是否超时
      if (Date.now() - startTime > timeout) {
        clearInterval(checkInterval);
        console.error('等待后端启动超时');
        logMessage('等待后端启动超时');
        reject(new Error('后端服务启动超时'));
      }
    }, 1000); // 每秒检查一次
  });
}

async function startDevBackend() {
  try {
    await startBackend();
    await waitForBackend();
    console.log('后端服务已完全启动！');
  } catch (error) {
    console.error('启动后端服务失败:', error);
    process.exit(1);
  }
}

startDevBackend();

// 处理进程退出
process.on('SIGINT', () => {
  console.log('接收到退出信号');
  if (backendProcess) {
    backendProcess.kill();
  }
  process.exit();
});