<div align="center">

# Agent-Analytics: 基于LLM-Agent的数据分析与报告生成系统

![Python](https://img.shields.io/badge/Python3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

<img src="frontend/src/assets/images/logo.png" alt="Logo" width="200" align="center">
</div>

[English](README_en.md)

## 项目简介

Agent-Analytics 是一个基于大语言模型（LLM）Agent 的自适应数据分析与报告生成系统，旨在通过智能代理技术实现自动化数据处理、分析与可视化报告输出。

该系统能够以可视化、0代码方式实现数据清洗、统计建模、机器学习、数据可视化等多种用途，并利用 LLM 进行报告产出、自然语言交互、提些建议。

## 应用展示

[👉示例展示](example.md)

### Agent对话

![img.png](images/img.png)

### 工具调用

![img_1.png](images/img_1.png)

### 工具链调用

![img_3.png](images/img_3.png)

### 分析渲染

![img_2.png](images/img_2.png)

### 可视化

![img_5.png](images/img_5.png)

### 文本分析

![img_4.png](images/img_4.png)

## 系统架构图

![系统架构图.drawio.png](images/%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84%E5%9B%BE.drawio.png)
![工程实现图.drawio.png](images/%E5%B7%A5%E7%A8%8B%E5%AE%9E%E7%8E%B0%E5%9B%BE.drawio.png)

## 系统目录结构

```bash
project/
├── backend/
│   ├── main.py              # FastAPI主程序
│   ├── agents/              # Agent实现
│   │   ├── tools/           # Agent工具API
│   │   └── reports/         # 报告生成
│   ├── routers/             # 路由定义
│   │   ├── analysis.py      # 分析相关接口
│   │   ├── charts.py        # 图表相关接口
│   │   ├── chat.py          # 聊天相关接口
│   │   ├── data.py          # 数据处理接口
│   │   ├── files.py         # 文件管理接口
│   │   └── nlp.py           # NLP相关接口
│   └── utils/               # 工具函数
│       ├── file_manager.py  # 文件管理工具
│       ├── ml_tool/         # 机器学习工具包
│       ├── nlp_tool/        # NLP工具包
│       └── pandas_tool/     # Pandas工具包
├── frontend/
│   └── src/
│       ├── views/
│       │   ├── Dashboard.vue # 主界面
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

### 现已推出ELectron本地测试版

<https://github.com/746505972/agent-analytics/releases/latest>

---

### 后端启动

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 设置环境变量（使用通义千问）：

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
npm run server
```

3. 访问 <http://localhost:5173> 查看应用

## Languages

Total : 153 files,  31024 codes, 3156 comments, 3982 blanks, all 38162 lines

| language   | files |   code | comment | blank |  total |
|:-----------|------:|-------:|--------:|------:|-------:|
| vue        |    76 | 23,202 |     257 | 2,459 | 25,918 |
| Python     |    42 |  6,121 |   2,693 | 1,283 | 10,097 |
| JavaScript |    16 |  1,154 |     197 |   124 |  1,475 |
