<template>
  <div class="slide-content">
    <h2 class="slide-title">系统局限性</h2>
    <div class="limitations-container">
      <div class="limitation-item">
        <div class="icon">⚠️</div>
        <div class="content">
          <h3>一步生成报告问题</h3>
          <p>在某些情况下，Agent 仍会跳过中间分析步骤，直接生成最终报告</p>
          <div class="impact">影响：降低了分析过程的透明度和可控性</div>
        </div>
      </div>
      
      <div class="limitation-item">
        <div class="icon">🔧</div>
        <div class="content">
          <h3>工具调用不完全可控</h3>
          <p>Agent 对工具的选择和调用顺序存在一定随机性</p>
          <div class="impact">影响：可能导致分析路径不够优化</div>
        </div>
      </div>
      
      <div class="limitation-item">
        <div class="icon">🧩</div>
        <div class="content">
          <h3>复杂任务理解有限</h3>
          <p>对于高度复杂或模糊的分析需求，理解能力仍有待提升</p>
          <div class="impact">影响：需要用户多次澄清和调整</div>
        </div>
      </div>
      
      <div class="improvement-direction">
        <h3>改进方向</h3>
        <div class="directions-grid">
          <div class="direction-item">
            <div class="number">01</div>
            <p>强化提示词工程，引导分步思考</p>
          </div>
          <div class="direction-item">
            <div class="number">02</div>
            <p>引入人工审核节点，增强可控性</p>
          </div>
          <div class="direction-item">
            <div class="number">03</div>
            <p>增加领域知识库，提升专业理解</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LimitationsSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.limitations-container {
  max-width: 1200px;
  margin: 0 auto;
}

.limitation-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg - 3px $spacing-xl - 3px;
  margin-bottom: $spacing-lg + 3px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateX(10px);
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.limitation-item .icon {
  @include icon-medium;
  min-width: 60px;
  text-align: center;
}

.limitation-item h3 {
  font-size: $font-size-heading;
  margin-bottom: $spacing-sm;
  color: $text-gold;
}

.limitation-item p {
  @include caption-text;
  margin-bottom: $spacing-xs;
}

.impact {
  background: rgba(239, 68, 68, 0.2);
  border-left: 4px solid #ef4444;
  padding: $spacing-xs $spacing-sm;
  border-radius: 5px;
  font-size: $font-size-body-small;
  margin-top: $spacing-xs;
}

.improvement-direction {
  margin-top: $spacing-xxl + 5px;
  background: rgba(34, 197, 94, 0.15);
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xxl $spacing-xxl + 5px;
  border: 2px solid rgba(34, 197, 94, 0.3);
}

.improvement-direction h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
  color: #4ade80;
}

.directions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-lg;
}

.direction-item {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-xl - 2px;
  text-align: center;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateY(-5px);
    background: $card-bg-hover;
  }
}

.direction-item .number {
  @include icon-large;
  font-weight: bold;
  color: $text-gold;
  margin-bottom: $spacing-md;
}

.direction-item p {
  font-size: $font-size-body;
  line-height: 1.6;
}
</style>
