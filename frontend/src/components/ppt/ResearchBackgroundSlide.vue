<template>
  <div class="slide-content">
    <h2 class="slide-title">研究背景与问题</h2>
    <div class="content-grid">
      <div class="info-card highlight">
        <div class="card-icon">📊</div>
        <h3>数据分析的重要性</h3>
        <p>大数据时代，数据分析成为决策支持的核心工具</p>
      </div>
      <div class="info-card">
        <div class="card-problem">⚠️</div>
        <h3>当前痛点</h3>
        <ul class="problem-list">
          <li>门槛高：需要编程和统计知识</li>
          <li>流程复杂：多步骤、多工具切换</li>
          <li>自动化工具"不会思考"</li>
        </ul>
      </div>
      <div class="info-card question">
        <div class="card-icon">❓</div>
        <h3>核心问题</h3>
        <p class="question-text">能不能让系统"像人一样分析数据"？</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResearchBackgroundSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.content-grid {
  @extend .content-grid;
}

.info-card {
  @extend .info-card;
  
  h3 {
    @extend h3;
  }
  
  p {
    @extend p;
  }
}

.problem-list {
  @extend .problem-list;
}

.question-text {
  @extend .question-text;
}
</style>
