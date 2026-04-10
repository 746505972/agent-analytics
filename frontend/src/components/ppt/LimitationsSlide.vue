<template>
  <div class="slide-content">
    <h2 class="slide-title">系统局限性</h2>
    <div class="limitations-container">
      <div class="limitation-item">
<!--        <div class="icon">⚠️</div>-->
        <div class="content">
          <h3>分析流程控制不稳定</h3>
          <p>用户输入模糊时（如"分析一下"），Agent仍可能跳过引导步骤，直接调用多工具生成完整报告</p>
          <div class="impact">原因：模型对"任务完成度"的偏好，倾向于输出更全面的结果</div>
          <div class="solution">已引入打断流式生成机制进行事后干预</div>
        </div>
      </div>
      
      <div class="limitation-item">
<!--        <div class="icon">🔧</div>-->
        <div class="content">
          <h3>用户意图约束不足</h3>
          <p>明确要求"仅相关性分析"时，Agent仍可能自动扩展调用回归分析等后续工具</p>
          <div class="impact">原因：模型基于常见分析流程自动扩展，任务边界识别不足</div>
          <div class="solution">需引入结构化约束机制（显式任务规划、工具调用次数限制）</div>
        </div>
      </div>
      
      <div class="limitation-item">
<!--        <div class="icon">📊</div>-->
        <div class="content">
          <h3>高维数据场景适应性弱</h3>
          <p>列数极多的数据集会导致工具选择不稳定、分析步骤混乱、结果解释质量下降</p>
          <div class="impact">原因：高维数据序列化后占用大量上下文，干扰关键信息提取</div>
          <div class="solution">需引入特征筛选、摘要表示或上下文压缩机制</div>
        </div>
      </div>
    </div>

    <div class="green-note">
      <div class="improvement-direction">
<!--        <div class="icon">✨</div>-->
        <h3>被动演进优势</h3>
        <p>系统基于云端API调用大语言模型,随底层模型能力提升而自然改善,无需频繁迭代即可获得推理与指令遵循能力的增强</p>
      </div>

      <div class="improvement-direction">
        <h3>未来改进方向</h3>
        <ul class="directions-grid">
          <li>强化任务规划机制,提升流程控制稳定性</li>
          <li>引入结构化约束,增强用户意图边界识别</li>
          <li>优化上下文管理,提升高维数据处理能力</li>
        </ul>
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
  margin: 0 auto;
  display:grid;
  grid-template-columns: repeat(3, 1fr);
}

.limitation-item {
  display: flex;
  align-items: flex-start;
  gap: $spacing-lg;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg - 3px $spacing-xl - 3px;
  margin-bottom: $spacing-sm;
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
  color: $text-red;
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

.solution {
  background: rgba(59, 130, 246, 0.2);
  border-left: 4px solid #3b82f6;
  padding: $spacing-xs $spacing-sm;
  border-radius: 5px;
  font-size: $font-size-body-small;
  margin-top: $spacing-xs;
  color: #60a5fa;
}

.improvement-direction {
  background: rgba(34, 197, 94, 0.15);
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xl $spacing-xl;
  border: 2px solid rgba(34, 197, 94, 0.3);
  flex: 1;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateY(-5px);
    background: rgba(34, 197, 94, 0.2);
  }
}

.improvement-direction h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
  color: #4ade80;
}

.directions-grid {
  @extend .problem-list;
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
  color: $text-blue;
  margin-bottom: $spacing-md;
}

.direction-item p {
  font-size: $font-size-body;
  line-height: 1.6;
}

.green-note {
  display: flex;
  gap: $spacing-lg;
  margin-top: $spacing-xl;
}
</style>
