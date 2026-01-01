const { exec, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function runCommand(command, cwd) {
  return new Promise((resolve, reject) => {
    console.log(`执行命令: ${command}`);
    const child = exec(command, { cwd }, (error, stdout, stderr) => {
      if (error) {
        console.error(`执行失败: ${error}`);
        reject(error);
        return;
      }
      console.log(`命令执行成功: ${stdout}`);
      resolve(stdout);
    });

    // 实时输出命令的进度
    child.stdout.on('data', (data) => {
      console.log(data.toString());
    });

    child.stderr.on('data', (data) => {
      console.error(data.toString());
    });
  });
}

async function rebuildApp() {
  console.log('开始重新构建应用...');

  const backendPath = path.join(__dirname, '..', 'backend');
  const frontendPath = path.join(__dirname, '..', 'frontend');
  const electronPath = __dirname;

  try {
    // 构建后端（使用多文件形式）
    console.log('构建后端服务...');
    await runCommand('npm run build-backend-dir', electronPath);

    // 构建前端
    console.log('构建前端应用...');
    await runCommand('npm run build', frontendPath);

    console.log('应用构建完成！');
  } catch (error) {
    console.error('构建过程中出现错误:', error);
    process.exit(1);
  }
}

rebuildApp();

// 构建完整的Electron应用
async function buildFullApp() {
  console.log('开始构建完整的Electron应用...');
  
  try {
    // 首先构建后端
    console.log('构建后端服务...');
    await new Promise((resolve, reject) => {
      const backendBuild = exec('npm run build-backend', {
        cwd: path.join(__dirname)
      });

      backendBuild.stdout.on('data', (data) => {
        console.log(`Backend build: ${data}`);
      });

      backendBuild.stderr.on('data', (data) => {
        console.error(`Backend build error: ${data}`);
      });

      backendBuild.on('close', (code) => {
        if (code === 0) {
          console.log('后端构建成功');
          resolve();
        } else {
          reject(new Error(`后端构建失败，退出码: ${code}`));
        }
      });
    });

    // 然后构建前端
    console.log('构建前端...');
    await new Promise((resolve, reject) => {
      const frontendBuild = exec('npm run build-frontend', {
        cwd: path.join(__dirname)
      });

      frontendBuild.stdout.on('data', (data) => {
        console.log(`Frontend build: ${data}`);
      });

      frontendBuild.stderr.on('data', (data) => {
        console.error(`Frontend build error: ${data}`);
      });

      frontendBuild.on('close', (code) => {
        if (code === 0) {
          console.log('前端构建成功');
          resolve();
        } else {
          reject(new Error(`前端构建失败，退出码: ${code}`));
        }
      });
    });

    // 最后构建Electron安装包
    console.log('构建Electron安装包...');
    await new Promise((resolve, reject) => {
      const electronBuild = exec('electron-builder', {
        cwd: path.join(__dirname)
      });
      
      electronBuild.stdout.on('data', (data) => {
        console.log(`Electron build: ${data}`);
      });
      
      electronBuild.stderr.on('data', (data) => {
        console.error(`Electron build error: ${data}`);
      });
      
      electronBuild.on('close', (code) => {
        if (code === 0) {
          console.log('Electron应用构建成功');
          resolve();
        } else {
          reject(new Error(`Electron构建失败，退出码: ${code}`));
        }
      });
    });
    
    console.log('所有构建步骤完成！');
  } catch (error) {
    console.error('构建过程中出现错误:', error);
    process.exit(1);
  }
}

// 运行构建
buildFullApp();