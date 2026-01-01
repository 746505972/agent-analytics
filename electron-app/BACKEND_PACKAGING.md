# 后端封装说明

## 概述

本项目提供了两种后端封装方式：

1. **单文件EXE封装** (`build-backend.js`)：将整个后端打包为单个可执行文件
2. **多文件目录封装** (`build-backend-dir.js`)：将后端打包为包含所有依赖的目录

从版本 v1.1 开始，推荐使用多文件目录封装方式，因为它具有以下优势：

- **更快的启动速度**：无需解压整个应用到临时目录
- **更好的调试支持**：可以更容易地查看运行时错误
- **更可靠的监控**：能够监控后端是否完全启动

## 构建脚本

### build-backend.js
- 使用 PyInstaller 的 `--onefile` 选项
- 生成单个可执行文件
- 启动较慢，因为需要解压到临时目录

### build-backend-dir.js (推荐)
- 使用 PyInstaller 的 `--onedir` 选项
- 生成包含所有依赖的目录
- 启动更快，监控更可靠

## 启动监控机制

Electron 应用现在包含后端启动监控功能：

1. **进程启动监控**：监控后端进程是否成功启动
2. **服务就绪监控**：通过 HTTP 请求检查后端服务是否完全就绪
3. **超时处理**：30秒超时，防止无限等待

## 使用方法

### 构建后端（多文件形式）
```bash
cd electron-app
npm run build-backend-dir
```

### 构建完整应用（多文件后端）
```bash
cd electron-app
npm run build-all-dir
```

### 开发模式下监控后端启动
```bash
cd electron-app
node dev-backend.js
```

## 配置说明

### main.js 中的监控功能
- `startBackend()`: 启动后端进程
- `waitForBackend()`: 等待后端服务完全就绪
- 日志记录到系统临时目录的 `agent-analytics-log.txt`

### 构建配置
- 所有必需的子目录（data, reports, routers, utils, agents, tools）都会被包含
- 环境变量（如 DASHSCOPE_API_KEY）会被正确传递给后端进程

## 故障排除

### 后端启动失败
1. 检查 `agent-analytics-log.txt` 日志文件
2. 确认 DASHSCOPE_API_KEY 环境变量已设置
3. 确认端口 8000 未被占用

### 监控超时
1. 检查后端是否正确输出 "Uvicorn running on" 消息
2. 确认防火墙未阻止本地连接
3. 验证后端进程是否正常运行

## 性能对比

| 方式 | 启动时间 | 磁盘占用 | 监控可靠性 |
|------|----------|----------|------------|
| 单文件EXE | 较慢 | 较小 | 一般 |
| 多文件目录 | 较快 | 稍大 | 很好 |