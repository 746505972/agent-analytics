<template>
  <div class="slide-content">
    <h2 class="slide-title">研究目标与贡献</h2>
    <div class="objectives-container">

      <!-- 总体目标 -->
      <div class="main-objective">
        <h3>总体目标</h3>
        <p>构建一个具备分析决策能力的自适应数据分析系统（LLM-Agent驱动）</p>
      </div>

      <!-- 创新点 -->
      <div class="innovations">
        <div class="innovation-item">
          <div class="number">1</div>
          <div class="content">
            <h4>分析流程的智能决策机制</h4>
            <p>
              将 LLM-Agent 引入数据分析流程，<br/>
              实现从“工具执行”到“自主决策”的转变
            </p>
          </div>
        </div>

        <div class="innovation-item">
          <div class="number">2</div>
          <div class="content">
            <h4>可控的工具调用与分步分析框架</h4>
            <p>
              基于 Function Calling 构建分步分析机制，<br/>
              提升分析过程的可解释性与可控性
            </p>
          </div>
        </div>

        <div class="innovation-item">
          <div class="number">3</div>
          <div class="content">
            <h4>面向结果输出的报告生成方法</h4>
            <p>
              实现对话驱动的报告生成，并支持过程筛选与人工干预
            </p>
          </div>
        </div>

      </div>
    </div>

    <div class="arrow">
      核心提升：从“自动执行工具” → “智能决策分析”
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
  flex-direction: unset;
  gap: $spacing-lg;
}

.innovation-item {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg $spacing-xl - 3px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.number {
  font-size: 36px;
  font-weight: bold;
  color: $text-blue;
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
