# Agent-Analytics: 基于LLM-Agent的自适应数据分析与报告生成系统

## 项目简介

Agent-Analytics 是一个基于大语言模型（LLM）Agent 的自适应数据分析与报告生成系统，旨在通过智能代理技术实现自动化数据处理、分析与可视化报告输出。

该系统能够以可视化、0代码方式实现数据清洗、统计建模、机器学习、数据可视化等多种用途，并利用 LLM 进行报告产出、自然语言交互、提供建议。

## 系统总体架构（逻辑分层）

可以分为 **五层架构**：

### 1. 前端展示层（Vue3 + ECharts）

* 功能：

  * 数据上传（csv文件）
  * 模块选择与参数可视化设置（如聚类数、回归变量选择等）
  * LLM 聊天式交互界面（支持自然语言分析请求）
  * 可视化结果展示（ECharts图表、分析报告、模型评估结果）
* 扩展建议：

  * 支持"分析历史记录"模块（方便复现与审计）
  * 支持"报告导出"（PDF/Markdown）

---

### 2. 后端服务层（FastAPI）

* 功能：

  * 提供统一的 RESTful 接口
  * 管理文件上传、任务调度、API调用、模型管理
  * 向前端提供异步任务状态（如分析中 / 已完成）
* 扩展建议：

  * 增加一个 **任务队列（Celery / Redis）** 用于异步分析任务执行，避免阻塞。
  * 提供 **WebSocket** 实时输出模型训练日志与分析进度。

---

### 3. 智能代理层（LangChain Agent核心）

* 功能：

  * 解析自然语言指令（例如"帮我做一个多元线性回归"）
  * 调用后端注册的各种分析工具（Tool/API）
  * 对分析结果进行总结、报告生成
  * 自适应推荐分析路径（基于上下文自动选择统计/机器学习方法）
* 关键组件建议：

  * **ToolKit体系**：

    * `DataCleaningTool`（数据缺失值、异常值处理）
    * `StatModelTool`（t检验、ANOVA、回归等）
    * `MLModelTool`（分类、聚类、回归等）
    * `NLPTool`（情感分析、关键词提取等）
    * `VisualizationTool`（自动生成图表）
  * **Memory模块**：保存对话历史、变量名、上一步操作结果。
  * **Agent Executor**：负责协调多步分析操作。

---

### 4. 模型与计算层（Pandas + PyTorch + Scikit-learn + 预训练模型）

* 功能：

  * 封装传统统计方法与机器学习方法为独立API模块。
  * 每个API模块可独立调用（供LLM工具或用户直接使用）。
* 示例模块建议：

  * `pandas_api/`

    * `cleaning.py`：缺失值处理、数据转换
    * `stats.py`：描述统计、方差分析、卡方检验
  * `ml_api/`

    * `regression.py`：线性/逻辑回归
    * `classification.py`：随机森林、SVM、神经网络
  * `nlp_api/`

    * `sentiment.py`、`wordcloud.py`（支持中文）
* 扩展建议：

  * 增加一个 **AutoML模块**，让Agent在不确定时自动搜索最佳模型/参数组合。

---

### 5. 报告生成与解释层（LLM + 模板引擎）

* 功能：

  * 将分析结果（如表格、指标、图表）输入LLM进行解读
  * 输出自然语言报告
* 扩展建议：

  * 使用 **Jinja2 模板引擎** 或 **Markdown模板** 自动渲染报告
  * LLM可生成分章节报告结构，如：

    ```
    一、数据概览  
    二、建模与分析过程  
    三、结果与可视化  
    四、结论与建议
    ```

## 数据流通逻辑

1. 用户上传CSV文件
2. 后端保存至`/data/`目录，并注册为一个数据会话对象
3. 用户输入自然语言  LLM解析意图
4. Agent通过调用相应Tool执行分析（使用Pandas/Torch）
5. Tool返回结果（DataFrame、模型评估、图表路径等）
6. Agent总结结果，生成文字报告
7. 前端展示图表与自然语言报告

## 系统目录结构建议

```bash
project/
├── backend/
│   ├── main.py                # FastAPI主程序
│   ├── routers/
│   │   ├── files.py           # 文件上传接口
│   │   ├── analysis.py        # 调用分析API接口
│   │   └── llm_agent.py       # LLM对话与Agent执行
│   ├── tools/
│   │   ├── pandas_api/
│   │   ├── ml_api/
│   │   ├── nlp_api/
│   │   └── visualization/
│   ├── models/
│   ├── reports/
│   └── utils/
├── frontend/
│   └── src/
│       ├── views/
│       │   ├── Chat.vue
│       │   ├── Upload.vue
│       │   └── Dashboard.vue
│       ├── components/
│       ├── api/
│       └── store/
├── data/                      # 数据存储目录
├── README.md
└── requirements.txt
```

## 安全与性能建议

* 对文件上传添加格式检测与最大文件大小限制；
* 对LLM调用结果进行内容过滤与异常处理；
* 对多用户使用情况添加session隔离；
* 训练型模型任务使用异步执行避免阻塞接口；
* 对大数据集分析支持分块处理。

## 快速开始

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python main.py
```

## 开发路线图

- [x] 基础文件上传功能
- [x] 重构项目结构
- [ ] 集成 LangChain 构建 LLM-Agent
- [ ] 实现基础数据分析 API
- [ ] 添加数据可视化功能
- [ ] 实现自然语言交互
- [ ] 自动生成分析报告