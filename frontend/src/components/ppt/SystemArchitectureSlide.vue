<template>
  <div class="slide-content">
    <h2 class="slide-title">系统总体架构</h2>
    <div class="architecture-diagram">
      <div class="layer input-layer">
        <div class="box">
          <div class="icon">💬</div>
          <p>用户输入</p>
          <p class="desc">自然语言描述需求</p>
        </div>
      </div>
      
      <div class="arrow">↓</div>
      
      <div class="layer agent-layer">
        <div class="box highlight">
          <div class="icon">🧠</div>
          <p>LLM-Agent</p>
          <p class="desc">理解意图 · 规划流程 · 决策调度</p>
        </div>
      </div>
      
      <div class="arrow">↓</div>
      
      <div class="layer tools-layer">
        <div class="tools-grid">
          <div class="tool-box">
            <div class="icon">📊</div>
            <p>数据处理</p>
          </div>
          <div class="tool-box">
            <div class="icon">📈</div>
            <p>统计分析</p>
          </div>
          <div class="tool-box">
            <div class="icon">📉</div>
            <p>机器学习</p>
          </div>
          <div class="tool-box">
            <div class="icon">📊</div>
            <p>可视化</p>
          </div>
        </div>
      </div>
      
      <div class="arrow">↓</div>
      
      <div class="layer output-layer">
        <div class="box">
          <div class="icon">📄</div>
          <p>报告生成</p>
          <p class="desc">自动化文档输出</p>
        </div>
      </div>
    </div>
    
    <div class="modules-description">
      <div class="module-item">
        <h4>Agent 决策模块</h4>
        <p>理解用户需求，规划分析路径</p>
      </div>
      <div class="module-item">
        <h4>工具调用模块</h4>
        <p>根据决策调用相应分析工具</p>
      </div>
      <div class="module-item">
        <h4>数据处理模块</h4>
        <p>数据加载、清洗、预处理</p>
      </div>
      <div class="module-item">
        <h4>报告生成模块</h4>
        <p>整合分析结果，生成结构化报告</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArchitectureSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.architecture-diagram {
  @extend .architecture-diagram;
}

.layer {
  @extend .layer;
}

.box {
  @extend .card-box;
  
  &.highlight {
    @include highlight-card;
  }
}

.icon {
  @extend .icon;
}

.desc {
  @extend .desc;
}

.arrow {
  @extend .arrow;
}

.tools-grid {
  @extend .tools-grid;
}

.tool-box {
  @extend .tool-box;
}

.modules-description {
  @extend .modules-description;
}

.module-item {
  @extend .module-card;
}
</style>
