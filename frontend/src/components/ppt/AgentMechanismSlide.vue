<template>
  <div class="slide-content">
    <h2 class="slide-title">LLM-Agent 决策与交互机制</h2>
    <div class="mechanism-container">
      <!-- 第一部分：可控的分析决策机制 -->
      <div class="mechanism-item">
        <div class="number-title-row">
          <div class="number">1</div>
          <h3>可控的分析决策机制</h3>
        </div>
        <div class="content">
          <ul class="feature-list">
            <li>通过结构化提示词定义角色、规则与输出目标</li>
            <li>Agent 在约束下自主规划分析路径（非固定流程）</li>
            <li>采用"理解问题 → 工具调用 → 结果解释"的分步执行策略</li>
          </ul>
          <div class="key-point">
            <span class="highlight-text">实现从"固定流程"到"自主决策"的转变</span>
          </div>
        </div>
      </div>

      <!-- 第二部分：工具驱动与系统鲁棒性设计 -->
      <div class="mechanism-item">
        <div class="number-title-row">
          <div class="number">2</div>
          <h3>工具驱动与系统鲁棒性设计</h3>
        </div>
        <div class="content">
          <ul class="feature-list">
            <li>分析操作由工具完成，Agent仅负责选择与调度</li>
            <li>分析逻辑与计算过程解耦，提升系统扩展性</li>
            <li>引入非阻断式异常处理，工具错误不会中断整体流程</li>
          </ul>
          <div class="key-point">
            <span class="highlight-text">保证系统稳定性与工程可扩展能力</span>
          </div>
        </div>
      </div>

      <!-- 第三部分：交互控制与人机协同机制 -->
      <div class="mechanism-item">
        <div class="number-title-row">
          <div class="number">3</div>
          <h3>交互控制与人机协同机制</h3>
        </div>
        <div class="content">
          <ul class="feature-list">
            <li>支持流式输出与用户中断，实现过程级交互控制</li>
            <li>展示工具调用过程，提升分析透明性与可解释性</li>
            <li>支持历史分析注入，实现人机协同分析</li>
          </ul>
          <div class="key-point">
            <span class="highlight-text">实现"用户可参与"的智能分析过程</span>
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
  display: flex;
  gap: $spacing-lg;
}

.mechanism-item {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-xl - 3px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }

  &:nth-child(1) {
    border-left-color: #667eea;
  }
  &:nth-child(2) {
    border-left-color: #f59e0b;
  }
  &:nth-child(3) {
    border-left-color: #10b981;
  }
}

.number-title-row {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.number {
  font-size: 36px;
  font-weight: bold;
  color: $text-blue;
  min-width: 40px;
  text-align: center;
}

.number-title-row h3 {
  font-size: $font-size-heading + 2px;
  margin: 0;
  flex: 1;
}

.content {
  padding-left: $spacing-xl;
}

//.feature-list {
//  list-style: none;
//  padding: 0;
//  margin: 0 0 $spacing-md 0;
//}
//
//.feature-list li {
//  font-size: $font-size-body-large;
//  line-height: 1.8;
//  padding-left: $spacing-lg;
//  position: relative;
//  margin-bottom: $spacing-sm;
//
//  &:before {
//    content: "•";
//    position: absolute;
//    left: 0;
//    color: $text-white;
//    font-weight: bold;
//    font-size: 20px;
//  }
//}

.feature-list {
  @extend .problem-list;
}

.key-point {
  margin-top: $spacing-md;
  padding: $spacing-md;
  background: rgba(99, 102, 241, 0.1);
  border-left: 4px solid $primary-gradient-start;
  border-radius: $border-radius-sm;
}

.highlight-text {
  font-size: $font-size-body-large;
  font-weight: bold;
  color: $text-opacity-90;
}
</style>
