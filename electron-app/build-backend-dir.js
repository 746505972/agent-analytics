const { exec } = require('child_process');
const path = require('path');
const fs = require('fs-extra');

async function buildBackend() {
  console.log('开始以多文件形式打包后端服务...');

  // 检查是否安装了PyInstaller
  try {
    const { execSync } = require('child_process');
    execSync('pyinstaller --version', { stdio: 'pipe' });
    console.log('PyInstaller已安装');
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

  // 构建后端命令 - 使用--onedir（多文件）而不是--onefile
  const pyInstallerCmd = `pyinstaller backend-server.spec`;

  console.log('执行PyInstaller命令...');
  console.log('PyInstaller命令:', pyInstallerCmd);
  
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
      const exeName = process.platform === 'win32' ? 'backend-server' : 'backend-server'; // 对于onedir模式，Windows上也是backend-server目录
      const backendExeSource = path.join(backendDist, exeName);
      
      // 复制整个目录到electron-app目录
      if (fs.existsSync(backendExeSource)) {
        const targetPath = path.join(distDir);
        if (fs.existsSync(targetPath)) {
          // 删除旧的目录
          fs.removeSync(targetPath);
        }
        
        fs.copySync(backendExeSource, targetPath);
        console.log(`后端目录已复制到: ${targetPath}`);
        
        // 检查是否包含所有必需的子目录
        const requiredDirs = ['data', 'reports', 'routers', 'utils', 'agents', 'tools'];
        for (const dir of requiredDirs) {
          const dirPath = path.join(targetPath, dir);
          if (!fs.existsSync(dirPath)) {
            console.warn(`警告: 目录 ${dir} 未正确复制`);
          }
        }
        
        console.log('后端服务多文件打包完成！');
      } else {
        console.error('未找到生成的后端目录');
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