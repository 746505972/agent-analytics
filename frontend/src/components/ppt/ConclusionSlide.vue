<template>
  <div class="slide-content">
    <h2 class="slide-title">总结与展望</h2>
    <div class="summary-container">
      <div class="summary-section">
        <div class="section-icon">✅</div>
        <h3>工作总结</h3>
        <div class="summary-list">
          <div class="summary-item">
            <span class="check">✓</span>
            <p>构建了基于 LLM-Agent的数据分析系统</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>实现了自然语言驱动的自动化分析流程</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>设计了工具调用和分步分析机制</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>开发了自动化报告生成功能</p>
          </div>
        </div>
      </div>
      
      <div class="outlook-section">
        <div class="section-icon">🚀</div>
        <h3>未来展望</h3>
        <div class="outlook-grid">
          <div class="outlook-item">
            <div class="icon">🧠</div>
            <p>更强的决策能力</p>
            <small>引入思维链和反思机制</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">🔗</div>
            <p>多工具协同</p>
            <small>支持复杂任务的并行处理</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">💡</div>
            <p>更智能的交互</p>
            <small>主动提问和意图识别</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConclusionSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.summary-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: $spacing-xl;
}

.summary-section,
.outlook-section {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-md - 2px $spacing-md + 5px;
  margin-bottom: $spacing-xl + 5px;
  border: 2px solid $card-border-default;
}

.section-icon {
  @include icon-large;
  text-align: center;
  margin-bottom: $spacing-lg;
}

.summary-section h3,
.outlook-section h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
  color: $text-blue;
}

.summary-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg - 3px $spacing-xl - 2px;
  border: 1px solid $card-border-light;
}

.summary-item .check {
  font-size: 24px;
  color: #4ade80;
  font-weight: bold;
}

.summary-item p {
  font-size: $font-size-body-large;
  flex: 1;
}

.outlook-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-lg;
}

.outlook-item {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-xl - 2px;
  text-align: center;
  border: 2px solid $card-border-light;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateY(-5px);
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.25);
  }
}

.outlook-item .icon {
  @include icon-large;
  margin-bottom: $spacing-md;
}

.outlook-item p {
  font-size: $font-size-heading - 2px;
  font-weight: bold;
  margin-bottom: $spacing-xs;
}

.outlook-item small {
  @include caption-text;
}

</style>
