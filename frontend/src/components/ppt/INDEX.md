# 🎨 PPT 统一样式系统 - 文档导航

欢迎使用 PPT 统一样式系统！本指南将帮助你快速找到所需文档。

## 📚 文档目录

### 🚀 新手入门（按顺序阅读）

#### 1. [安装与配置指南](INSTALLATION.md) ⭐⭐⭐
**适合人群**: 首次使用者  
**内容**:
- ✅ 环境要求和依赖检查
- 🔧 Vite 配置说明
- 🚀 快速开始步骤
- 🐛 常见问题解决
- 📱 浏览器兼容性测试

**阅读时间**: 10 分钟

---

#### 2. [样式快速参考](QUICK_REFERENCE.md) ⭐⭐⭐⭐⭐
**适合人群**: 日常开发者  
**内容**:
- 📋 基础模板（复制即用）
- 🎯 常用类名速查表
- 🔧 Mixins 快速参考
- 🎨 常见场景模板
- 💡 使用技巧（DO/DON'T）

**阅读时间**: 5 分钟  
**使用频率**: 每天多次

---

#### 3. [完整使用指南](README_STYLES.md) ⭐⭐⭐⭐
**适合人群**: 深度学习者  
**内容**:
- 🎨 核心设计理念
- 🛠️ 三种使用方法详解
- 📦 所有组件类的完整说明
- 🌈 颜色和变量系统
- 📝 最佳实践建议
- 🔍 调试技巧

**阅读时间**: 30 分钟  
**推荐**: 至少通读一遍

---

#### 4. [项目总结文档](STYLE_SYSTEM_SUMMARY.md) ⭐⭐⭐
**适合人群**: 项目管理者、技术决策者  
**内容**:
- 📦 项目概述和目标
- 📁 完整文件清单
- 🎨 设计规范详解
- 📊 成效对比数据
- 🔮 未来扩展方向
- 👥 贡献指南

**阅读时间**: 15 分钟

---

### 🎯 实战演练

#### 5. [样式演示组件](StyleDemoSlide.vue) ⭐⭐⭐⭐
**适合人群**: 视觉学习者  
**内容**:
- 🎨 可视化展示所有样式
- 📦 实际代码示例
- 🎯 可直接用作幻灯片

**使用方式**: 
```bash
# 在浏览器中查看效果
npm run dev
# 访问 PPT 演示页面
```

---

## 🗺️ 使用场景导航

### 场景 1: 我是新手，第一次使用这个样式系统

**推荐路径**:
1. 阅读 [安装指南](INSTALLATION.md) ✓
2. 浏览 [快速参考](QUICK_REFERENCE.md) ✓
3. 查看 [演示组件](StyleDemoSlide.vue) ✓
4. 开始编码！

---

### 场景 2: 我需要快速查找某个类名的用法

**推荐路径**:
1. 打开 [快速参考](QUICK_REFERENCE.md) ✓
2. 查找"常用类名速查"表格
3. 复制示例代码
4. 粘贴到你的项目中

---

### 场景 3: 我想深入了解设计理念

**推荐路径**:
1. 阅读 [完整指南](README_STYLES.md) 的"核心设计理念"部分 ✓
2. 查看 [_variables.scss](_variables.scss) 了解设计令牌
3. 阅读 [项目总结](STYLE_SYSTEM_SUMMARY.md) 的"设计规范"部分 ✓

---

### 场景 4: 我遇到了编译错误

**推荐路径**:
1. 查看 [安装指南](INSTALLATION.md) 的"常见问题解决"部分 ✓
2. 运行诊断命令（文档中有详细说明）
3. 检查依赖是否正确安装

---

### 场景 5: 我想扩展或修改样式系统

**推荐路径**:
1. 阅读 [项目总结](STYLE_SYSTEM_SUMMARY.md) 的"未来扩展"部分 ✓
2. 查看 [完整指南](README_STYLES.md) 的"扩展现有样式"部分 ✓
3. 阅读 [贡献指南](STYLE_SYSTEM_SUMMARY.md#贡献指南) ✓

---

## 📂 文件结构概览

```
frontend/src/components/ppt/
│
├── 📄 核心样式文件
│   ├── _variables.scss        # 设计令牌（颜色、字体、间距）
│   ├── _mixins.scss          # 可复用样式模式
│   ├── _base-components.scss # 预定义组件类
│   └── styles.scss           # 主入口文件
│
├── 📄 文档文件
│   ├── INDEX.md              # 📍 你在这里（文档导航）
│   ├── INSTALLATION.md       # 安装与配置
│   ├── QUICK_REFERENCE.md    # 快速参考卡片
│   ├── README_STYLES.md      # 完整使用指南
│   └── STYLE_SYSTEM_SUMMARY.md # 项目总结
│
├── 📄 Vue 组件
│   ├── TitleSlide.vue        # 封面（已更新）
│   ├── ResearchBackgroundSlide.vue  # 背景（已更新）
│   ├── SystemArchitectureSlide.vue  # 架构（已更新）
│   ├── StyleDemoSlide.vue    # ✨ 样式演示（新增）
│   └── [...其他幻灯片组件]
│
└── 📄 配置文件
    └── index.js              # 组件导出（已更新）
```

---

## 🎯 快速查找表

### 我想知道...

| 问题 | 答案位置 |
|------|---------|
| 如何安装？ | [INSTALLATION.md](INSTALLATION.md) |
| 有哪些可用的类名？ | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 常用类名速查 |
| 如何使用 mixin？ | [README_STYLES.md](README_STYLES.md) - Mixins 章节 |
| 颜色变量在哪里？ | [_variables.scss](_variables.scss) 或 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 间距系统是什么？ | [_variables.scss](_variables.scss) 或 [README_STYLES.md](README_STYLES.md) |
| 如何创建卡片？ | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 常见场景模板 |
| 响应式如何工作？ | [_base-components.scss](_base-components.scss) 底部 |
| 动画效果有哪些？ | [_mixins.scss](_mixins.scss) - 动画关键帧部分 |
| 遇到错误怎么办？ | [INSTALLATION.md](INSTALLATION.md) - 常见问题解决 |
| 如何扩展样式？ | [README_STYLES.md](README_STYLES.md) - 扩展现有样式 |

---

## 🎓 学习路径建议

### 入门级（预计 1 小时）
1. ✅ 安装依赖（[INSTALLATION.md](INSTALLATION.md)）
2. ✅ 运行演示（[StyleDemoSlide.vue](StyleDemoSlide.vue)）
3. ✅ 阅读快速参考（[QUICK_REFERENCE.md](QUICK_REFERENCE.md)）
4. ✅ 创建第一个幻灯片（使用基础模板）

### 进阶级（预计 3 小时）
1. ✅ 通读完整指南（[README_STYLES.md](README_STYLES.md)）
2. ✅ 理解设计理念（_variables.scss）
3. ✅ 练习使用 mixins（_mixins.scss）
4. ✅ 自定义一个组件样式

### 专家级（预计 1 天）
1. ✅ 研究所有源码
2. ✅ 理解 CSS 架构
3. ✅ 扩展新的样式组件
4. ✅ 优化现有实现

---

## 💡 使用技巧

### 高效开发流程

1. **启动开发服务器**
   ```bash
   npm run dev
   ```

2. **打开两个窗口**
   - 左边：代码编辑器
   - 右边：浏览器（实时预览）

3. **使用快速参考**
   - 将 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) 加入书签
   - 需要时快速查找

4. **参考演示组件**
   - 不确定效果？查看 [StyleDemoSlide.vue](StyleDemoSlide.vue)
   - 直接复制修改

### 调试技巧

- **查看继承链**: DevTools → Computed Styles
- **检查变量值**: [_variables.scss](_variables.scss)
- **测试响应式**: 调整浏览器窗口
- **验证 SCSS**: https://www.sassmeister.com/

---

## 🔗 相关资源

### 内部资源
- [PPTPresentation.vue](../../views/PPTPresentation.vue) - 主容器组件
- [index.js](index.js) - 组件导出配置

### 外部资源
- [SCSS 官方文档](https://sass-lang.com/documentation)
- [Vue.js 官方文档](https://vuejs.org/)
- [Vite 官方文档](https://vitejs.dev/)

---

## ❓ 常见问题 FAQ

### Q: 我应该从哪个文档开始？
**A**: 新手从 [安装指南](INSTALLATION.md) 开始，日常开发看 [快速参考](QUICK_REFERENCE.md)。

### Q: 所有文档都需要读吗？
**A**: 不需要。[快速参考](QUICK_REFERENCE.md) 覆盖 90% 的日常需求，其他作为参考。

### Q: 如何快速找到我需要的信息？
**A**: 使用本文档的"快速查找表"或 Ctrl+F 搜索关键词。

### Q: 文档版本不一致怎么办？
**A**: 以最新的文档为准，通常 [README_STYLES.md](README_STYLES.md) 最完整。

---

## 📞 需要帮助？

如果你在这些文档中找不到答案：

1. **检查是否遗漏了某个步骤**
   - 重新阅读 [安装指南](INSTALLATION.md)

2. **查看示例代码**
   - [TitleSlide.vue](TitleSlide.vue) - 简单示例
   - [StyleDemoSlide.vue](StyleDemoSlide.vue) - 完整示例

3. **运行诊断**
   - 按照 [安装指南](INSTALLATION.md) 的"常见问题解决"排查

---

## 🎉 开始使用

选择适合你的起点：

- 🔰 **新手**: 从 [安装指南](INSTALLATION.md) 开始
- ⚡ **急需**: 直接看 [快速参考](QUICK_REFERENCE.md)
- 👀 **好奇**: 先看看 [项目总结](STYLE_SYSTEM_SUMMARY.md)
- 🎨 **视觉**: 打开 [样式演示](StyleDemoSlide.vue)

---

**祝你使用愉快！** 🚀

*文档最后更新：2026-04-01*  
*样式系统版本：v1.0.0*
