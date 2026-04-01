# PPT 样式快速参考

## 🚀 快速开始（复制即用）

### 基础模板
```vue
<template>
  <div class="slide-content">
    <h2 class="slide-title">标题</h2>
    <div class="content-grid">
      <div class="info-card">
        <div class="icon-large">📊</div>
        <h3>小标题</h3>
        <p>描述文字</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/components/ppt/styles';
</style>
```

## 📋 常用类名速查

### 容器
| 类名 | 用途 | 说明 |
|------|------|------|
| `.slide-content` | 幻灯片内容容器 | 居中、自动内边距 |
| `.content-grid` | 三列网格 | 默认 3 列，等大分布 |
| `.tools-grid` | 四列工具网格 | 4 列布局 |
| `.modules-description` | 模块说明网格 | 4 列布局 |

### 卡片
| 类名 | 用途 | 特点 |
|------|------|------|
| `.info-card` | 信息卡片 | 毛玻璃、悬停上浮 |
| `.info-card.highlight` | 高亮卡片 | 紫色背景 |
| `.info-card.question` | 问题卡片 | 深紫背景 |
| `.card-box` | 通用卡片盒 | 悬停放大 |
| `.module-card` | 模块卡片 | 小型卡片 |
| `.tool-box` | 工具盒子 | 紧凑布局 |

### 文字
| 类名 | 字体大小 | 用途 |
|------|---------|------|
| `.slide-title` | 48px | 幻灯片主标题 |
| `.title` | 72px | 封面大标题 |
| `.subtitle` | 36px | 副标题 |
| `h3` | 22px | 卡片标题 |
| `p` | 15px | 正文 |

### 图标
| 类名 | 大小 | 用途 |
|------|------|------|
| `.icon-large` | 60px | 大图标（卡片顶部） |
| `.icon-medium` | 40px | 中标图 |
| `.icon-small` | 32px | 小图标 |

## 🎨 颜色变量

```scss
// 金色（强调色）
$text-gold: #ffd700;

// 卡片背景
$card-bg-default: rgba(255, 255, 255, 0.1);     // 默认
$card-bg-highlight: rgba(102, 126, 234, 0.3);   // 高亮
$card-bg-question: rgba(118, 75, 162, 0.3);     // 问题
```

## 🔧 Mixins 速查

### 创建卡片
```scss
@include info-card($bg-color, $border-color)
```

### 文字样式
```scss
@include slide-title      // 幻灯片标题
@include body-text        // 正文
@include heading-text     // 标题
```

### 布局
```scss
@include grid-layout(3, 25px)  // 3 列网格，间距 25px
@include flex-center           // Flex 居中
```

## 📱 响应式断点

- 默认：桌面端（多列网格）
- ≤768px：移动端（单列网格，字号缩小）

## ✨ 交互效果

### 悬停效果
- **info-card**: 向上浮动 `translateY(-10px)`
- **card-box**: 放大 `scale(1.02)`
- **indicator**: 放大 `scale(1.2)`

### 动画
- **淡入**: `fadeIn 0.5s ease-in-out`
- **过渡**: `0.3s ease`

## 🎯 常见场景模板

### 场景 1：三栏对比
```vue
<div class="content-grid">
  <div class="info-card highlight">
    <div class="icon-large">✅</div>
    <h3>优势</h3>
    <p>描述内容</p>
  </div>
  <div class="info-card">
    <div class="icon-large">⚠️</div>
    <h3>挑战</h3>
    <p>描述内容</p>
  </div>
  <div class="info-card question">
    <div class="icon-large">❓</div>
    <h3>问题</h3>
    <p>描述内容</p>
  </div>
</div>
```

### 场景 2：工具展示
```vue
<div class="tools-grid">
  <div class="tool-box">
    <div class="icon-small">📊</div>
    <p>数据处理</p>
  </div>
  <div class="tool-box">
    <div class="icon-small">📈</div>
    <p>统计分析</p>
  </div>
</div>
```

### 场景 3：模块说明
```vue
<div class="modules-description">
  <div class="module-card">
    <h4>模块名称</h4>
    <p>功能描述</p>
  </div>
</div>
```

### 场景 4：列表展示
```vue
<ul class="problem-list">
  <li>第一点内容</li>
  <li>第二点内容</li>
  <li>第三点内容</li>
</ul>
```

## 💡 使用技巧

### ✅ DO（推荐）
```vue
<!-- 使用语义化类名 -->
<div class="info-card highlight">

<!-- 使用预定义图标大小 -->
<div class="icon-large">

<!-- 引入统一样式 -->
@import '@/components/ppt/styles';
```

### ❌ DON'T（避免）
```vue
<!-- 不要硬编码样式 -->
<div style="font-size: 48px;">

<!-- 不要重复定义颜色 -->
background: rgba(255, 255, 255, 0.1);

<!-- 不要使用行内样式 -->
<div style="margin-top: 80px;">
```

## 🔍 调试技巧

1. **查看继承链**：在 DevTools 中查看 Computed Styles
2. **检查变量值**：在 `_variables.scss` 中查找
3. **测试响应式**：调整浏览器窗口宽度
4. **修改间距**：使用 `$spacing-*` 变量而非固定值

---

**提示**：将此页面加入书签，需要时快速查阅！
