<template>
  <div class="slide-content">
    <h2 class="slide-title">系统总体架构</h2>
    
    <!-- 主内容区：左 - 中-右布局 -->
    <div class="main-layout">
      <!-- 左侧卡片 -->
      <div class="side-column">
        <div class="module-item">
          <div class="module-icon">👤</div>
          <h4>用户层</h4>
          <p>双模式交互：Agent 对话 或 可视化操作</p>
        </div>
        <div class="module-item">
          <div class="module-icon">🧠</div>
          <h4>Agent 代理层</h4>
          <p>核心决策中枢：意图解析、任务规划、工具选择、任务执行、报告生成</p>
        </div>
      </div>
      
      <!-- 中间 iframe -->
      <img src="@/assets/images/系统架构图.svg" width="50%" alt="Agent-Analytics" style="border-radius: 15px">

      <!-- 右侧卡片 -->
      <div class="side-column">
        <div class="module-item">
          <div class="module-icon">⚙️</div>
          <h4>工具接口层</h4>
          <p>执行引擎：文件处理工具、文件分析工具</p>
        </div>
        <div class="module-item">
          <div class="module-icon">📦</div>
          <h4>输出层</h4>
          <p>多维度输出：前端展示、PDF 报告、图表、文字结果、下载文件</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArchitectureSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.architecture-diagram {
  @extend .architecture-diagram;
}

.main-layout {
  display: flex;
  gap: 20px;
  height: calc(100% - 60px);
  margin-top: 20px;
}

.side-column {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
  max-width: 280px;
}

.module-item {
  @extend .module-card;
  text-align: center;
  padding: 16px;
  border-left: 3px solid transparent;
  transition: all $transition-fast;

  &:nth-child(1) {
    border-left-color: #667eea;
  }
  &:nth-child(2) {
    border-left-color: #f59e0b;
  }
  &:nth-child(3) {
    border-left-color: #10b981;
  }
  &:nth-child(4) {
    border-left-color: #3b82f6;
  }
  &:hover {
    transform: translateY(-5px)
  }
}

.module-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

</style>
