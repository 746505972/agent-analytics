<template>
  <div class="slide-content">
    <h2 class="slide-title">工具体系与报告生成</h2>
    
    <!-- 数据分析工具部分 -->
    <div class="tools-container">
      <div class="tool-category">
        <div class="category-icon">🧹</div>
        <h3>数据预处理</h3>
        <ul>
          <li>数据清洗</li>
          <li>缺失值处理</li>
          <li>异常值检测</li>
          <li>数据类型转换</li>
        </ul>
      </div>
      
      <div class="tool-category">
        <div class="category-icon">📊</div>
        <h3>统计分析</h3>
        <ul>
          <li>描述性统计</li>
          <li>相关性分析</li>
          <li>假设检验</li>
          <li>回归分析</li>
        </ul>
      </div>
      
      <div class="tool-category">
        <div class="category-icon">🤖</div>
        <h3>机器学习</h3>
        <ul>
          <li>分类算法</li>
          <li>聚类分析</li>
          <li>神经网络</li>
          <li>XGBoost</li>
        </ul>
      </div>
      
      <div class="tool-category">
        <div class="category-icon">📈</div>
        <h3>可视化</h3>
        <ul>
          <li>基础图表</li>
          <li>分布图</li>
          <li>热力图</li>
          <li>词云图</li>
        </ul>
      </div>

<!--      <div class="feature-highlight">-->
<!--        <div class="icon">✨</div>-->
<!--        <p>一份代码,两处使用</p>-->
<!--      </div>-->
    </div>

    <!-- 报告生成流程部分 -->
    <div class="report-section">
<!--      <h3 class="section-subtitle">报告生成方法</h3>-->
      <div class="process-flow">
        <div class="flow-step">
          <div class="step-icon">💬</div>
          <h4>对话记录</h4>
          <p>完整的交互历史</p>
        </div>
        
        <div class="arrow">→</div>
        
        <div class="flow-step">
          <div class="step-icon">🔍</div>
          <h4>内容筛选</h4>
          <p>提取关键分析结果</p>
        </div>
        
        <div class="arrow">→</div>
        
        <div class="flow-step">
          <div class="step-icon">📄</div>
          <h4>文档输出</h4>
          <p>Word/PDF/Markdown</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'AnalysisToolsSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.tools-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-lg + 3px;
  margin-bottom: $spacing-xl - 6px;
}

.tool-category {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg $spacing-md + 3px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateY(-8px);
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.category-icon {
  @include icon-large;
  margin-bottom: $spacing-md;
  text-align: center;
}

.tool-category h3 {
  font-size: $font-size-heading;
  margin-bottom: $spacing-md;
  text-align: center;
  color: $text-blue;
}

.tool-category ul {
  list-style: none;
  padding: 0;
}

.tool-category li {
  @include caption-text;
  padding-left: $spacing-md + 3px;
  position: relative;
}

.tool-category li:before {
  content: "▸";
  position: absolute;
  left: 0;
  color: $text-blue;
}

.feature-highlight {
  @include highlight-card;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-lg $spacing-xl;
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.feature-highlight .icon {
  @include icon-large;
}

.feature-highlight p {
  font-size: $font-size-body-large;
  font-weight: bold;
}

/* 报告生成部分样式 */
.report-section {
  margin-bottom: $spacing-xl;
}

.section-subtitle {
  font-size: $font-size-heading + 8px;
  margin-bottom: $spacing-lg;
  text-align: center;
  color: $text-blue;
}

.process-flow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xl $spacing-lg + 5px;
  border: 2px solid $card-border-default;
}

.flow-step {
  text-align: center;
  flex: 1;
  transition: all $transition-fast;
  
  &:hover {
    transform: scale(1.05);
  }
}

.step-icon {
  @include icon-medium;
  margin-bottom: $spacing-sm;
}

.flow-step h4 {
  font-size: $font-size-body-large;
  margin-bottom: $spacing-sm;
  color: $text-blue;
}

.flow-step p {
  @include caption-text;
}

.arrow {
  font-size: 36px;
  opacity: 0.6;
  margin: 0 $spacing-md;
}
</style>
