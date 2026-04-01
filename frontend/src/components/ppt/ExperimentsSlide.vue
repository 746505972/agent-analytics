<template>
  <div class="slide-content">
    <h2 class="slide-title">实验与效果分析</h2>
    <div class="comparison-container">
      <div class="comparison-table">
        <div class="table-header">
          <div class="header-cell empty"></div>
          <div class="header-cell highlight">传统分析流程</div>
          <div class="header-cell success">本系统</div>
        </div>
        
        <div class="table-row">
          <div class="cell label">学习成本</div>
          <div class="cell traditional">高<br><small>需要编程和统计知识</small></div>
          <div class="cell our-system success">低<br><small>自然语言即可</small></div>
        </div>
        
        <div class="table-row">
          <div class="cell label">分析效率</div>
          <div class="cell traditional">低<br><small>多工具切换，手动操作</small></div>
          <div class="cell our-system success">高<br><small>自动化执行</small></div>
        </div>
        
        <div class="table-row">
          <div class="cell label">自动化程度</div>
          <div class="cell traditional">低<br><small>需要人工规划流程</small></div>
          <div class="cell our-system success">高<br><small>Agent 自主决策</small></div>
        </div>
        
        <div class="table-row">
          <div class="cell label">用户体验</div>
          <div class="cell traditional">复杂<br><small>专业门槛高</small></div>
          <div class="cell our-system success">简单<br><small>零代码基础</small></div>
        </div>
      </div>
      
      <div class="metrics">
        <h3>关键指标提升</h3>
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="percentage">⬇️ 90%</div>
            <p>学习成本降低</p>
          </div>
          
          <div class="metric-item">
            <div class="percentage">⬆️ 5x</div>
            <p>分析效率提升</p>
          </div>
          
          <div class="metric-item">
            <div class="percentage">✅ 100%</div>
            <p>零代码要求</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExperimentsSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.comparison-container {
  max-width: 1200px;
  margin: 0 auto;
}

.comparison-table {
  margin-bottom: $spacing-xxl + 5px;
  border-radius: $border-radius-lg;
  overflow: hidden;
  border: 2px solid $card-border-default;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 3fr 3fr;
  background: rgba(255, 255, 255, 0.15);
}

.header-cell {
  padding: $spacing-md;
  font-size: $font-size-heading - 2px;
  font-weight: bold;
  text-align: center;
  border-right: 1px solid $card-border-light;
}

.header-cell.empty {
  background: transparent;
}

.header-cell.highlight {
  background: rgba(239, 68, 68, 0.3);
}

.header-cell.success {
  background: rgba(34, 197, 94, 0.3);
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 3fr 3fr;
  border-bottom: 1px solid $card-border-light;
}

.table-row:last-child {
  border-bottom: none;
}

.cell {
  padding: $spacing-lg;
  text-align: center;
  border-right: 1px solid $card-border-light;
}

.cell.label {
  font-weight: bold;
  font-size: $font-size-heading - 2px;
  background: rgba(255, 255, 255, 0.05);
}

.cell.traditional {
  background: rgba(239, 68, 68, 0.1);
}

.cell.our-system {
  background: rgba(34, 197, 94, 0.1);
}

.cell.success {
  color: #4ade80;
  font-weight: bold;
}

.cell small {
  font-size: $font-size-body-small;
  opacity: 0.8;
  font-weight: normal;
}

.metrics {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xxl $spacing-xxl + 5px;
  border: 2px solid $card-border-default;
}

.metrics h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-xl;
}

.metric-item {
  text-align: center;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-xl - 2px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: scale(1.05);
    background: $card-bg-hover;
  }
}

.percentage {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: $spacing-md;
}

.metric-item p {
  font-size: $font-size-body-large;
  opacity: 0.9;
}
</style>
