# PPT 统一样式规范使用指南

## 📁 文件结构

```
frontend/src/components/ppt/
├── _variables.scss        # 样式变量定义
├── _mixins.scss          # 可复用的样式模式
├── _base-components.scss # 基础组件样式
├── styles.scss           # 主样式文件（入口）
└── [各个幻灯片组件].vue
```

## 🎨 核心设计理念

### 1. **统一的视觉语言**
- 渐变背景：紫色系 (#667eea → #764ba2)
- 毛玻璃效果：backdrop-filter: blur(10px)
- 卡片式布局：半透明背景 + 边框
- 悬停动画：位移和缩放效果

### 2. **一致的间距系统**
```scss
$spacing-xs: 8px;    // 极小间距
$spacing-sm: 12px;   // 小间距
$spacing-md: 15px;   // 中间距
$spacing-lg: 20px;   // 大间距
$spacing-xl: 25px;   // 超大间距
$spacing-xxl: 35px;  // 特大间距
$spacing-huge: 60px; // 巨大间距
```

### 3. **标准化的字体大小**
```scss
$font-size-title: 72px;        // 封面标题
$font-size-subtitle: 36px;     // 副标题
$font-size-slide-title: 48px;  // 幻灯片标题
$font-size-heading: 22px;      // 卡片标题
$font-size-body-large: 18px;   // 正文 - 大
$font-size-body: 15px;         // 正文
$font-size-body-small: 14px;   // 正文 - 小
$font-size-caption: 13px;      // 说明文字
```

## 🛠️ 使用方法

### 方法一：使用预定义类（推荐）

在组件中直接引入样式文件并使用预定义的 class：

```vue
<template>
  <div class="slide-content">
    <h2 class="slide-title">我的幻灯片标题</h2>
    
    <div class="content-grid">
      <div class="info-card highlight">
        <div class="icon-large">📊</div>
        <h3>卡片标题</h3>
        <p>卡片内容描述</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/components/ppt/styles';
</style>
```

### 方法二：使用 @extend 扩展样式

如果需要自定义类名，可以继承基础样式：

```vue
<style scoped lang="scss">
@import '@/components/ppt/styles';

.my-custom-card {
  @extend .info-card;
  
  h3 {
    @extend h3;
  }
  
  p {
    @extend p;
  }
}
</style>
```

### 方法三：使用 Mixins 创建自定义样式

```vue
<style scoped lang="scss">
@import '@/components/ppt/styles';

.custom-component {
  @include info-card($card-bg-highlight, $card-border-highlight);
  
  .title {
    @include heading-text;
  }
  
  .content {
    @include body-text;
  }
}
</style>
```

## 📦 可用组件类

### 容器类
- `.slide-content` - 幻灯片内容容器（居中、内边距）
- `.content-grid` - 三列网格布局
- `.tools-grid` - 四列工具网格
- `.modules-description` - 四列模块描述

### 卡片类
- `.info-card` - 信息卡片（带悬停效果）
  - `.info-card.highlight` - 高亮版本
  - `.info-card.question` - 问题版本
- `.card-box` - 卡片盒子（带图标和描述）
- `.module-card` - 模块卡片（小型）
- `.tool-box` - 工具盒子

### 文字类
- `.slide-title` - 幻灯片标题（48px）
- `.title` - 封面大标题（72px）
- `.subtitle` - 副标题（36px）
- `.heading-text` - 标题文字（22px）
- `.body-text` - 正文字（15px）
- `.caption-text` - 说明文字（13px）
- `.question-text` - 问题文字（金色加粗）

### 图标类
- `.icon-large` - 大图标（60px）
- `.icon-medium` - 中标图（40px）
- `.icon-small` - 小图标（32px）

### 其他组件
- `.problem-list` / `.bullet-list` - 列表
- `.arrow` - 箭头指示器
- `.data-table` - 数据表格
- `.chart-container` - 图表容器
- `.code-block` - 代码块

## 🎯 常用 Mixins

### 卡片 Mixins
```scss
@include info-card($bg-color, $border-color)  // 信息卡片
@include card-box($bg-color, $border-color)   // 卡片盒子
@include module-card                          // 模块卡片
```

### 文字 Mixins
```scss
@include slide-title        // 幻灯片标题
@include title-text         // 大标题
@include subtitle-text      // 副标题
@include heading-text       // 标题
@include body-text($size, $line-height)  // 正文
@include caption-text       // 说明文字
```

### 图标 Mixins
```scss
@include icon-large    // 大图标
@include icon-medium   // 中标图
@include icon-small    // 小图标
```

### 布局 Mixins
```scss
@include flex-center              // Flex 居中
@include grid-layout($columns, $gap)  // 网格布局
```

### 特效 Mixins
```scss
@include glass-effect       // 毛玻璃效果
@include highlight-card     // 高亮卡片
@include question-card      // 问题卡片
@include fade-in            // 淡入动画
```

## 🌈 颜色变量

```scss
// 主色调
$primary-gradient-start: #667eea;
$primary-gradient-end: #764ba2;

// 文字颜色
$text-white: #ffffff;
$text-gold: #ffd700;

// 卡片背景
$card-bg-default: rgba(255, 255, 255, 0.1);
$card-bg-hover: rgba(255, 255, 255, 0.15);
$card-bg-highlight: rgba(102, 126, 234, 0.3);
$card-bg-question: rgba(118, 75, 162, 0.3);

// 卡片边框
$card-border-default: rgba(255, 255, 255, 0.2);
$card-border-highlight: rgba(102, 126, 234, 0.5);
$card-border-question: rgba(118, 75, 162, 0.5);
$card-border-light: rgba(255, 255, 255, 0.15);
```

## 📝 最佳实践

### ✅ 推荐做法
1. **优先使用预定义类** - 保持最大程度的统一性
2. **使用语义化类名** - 如 `info-card`、`module-item`
3. **遵循间距系统** - 使用 `$spacing-*` 变量
4. **保持一致的动画** - 使用 `$transition-fast` 和 `$transform-hover-*`

### ⚠️ 避免做法
1. ~~不要硬编码样式值~~（如 `font-size: 48px`）
2. ~~不要创建重复的样式~~（优先复用已有样式）
3. ~~不要破坏设计系统~~（保持视觉一致性）
4. ~~不要混用不同的单位~~（统一使用 px）

## 🔧 扩展现有样式

如果需要添加新的样式变体：

```scss
// 在组件的 style 标签中
.info-card.custom-variant {
  @extend .info-card;
  
  // 只覆盖需要修改的部分
  background: rgba(255, 215, 0, 0.2);
  border-color: rgba(255, 215, 0, 0.4);
}
```

## 📱 响应式支持

样式系统已内置响应式适配，在小屏幕设备上会自动调整：
- 标题字号缩小
- 网格布局变为单列
- 内边距减小

无需额外配置即可享受响应式体验。

## 🎓 完整示例

```vue
<template>
  <div class="slide-content">
    <h2 class="slide-title">数据分析流程</h2>
    
    <div class="content-grid">
      <!-- 步骤 1 -->
      <div class="info-card">
        <div class="icon-large">📥</div>
        <h3>数据加载</h3>
        <p>读取 CSV、Excel 等格式数据</p>
      </div>
      
      <!-- 步骤 2 -->
      <div class="info-card highlight">
        <div class="icon-large">🧹</div>
        <h3>数据清洗</h3>
        <p>处理缺失值、异常值</p>
      </div>
      
      <!-- 步骤 3 -->
      <div class="info-card">
        <div class="icon-large">📊</div>
        <h3>数据分析</h3>
        <p>统计分析、机器学习建模</p>
      </div>
    </div>
    
    <div class="modules-description" style="margin-top: 30px;">
      <div class="module-card">
        <h4>工具调用</h4>
        <p>自动选择合适的分析工具</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/components/ppt/styles';
</style>
```

## 💡 提示

1. **SCSS 支持**：确保组件的 `<style>` 标签包含 `lang="scss"`
2. **路径别名**：使用 `@/` 指向 `frontend/src/` 目录
3. **热更新**：修改样式文件后会自动更新所有引用该样式的组件
4. **调试技巧**：在浏览器开发者工具中可以查看继承的样式链

---

如有任何问题或需要新增样式组件，请参考现有代码或联系项目维护者。
