<template>
  <div class="slide-content">
    <h2 class="slide-title">相关技术</h2>
    <div class="tech-container">
      <div class="tech-item">
        <div class="tech-icon">🧠</div>
        <div class="tech-info">
          <h3>大语言模型 (LLM)</h3>
          <p>强大的自然语言理解和生成能力</p>
          <p class="highlight">为系统提供"思考"能力</p>
        </div>
      </div>
      
      <div class="tech-item">
        <div class="tech-icon">🔧</div>
        <div class="tech-info">
          <h3>Function Calling</h3>
          <p>结构化输出，精确调用工具函数</p>
          <p class="highlight">连接 AI 与执行能力的桥梁</p>
        </div>
      </div>
      
      <div class="tech-item">
        <div class="tech-icon">🤖</div>
        <div class="tech-info">
          <h3>Agent 技术</h3>
          <p>自主规划、工具使用、任务分解</p>
          <p class="highlight">让系统具备"代理人"特征</p>
        </div>
      </div>
    </div>

    <div class="summary-box">
        <h4>技术整合</h4>
        <p>LLM + Function Calling + Agent = 智能数据分析系统</p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'TechnologiesSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.tech-container {
  display: flex;
  flex-direction: unset;
  gap: $spacing-lg;
}

.tech-item {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg $spacing-xl - 3px;
  margin-bottom: $spacing-lg;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.tech-icon {
  @include icon-large;
  min-width: 60px;
  text-align: center;
}

.tech-info h3 {
  font-size: $font-size-heading + 2px;
  margin-bottom: $spacing-sm;
}

.tech-info p {
  @include caption-text;
}

.tech-info .highlight {
  color: $text-blue;
  font-weight: bold;
  margin-top: $spacing-xs;
  font-size: $font-size-body-small;
}

.summary-box {
  @include highlight-card;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-lg $spacing-xl;
  text-align: center;
  border: 2px solid rgba(255, 255, 255, 0.3);
  margin-top: $spacing-lg;
}

.summary-box h4 {
  font-size: $font-size-heading;
  margin-bottom: $spacing-sm;
}

.summary-box p {
  font-size: $font-size-body-large;
  font-weight: bold;
}
</style>
