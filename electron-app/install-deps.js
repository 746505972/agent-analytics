const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('正在安装Electron应用依赖...');

try {
  // 安装Electron应用的依赖
  execSync('npm install', { stdio: 'inherit', cwd: __dirname });
  console.log('✓ Electron应用依赖安装完成');

  // 检查并安装前端依赖
  const frontendPath = path.join(__dirname, '..', 'frontend');
  if (fs.existsSync(path.join(frontendPath, 'package.json'))) {
    console.log('正在安装前端依赖...');
    execSync('npm install', { stdio: 'inherit', cwd: frontendPath });
    console.log('✓ 前端依赖安装完成');
  }

  // 检查并安装后端依赖
  const backendPath = path.join(__dirname, '..', 'backend');
  if (fs.existsSync(path.join(backendPath, 'requirements.txt'))) {
    console.log('正在安装后端依赖...');
    execSync('pip install -r requirements.txt', { stdio: 'inherit', cwd: backendPath });
    console.log('✓ 后端依赖安装完成');
  }

  console.log('\n所有依赖安装完成！');
  console.log('要启动开发模式，请按以下顺序执行：');
  console.log('1. cd ../backend && python main.py');
  console.log('2. cd ../frontend && npm run dev');
  console.log('3. cd ../electron-app && npm start');
  console.log('\n要构建生产版本，请执行：');
  console.log('cd ../electron-app && npm run dist');
} catch (error) {
  console.error('安装依赖时出错:', error.message);
  process.exit(1);
}