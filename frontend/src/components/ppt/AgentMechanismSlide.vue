<template>
  <div class="slide-content">
    <h2 class="slide-title">Agent 决策机制</h2>
    <div class="mechanism-container">
      <div class="problem-solution">
        <div class="problem-box">
          <h3>🔴 分析问题</h3>
          <ul>
            <li>用户需求模糊</li>
            <li>分析路径不确定</li>
            <li>需要多步骤推理</li>
          </ul>
        </div>
        
        <div class="solution-box">
          <h3>🟢 解决方案</h3>
          <ul>
            <li>分步分析策略</li>
            <li>工具调用链</li>
            <li>中间结果保留</li>
          </ul>
        </div>
      </div>
      
      <div class="key-mechanisms">
        <h3>关键机制</h3>
        <div class="mechanism-grid">
          <div class="mechanism-item">
            <div class="icon">📝</div>
            <h4>提示词设计</h4>
            <p>控制 Agent 行为模式</p>
          </div>
          
          <div class="mechanism-item highlight">
            <div class="icon">⛓️</div>
            <h4>工具调用链</h4>
            <p>多工具协同完成复杂任务</p>
          </div>
          
          <div class="mechanism-item">
            <div class="icon">💾</div>
            <h4>中间过程保留</h4>
            <p>记录每一步分析结果</p>
          </div>
          
          <div class="mechanism-item highlight">
            <div class="icon">⏸️</div>
            <h4>打断机制</h4>
            <p>用户可随时干预调整方向</p>
          </div>
        </div>
      </div>
      
      <div class="workflow">
        <h3>工作流程</h3>
        <div class="workflow-steps">
          <div class="step">
            <div class="step-number">1</div>
            <p>理解需求</p>
          </div>
          <div class="arrow">→</div>
          <div class="step">
            <div class="step-number">2</div>
            <p>规划路径</p>
          </div>
          <div class="arrow">→</div>
          <div class="step">
            <div class="step-number">3</div>
            <p>调用工具</p>
          </div>
          <div class="arrow">→</div>
          <div class="step">
            <div class="step-number">4</div>
            <p>输出结果</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgentMechanismSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.mechanism-container {
  max-width: 1200px;
  margin: 0 auto;
}

.problem-solution {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-lg;
  margin-bottom: $spacing-xl + 5px;
}

.problem-box,
.solution-box {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg;
  border: 2px solid $card-border-default;
}

.problem-box {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
}

.solution-box {
  background: rgba(34, 197, 94, 0.2);
  border-color: rgba(34, 197, 94, 0.4);
}

.problem-box h3,
.solution-box h3 {
  font-size: $font-size-heading + 4px;
  margin-bottom: $spacing-lg;
}

.problem-box ul,
.solution-box ul {
  list-style: none;
  padding-left: 0;
}

.problem-box li,
.solution-box li {
  font-size: $font-size-body-large;
  line-height: 2;
  padding-left: $spacing-lg;
  position: relative;
}

.problem-box li:before {
  content: "✗";
  position: absolute;
  left: 0;
  color: #ef4444;
}

.solution-box li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #22c55e;
}

.key-mechanisms {
  margin-bottom: $spacing-xl + 5px;
}

.key-mechanisms h3 {
  font-size: $font-size-heading + 4px;
  margin-bottom: $spacing-lg;
  text-align: center;
}

.mechanism-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-md;
}

.mechanism-item {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg $spacing-md;
  text-align: center;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &.highlight {
    @include highlight-card;
  }
  
  &:hover {
    transform: translateY(-5px);
    background: $card-bg-hover;
  }
}

.mechanism-item .icon {
  @include icon-medium;
  margin-bottom: $spacing-sm;
}

.mechanism-item h4 {
  font-size: $font-size-caption + 4px;
  margin-bottom: $spacing-xs;
}

.mechanism-item p {
  @include caption-text;
}

.workflow h3 {
  font-size: $font-size-heading + 4px;
  margin-bottom: $spacing-lg;
  text-align: center;
}

.workflow-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg;
  border: 2px solid $card-border-default;
}

.step {
  text-align: center;
  flex: 1;
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, $primary-gradient-start, $primary-gradient-end);
  color: $text-white;
  font-size: 22px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto $spacing-sm;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.step p {
  font-size: $font-size-body-small;
  font-weight: bold;
}

.arrow {
  font-size: 32px;
  opacity: 0.6;
  margin: 0 $spacing-xs;
}
</style>
