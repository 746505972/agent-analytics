# Agent Analytics - Electron应用

这是一个将Agent Analytics数据分析系统打包为桌面应用的Electron项目。

## 项目结构

- `main.js`: Electron主进程文件
- `preload.js`: 预加载脚本，用于安全地将API暴露给渲染进程
- `package.json`: Electron应用的配置文件
- `build-frontend.js`: 构建前端并复制到Electron应用的脚本
- `build-backend.js`: 使用PyInstaller打包后端服务的脚本
- `build-script.js`: 完整的构建脚本
- `install-deps.js`: 自动安装所有依赖的脚本

## 开发环境要求

- Node.js (v14或更高版本)
- Python 3.x (用于后端服务)
- PyInstaller (用于打包后端)
- npm 或 yarn

## 环境变量配置

此应用需要以下环境变量：

- `DASHSCOPE_API_KEY`: 用于访问阿里云千问模型的API密钥

### Windows设置环境变量
```cmd
set DASHSCOPE_API_KEY=your_api_key_here
```

### PowerShell设置环境变量
```powershell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

### 永久设置环境变量
在系统环境变量中添加 `DASHSCOPE_API_KEY` 变量，值为您的API密钥。

## 快速开始（推荐）

运行以下命令自动安装所有依赖：

```bash
node install-deps.js
```

## 手动安装依赖

```bash
# 在electron-app目录中安装依赖
cd electron-app
npm install

# 安装PyInstaller用于打包后端
pip install pyinstaller
```

另外还需要安装前端和后端依赖：

```bash
# 安装前端依赖
cd ../frontend
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

## 运行开发模式

要运行开发模式，您需要同时启动后端和前端：

1. 设置环境变量：
```bash
# Windows CMD
set DASHSCOPE_API_KEY=your_api_key_here

# 或 PowerShell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

2. 启动后端服务：
```bash
cd ../backend
python main.py
```

3. 在另一个终端中启动前端开发服务器：
```bash
cd ../frontend
npm run dev
```

4. 在另一个终端中运行Electron应用：
```bash
cd ../electron-app
npm start
```

## 创建完全独立的桌面应用

为了创建完全独立的桌面应用（用户无需安装Python），请按以下步骤操作：

### 方法一：使用自动化脚本（推荐）
```bash
# 1. 设置环境变量
# Windows CMD
set DASHSCOPE_API_KEY=your_api_key_here

# 或 PowerShell
$env:DASHSCOPE_API_KEY="your_api_key_here"

# 2. 安装PyInstaller
pip install pyinstaller

# 3. 打包后端服务
cd electron-app
npm run build-backend

# 4. 构建完整应用
npm run build-all
```

### 方法二：手动打包
1. 安装PyInstaller：
```bash
pip install pyinstaller
```

2. 在backend目录中打包Python后端：
```bash
cd ../backend
pyinstaller --onefile --name backend-server main.py -p . --collect-all fastapi --collect-all uvicorn --collect-all pydantic --collect-all jieba --collect-all dashscope --collect-all pandas --collect-all numpy
```

3. 将生成的可执行文件复制到electron-app目录：
```bash
# Windows
mkdir -p ../electron-app/backend-server
cp dist/backend-server.exe ../electron-app/backend-server/

# macOS/Linux
mkdir -p ../electron-app/backend-server
cp dist/backend-server ../electron-app/backend-server/
```

4. 现在可以构建完整的Electron应用：
```bash
cd ../electron-app
npm run dist
```

## 中文路径问题解决

如果在中文路径下运行遇到字符编码问题，请尝试以下方法：

1. 将项目移动到纯英文路径（推荐）
2. 或者使用以下命令运行：
```bash
npm start
```

目前应用已在中文路径下测试成功，主要问题在于终端显示字符，不影响实际运行。

## 构建生产版本（简单方式）

如果不需要完全独立的打包（用户需安装Python），可以直接运行：

```bash
npm run dist
```

这将：
1. 自动构建前端项目
2. 将构建产物复制到Electron应用目录
3. 使用electron-builder打包应用

构建的安装包将位于 `dist` 目录中。

## 打包说明

- Windows: NSIS安装程序
- macOS: DMG磁盘映像
- Linux: AppImage

## 注意事项

1. 确保您的系统已安装Python 3.x，并且`python`命令可用
2. 在构建应用前，确保后端依赖已安装：
```bash
pip install -r ../requirements.txt
```
3. 如果需要自定义图标，请将`icon.png`放置在electron-app目录中
4. 在生产环境中，Electron应用会自动启动后端服务
5. 如果可能，建议将项目放在纯英文路径下以避免字符编码问题
6. 确保设置了`DASHSCOPE_API_KEY`环境变量以使用AI功能

## 故障排除

如果遇到问题，请检查：

1. 后端服务是否正常运行（默认端口8000）
2. 前端构建是否成功
3. 系统环境变量是否正确配置
4. 尝试将项目移动到纯英文路径
5. 确认`DASHSCOPE_API_KEY`环境变量已正确设置