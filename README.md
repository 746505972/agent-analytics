# Agent-Analytics: 基于LLM-Agent的自适应数据分析与报告生成系统


![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![npm](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![ngrok](https://img.shields.io/badge/ngrok-1F1E37?style=for-the-badge&logo=ngrok&logoColor=white)

## 项目简介

Agent-Analytics 是一个基于大语言模型（LLM）Agent 的自适应数据分析与报告生成系统，旨在通过智能代理技术实现自动化数据处理、分析与可视化报告输出。

该系统能够以可视化、0代码方式实现数据清洗、统计建模、机器学习、数据可视化等多种用途，并利用 LLM 进行报告产出、自然语言交互、提些建议。

## 当前系统架构

### 1. 前端展示层（Vue3 + ECharts）

* 功能：

  * 数据上传界面（支持 CSV、XLS、XLSX 文件）
  * 数据预览和基本统计信息展示
  * LLM 聊天式交互界面（支持自然语言分析请求）
  * 分析结果可视化展示（图表、分析报告等）

### 2. 后端服务层（FastAPI）

* 功能：

  * 提供统一的 RESTful 接口
  * 管理文件上传、会话管理和API调用
  * 实现定期清理过期会话和文件的功能
  * 支持跨域请求，便于前后端分离开发

### 3. 智能代理层（LangChain Agent核心）

* 功能：

  * 解析自然语言指令（例如"帮我分析这份数据"）
  * 调用后端注册的各种分析工具（Tool/API）
  * 对分析结果进行总结、报告生成

### 4. 模型与计算层（Pandas + PyTorch + Scikit-learn）

* 功能：

  * 封装传统统计方法与机器学习方法为独立API模块。
  * 每个API模块可独立调用（供LLM工具或用户直接使用）。

### 5. 报告生成与解释层（LLM）

* 功能：

  * 将分析结果（如表格、指标、图表）输入LLM进行解读
  * 输出自然语言报告、PDF报告

## 实际系统目录结构

```bash
project/
├── backend/
│   ├── main.py              # FastAPI主程序
│   ├── agents/              # Agent实现
│   ├── routers/             # 路由定义
│   │   ├── chat.py          # 聊天相关接口
│   │   ├── data.py          # 数据处理接口
│   │   └── files.py         # 文件管理接口
│   ├── tools/               # 工具API
│   │   ├── ml_api/          # 机器学习API
│   │   ├── nlp_api/         # 自然语言处理API
│   │   ├── pandas_api/      # 数据处理API
│   │   └── visualization/   # 可视化API
│   ├── reports/             # 报告生成
│   └── utils/               # 工具函数
│       ├── cleanup.py       # 清理工具
│       └── file_manager.py  # 文件管理工具
├── frontend/
│   └── src/
│       ├── views/
│       │   ├── Analysis.vue # 分析界面
│       │   ├── Dashboard.vue# 主界面
│       │   ├── Preview.vue  # 预览界面
│       │   └── Upload.vue   # 上传界面
│       ├── router/          # 路由配置
│       └── main.js          # 入口文件
├── README.md
└── requirements.txt
```

## 数据流通逻辑

1. 用户上传数据文件（CSV/XLS/XLSX）
2. 后端保存至`data/`目录，并关联唯一session_id
3. 用户通过聊天界面输入自然语言指令
4. LLM解析意图并指导Agent调用相应Tool执行分析
5. Tool返回结果（DataFrame、模型评估、图表等）
6. Agent总结结果，生成文字报告
7. 前端展示图表与自然语言报告

## 安全与性能特性

* 支持多种数据格式上传（CSV、XLS、XLSX）
* 基于Session的会话管理，隔离不同用户数据
* 定期自动清理过期会话和文件，节省存储空间
* 异步文件处理，提高响应速度

## 快速开始

### 后端启动

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量（如果使用通义千问）：
```bash
export DASHSCOPE_API_KEY=你的API密钥
```

3. 运行后端服务：
```bash
python backend/main.py
```

### 前端启动

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 运行前端开发服务器：
```bash
npm run dev
```

3. 访问 http://localhost:5173 查看应用

## 开发路线图

- [x] 基础文件上传功能
- [ ] 实现基础数据分析 API
- [ ] 添加数据可视化功能
- [x] 实现自然语言交互
- [ ] 自动生成分析报告
- [ ] 集成更多机器学习算法
- [ ] 支持更多文件格式
- [ ] 增强报告模板功能
- [ ] 添加用户认证和权限管理