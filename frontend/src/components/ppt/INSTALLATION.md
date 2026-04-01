# PPT 样式系统 - 安装与配置指南

## ✅ 前置要求

确保你的开发环境满足以下要求：

- **Node.js**: v16.0.0 或更高版本
- **npm**: v7.0.0 或更高版本
- **Vue**: v3.5.24+ (项目已包含)
- **Vite**: v7.2.2+ (项目已包含)

## 📦 依赖检查

### 必需依赖

项目已经包含以下必需依赖（检查 `package.json`）：

```json
{
  "dependencies": {
    "vue": "^3.5.24",
    "vue-router": "^4.6.3"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^6.0.1",
    "sass-embedded": "^1.98.0",
    "vite": "^7.2.2"
  }
}
```

### 关键依赖说明

1. **sass-embedded** (^1.98.0)
   - 用于编译 SCSS 文件
   - Vite 会自动使用它处理 `.scss` 文件
   - ✅ 已安装，无需额外操作

2. **@vitejs/plugin-vue**
   - 支持 Vue 单文件组件
   - 自动处理 `<style scoped lang="scss">`
   - ✅ 已配置

## 🚀 快速开始

### 步骤 1：安装依赖

如果还没有安装依赖，运行：

```bash
cd frontend
npm install
```

### 步骤 2：验证 SCSS 支持

创建测试文件 `frontend/src/test-scss.vue`：

```vue
<template>
  <div class="test">SCSS 测试</div>
</template>

<style scoped lang="scss">
$test-color: #667eea;

.test {
  color: $test-color;
  font-size: 20px;
}
</style>
```

如果能正常编译，说明 SCSS 工作正常。

### 步骤 3：使用 PPT 样式系统

在任意 PPT 幻灯片组件中：

```vue
<template>
  <div class="slide-content">
    <h2 class="slide-title">我的标题</h2>
    <div class="info-card">
      <p>内容</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/components/ppt/styles';
</style>
```

## ⚙️ Vite 配置

当前 Vite 配置（`vite.config.js`）已包含必要设置：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],  // ✅ 自动处理 SCSS
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')  // ✅ 支持 @ 路径别名
    }
  }
})
```

**无需修改配置**，开箱即用！

## 🔧 常见问题解决

### 问题 1: SCSS 编译错误

**错误信息**: `[plugin:vite:css] Can't find stylesheet to import.`

**解决方案**:
```bash
# 重新安装依赖
rm -rf node_modules package-lock.json
npm install
```

### 问题 2: 路径别名不工作

**错误信息**: `Cannot find module '@/components/ppt/styles'`

**解决方案**:
1. 检查 `vite.config.js` 是否有 `@` 别名配置
2. 重启开发服务器
3. 清除 IDE 缓存

### 问题 3: @extend 不生效

**原因**: Vue 的 scoped 样式隔离

**解决方案**:
```vue
<!-- ❌ 错误 -->
<style scoped lang="scss">
@import '@/components/ppt/styles';
.my-class {
  @extend .info-card;
}
</style>

<!-- ✅ 正确 -->
<style scoped lang="scss">
@import '@/components/ppt/styles';

// 方法 1: 直接使用类名
// <div class="info-card"></div>

// 方法 2: 使用 mixins
.my-class {
  @include info-card;
}
</style>
```

### 问题 4: 样式冲突

**症状**: 自定义样式覆盖了统一样式

**解决方案**:
```vue
<!-- ❌ 避免在内联样式中定义已存在的样式 -->
<div class="info-card" style="background: red;">

<!-- ✅ 使用 CSS 优先级覆盖 -->
<style scoped lang="scss">
@import '@/components/ppt/styles';

.info-card.custom {
  background: red;
}
</style>

<div class="info-card custom">
```

## 📝 使用清单

### ✅ 必须遵守的规则

1. **所有 PPT 组件必须使用 `lang="scss"`**
   ```vue
   <style scoped lang="scss">
   ```

2. **必须导入统一样式**
   ```vue
   @import '@/components/ppt/styles';
   ```

3. **优先使用预定义类名**
   ```vue
   <div class="slide-content">
   <h2 class="slide-title">
   <div class="info-card">
   ```

4. **不要硬编码样式值**
   ```scss
   // ❌ 错误
   font-size: 48px;
   
   // ✅ 正确
   @include slide-title;
   // 或
   font-size: $font-size-slide-title;
   ```

### ✅ 推荐做法

1. **查看演示组件获取灵感**
   - 位置：`StyleDemoSlide.vue`
   - 用途：可视化展示所有可用样式

2. **查阅快速参考**
   - 文件：`QUICK_REFERENCE.md`
   - 场景：日常开发时快速查找

3. **深入阅读完整文档**
   - 文件：`README_STYLES.md`
   - 场景：系统性学习和理解

## 🎯 验证安装

### 测试步骤

1. **启动开发服务器**
   ```bash
   cd frontend
   npm run dev
   ```

2. **访问 PPT 演示页面**
   ```
   http://localhost:5173/#/ppt
   ```

3. **检查以下内容**:
   - ✅ 渐变背景显示正常（紫色系）
   - ✅ 卡片有毛玻璃效果
   - ✅ 悬停时有动画（上浮或放大）
   - ✅ 文字清晰可见，大小合适
   - ✅ 响应式布局在小屏幕正常工作

### 预期效果

如果一切正常，你应该看到：
- 统一的紫色渐变背景
- 半透明卡片带有圆角和边框
- 鼠标悬停时卡片会上浮或放大
- 文字使用白色，标题有阴影效果
- 所有元素间距一致、视觉和谐

## 🔄 升级指南

### 更新样式系统

如果需要更新样式变量或添加新组件：

1. **修改变量** (`_variables.scss`)
   ```scss
   // 修改主色调
   $primary-gradient-start: #newcolor;
   ```

2. **添加新 Mixin** (`_mixins.scss`)
   ```scss
   @mixin my-new-mixin {
     // 样式代码
   }
   ```

3. **添加新组件类** (`_base-components.scss`)
   ```scss
   .my-new-component {
     @include my-new-mixin;
   }
   ```

4. **所有组件自动更新** - 无需手动修改各个组件

### 测试变更

修改后运行：
```bash
npm run build
```

检查是否有编译错误，然后测试所有 PPT 页面。

## 💻 IDE 支持

### VS Code 推荐插件

1. **Vetur** 或 **Volar**
   - Vue 单文件组件支持
   - SCSS 语法高亮

2. **SCSS IntelliSense**
   - 变量和 mixin 自动补全
   - 跳转到定义

3. **Path Intellisense**
   - 路径自动补全
   - 支持 `@` 别名

### WebStorm

WebStorm 内置支持：
- ✅ Vue.js
- ✅ SCSS
- ✅ 路径别名

无需额外配置。

## 📱 浏览器测试

### 桌面浏览器
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### 移动浏览器
- ✅ iOS Safari 14+
- ✅ Chrome Mobile 90+
- ✅ Samsung Internet 14+

### 测试命令

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

然后在不同设备上访问预览地址。

## 🆘 获取帮助

如果遇到无法解决的问题：

1. **查看错误日志**
   ```bash
   npm run dev -- --debug
   ```

2. **检查 SCSS 语法**
   - 使用在线工具：https://www.sassmeister.com/
   - 粘贴代码验证语法

3. **参考示例**
   - `TitleSlide.vue` - 基础示例
   - `StyleDemoSlide.vue` - 完整示例

4. **查阅文档**
   - `README_STYLES.md` - 详细说明
   - `QUICK_REFERENCE.md` - 快速解答

---

**提示**: 保持依赖更新到最新兼容版本，但避免跨大版本升级。

*最后更新：2026-04-01*
