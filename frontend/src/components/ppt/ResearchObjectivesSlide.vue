<template>
  <div class="slide-content">
    <h2 class="slide-title">研究目标与贡献</h2>
    <div class="objectives-container">
      <div class="main-objective">
        <div class="icon-target">🎯</div>
        <h3>总体目标</h3>
        <p>构建一个自然语言驱动的数据分析系统</p>
      </div>
      
      <div class="innovations">
        <div class="innovation-item">
          <div class="number">01</div>
          <div class="content">
            <h4>LLM-Agent 驱动分析流程决策</h4>
            <p>利用大模型的推理能力，自动规划分析路径</p>
          </div>
        </div>
        
        <div class="innovation-item">
          <div class="number">02</div>
          <div class="content">
            <h4>工具调用 + 分步分析机制</h4>
            <p>通过 Function Calling 实现可控的分析过程</p>
          </div>
        </div>
        
        <div class="innovation-item">
          <div class="number">03</div>
          <div class="content">
            <h4>自动化报告生成 + 可控性设计</h4>
            <p>从对话到报告的自动转换，保留人工干预能力</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResearchObjectivesSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.objectives-container {
  max-width: 1200px;
  margin: 0 auto;
}

.main-objective {
  @include highlight-card;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-xl;
  text-align: center;
  margin-bottom: $spacing-xl;
}

.icon-target {
  @include icon-large;
  margin-bottom: $spacing-md;
}

.main-objective h3 {
  font-size: $font-size-heading + 4px;
  margin-bottom: $spacing-sm;
}

.main-objective p {
  font-size: $font-size-body-large;
  opacity: 0.95;
}

.innovations {
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
}

.innovation-item {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg $spacing-xl - 3px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateX(10px);
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.number {
  font-size: 36px;
  font-weight: bold;
  color: $text-gold;
  min-width: 60px;
  text-align: center;
}

.content h4 {
  font-size: $font-size-heading;
  margin-bottom: $spacing-sm;
}

.content p {
  @include caption-text;
}
</style>
