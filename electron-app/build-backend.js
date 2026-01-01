const { exec } = require('child_process');
const path = require('path');
const fs = require('fs-extra');

async function buildBackend() {
  console.log('开始打包后端服务...');
  
  // 检查是否安装了PyInstaller
  try {
    const checkPyInstaller = exec('pyinstaller --version');
    await new Promise((resolve, reject) => {
      checkPyInstaller.on('close', (code) => {
        if (code === 0) {
          console.log('PyInstaller已安装');
          resolve();
        } else {
          console.error('未找到PyInstaller，请先安装: pip install pyinstaller');
          process.exit(1);
        }
      });
    });
  } catch (error) {
    console.error('未找到PyInstaller，请先安装: pip install pyinstaller');
    process.exit(1);
  }
  
  // 检查DASHSCOPE_API_KEY环境变量
  if (!process.env.DASHSCOPE_API_KEY) {
    console.warn('警告: DASHSCOPE_API_KEY环境变量未设置，AI功能可能无法正常工作');
  }
  
  // 确定后端目录
  const backendDir = path.join(__dirname, '..', 'backend');
  const distDir = path.join(__dirname, 'backend-server');
  
  // 创建输出目录
  if (!fs.existsSync(distDir)) {
    fs.ensureDirSync(distDir);
  }
  
  // 构建后端命令 - 改为多文件形式
  const pyInstallerCmd = `pyinstaller --onedir --name backend-server main.py ` +
    `-p . --collect-all fastapi --collect-all uvicorn --collect-all pydantic ` +
    `--collect-all jieba --collect-all dashscope --collect-all pandas --collect-all numpy ` +
    `--collect-all sklearn --collect-all scipy --collect-all statsmodels`;
  
  console.log('执行PyInstaller命令...');
  const buildProcess = exec(pyInstallerCmd, {
    cwd: backendDir,
    env: {
      ...process.env, // 传递所有当前环境变量，包括DASHSCOPE_API_KEY
      PYTHONPATH: backendDir
    }
  });
  
  buildProcess.stdout.on('data', (data) => {
    console.log(`PyInstaller stdout: ${data}`);
  });
  
  buildProcess.stderr.on('data', (data) => {
    console.error(`PyInstaller stderr: ${data}`);
  });
  
  buildProcess.on('close', async (code) => {
    if (code === 0) {
      console.log('后端打包成功');
      
      // 确定可执行文件路径
      const backendDist = path.join(backendDir, 'dist');
      const exeName = process.platform === 'win32' ? 'backend-server.exe' : 'backend-server';
      const backendExe = path.join(backendDist, exeName);
      
      // 复制到electron-app目录
      if (fs.existsSync(backendExe)) {
        const targetPath = path.join(distDir, exeName);
        fs.copyFileSync(backendExe, targetPath);
        console.log(`后端可执行文件已复制到: ${targetPath}`);
        
        console.log('后端服务打包完成！');
      } else {
        console.error('未找到生成的可执行文件');
        process.exit(1);
      }
    } else {
      console.error(`PyInstaller打包失败，退出码: ${code}`);
      process.exit(1);
    }
  });
}

buildBackend().catch(err => {
  console.error('打包过程中出现错误:', err);
  process.exit(1);
});