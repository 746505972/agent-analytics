<template>
  <div class="slide-content">
    <h2 class="slide-title">报告生成方法</h2>
    <div class="report-container">
      <div class="process-flow">
        <div class="flow-step">
          <div class="step-icon">💬</div>
          <h4>对话记录</h4>
          <p>完整的交互历史</p>
        </div>
        
        <div class="arrow">→</div>
        
        <div class="flow-step">
          <div class="step-icon">🔍</div>
          <h4>内容筛选</h4>
          <p>提取关键分析结果</p>
        </div>
        
        <div class="arrow">→</div>
        
<!--        <div class="flow-step">-->
<!--          <div class="step-icon">📑</div>-->
<!--          <h4>结构组织</h4>-->
<!--          <p>按章节逻辑编排</p>-->
<!--        </div>-->
<!--        -->
<!--        <div class="arrow">→</div>-->
        
        <div class="flow-step">
          <div class="step-icon">📄</div>
          <h4>文档输出</h4>
          <p>Word/PDF/Markdown</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ReportGenerationSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.report-container {
  max-width: 1200px;
  margin: 0 auto;
}

.process-flow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xxl $spacing-xl + 5px;
  margin-bottom: $spacing-xxl + 5px;
  border: 2px solid $card-border-default;
}

.flow-step {
  text-align: center;
  flex: 1;
  transition: all $transition-fast;
  
  &:hover {
    transform: scale(1.05);
  }
}

.step-icon {
  @include icon-large;
  margin-bottom: $spacing-md;
}

.flow-step h4 {
  font-size: $font-size-heading;
  margin-bottom: $spacing-md;
  color: $text-blue;
}

.flow-step p {
  @include caption-text;
}

.arrow {
  font-size: 40px;
  opacity: 0.6;
  margin: 0 $spacing-md;
}

.key-points {
  margin-top: $spacing-xl + 5px;
}

.key-points h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
}

.points-grid {
  display: flex;
  gap: $spacing-lg;
}

.point-item {
  display: flex;
  align-items: center;
  gap: $spacing-xl;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-xl - 2px $spacing-xl + 3px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateX(10px);
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.number {
  font-size: 42px;
  font-weight: bold;
  color: $text-blue;
  min-width: 70px;
  text-align: center;
}

.content h4 {
  font-size: $font-size-heading + 2px;
  margin-bottom: $spacing-sm;
}

.content p {
  font-size: $font-size-body-large - 1px;
  line-height: 1.6;
  opacity: 0.9;
}
</style>
