const { buildFrontend } = require('./build-frontend.js');
const { exec } = require('child_process');
const path = require('path');

async function buildApp() {
  try {
    console.log('开始构建Electron应用...');
    
    // 首先构建前端
    await buildFrontend();
    
    // 然后构建Electron应用
    console.log('开始打包Electron应用...');
    const electronBuild = exec('npm run dist', {
      cwd: __dirname
    });

    electronBuild.stdout.on('data', (data) => {
      console.log(`Electron build stdout: ${data}`);
    });

    electronBuild.stderr.on('data', (data) => {
      console.error(`Electron build stderr: ${data}`);
    });

    electronBuild.on('close', (code) => {
      if (code === 0) {
        console.log('Electron应用构建成功！');
      } else {
        console.error(`Electron应用构建失败，退出码: ${code}`);
        process.exit(code);
      }
    });
  } catch (error) {
    console.error('构建过程中出现错误:', error);
    process.exit(1);
  }
}

buildApp();