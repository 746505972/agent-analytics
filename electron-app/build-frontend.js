const { exec } = require('child_process');
const path = require('path');
const fs = require('fs-extra');

function buildFrontend() {
  return new Promise((resolve, reject) => {
    // 确保目标目录存在
    const distDir = path.join(__dirname, 'frontend', 'dist');
    if (!fs.existsSync(distDir)) {
      fs.ensureDirSync(distDir);
    }

    // 执行前端构建命令
    const buildProcess = exec('npm run build', {
      cwd: path.join(__dirname, '..', 'frontend')
    });

    buildProcess.stdout.on('data', (data) => {
      console.log(`Frontend build stdout: ${data}`);
    });

    buildProcess.stderr.on('data', (data) => {
      console.error(`Frontend build stderr: ${data}`);
    });

    buildProcess.on('close', (code) => {
      if (code === 0) {
        console.log('前端构建成功');
        // 将构建产物复制到Electron应用目录
        const sourceDir = path.join(__dirname, '..', 'frontend', 'dist');
        const targetDir = path.join(__dirname, 'frontend', 'dist');
        
        fs.copy(sourceDir, targetDir, (err) => {
          if (err) {
            console.error('复制前端构建产物失败:', err);
            reject(err);
          } else {
            console.log('前端构建产物已复制到Electron应用目录');
            resolve();
          }
        });
      } else {
        console.error(`前端构建失败，退出码: ${code}`);
        reject(new Error(`前端构建失败，退出码: ${code}`));
      }
    });
  });
}

module.exports = { buildFrontend };