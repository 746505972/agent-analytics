<template>
  <div class="slide-content">
    <h2 class="slide-title">总结与展望</h2>
    <div class="summary-container">
      <div class="summary-section">
<!--        <div class="section-icon">✅</div>-->
        <h3>研究工作总结</h3>
        <div class="summary-list">
          <div class="summary-item">
            <span class="check">✓</span>
            <p>构建了"LLM决策+工具执行"的分析架构</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>实现了自然语言驱动的数据处理、统计分析与机器学习建模</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>设计了无状态工具与集中式会话管理机制</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>开发了基于分析过程记录的自动化报告生成功能</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>通过实验验证了系统的可行性与有效性</p>
          </div>
          <div class="summary-item">
            <span class="check">✓</span>
            <p>开源项目发布至GitHub，持续迭代更新</p>
          </div>
        </div>
      </div>
      
      <div class="outlook-section">
<!--        <div class="section-icon">🚀</div>-->
        <h3>不足与展望</h3>
        <div class="outlook-grid">
          <div class="outlook-item">
            <div class="icon">🎯</div>
            <p>增强意图理解能力</p>
            <small>优化提示策略，引入用户确认机制</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">📊</div>
            <p>改进报告生成机制</p>
            <small>发挥LLM自动总结与结构化表达潜力</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">🔧</div>
            <p>扩展分析工具库</p>
            <small>支持领域特定分析方法，标准化接口</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">👥</div>
            <p>扩大实验验证范围</p>
            <small>更多用户群体与多样化数据场景</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">💡</div>
            <p>个性化分析辅助</p>
            <small>结合用户行为数据与历史分析记录</small>
          </div>
          
          <div class="outlook-item">
            <div class="icon">🌐</div>
            <p>推广应用至实际场景</p>
            <small>教学、科研及业务分析等多层级支持</small>
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
  padding: $spacing-md - 3px $spacing-md - 2px;
  border: 1px solid $card-border-light;
}

.summary-item .check {
  font-size: 20px;
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
