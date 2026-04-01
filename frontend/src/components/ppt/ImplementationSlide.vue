<template>
  <div class="slide-content">
    <h2 class="slide-title">系统实现与界面展示</h2>
    <div class="showcase-container">
      <div class="feature-grid">
        <div class="feature-item">
          <div class="screenshot-placeholder">
            <div class="icon">💬</div>
            <p>智能对话界面</p>
          </div>
          <p class="desc">自然语言交互，零门槛使用</p>
        </div>
        
        <div class="feature-item">
          <div class="screenshot-placeholder">
            <div class="icon">⚙️</div>
            <p>分析过程可视化</p>
          </div>
          <p class="desc">实时显示 Agent 思考和执行步骤</p>
        </div>
        
        <div class="feature-item">
          <div class="screenshot-placeholder">
            <div class="icon">📊</div>
            <p>分析结果展示</p>
          </div>
          <p class="desc">图表、统计数据直观呈现</p>
        </div>
        
        <div class="feature-item">
          <div class="screenshot-placeholder">
            <div class="icon">📝</div>
            <p>自动化报告</p>
          </div>
          <p class="desc">一键生成结构化分析报告</p>
        </div>
      </div>
      
      <div class="tech-stack">
        <h3>技术栈</h3>
        <div class="stack-grid">
          <div class="stack-item">
            <span class="badge backend">后端</span>
            <p>Python · FastAPI · LangChain · Pandas · Scikit-learn</p>
          </div>
          <div class="stack-item">
            <span class="badge frontend">前端</span>
            <p>Vue.js · Vite · ECharts</p>
          </div>
          <div class="stack-item">
            <span class="badge ai">AI</span>
            <p>LLM Agent · Function Calling</p>
          </div>
          <div class="stack-item">
            <span class="badge desktop">桌面端</span>
            <p>Electron</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImplementationSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

.showcase-container {
  max-width: 1200px;
  margin: 0 auto;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-xl;
  margin-bottom: $spacing-xxl + 5px;
}

.feature-item {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-xl - 2px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateY(-8px);
    background: $card-bg-hover;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.screenshot-placeholder {
  background: rgba(255, 255, 255, 0.15);
  border-radius: $border-radius-md;
  padding: $spacing-xxl $spacing-lg;
  text-align: center;
  margin-bottom: $spacing-lg;
  border: 2px dashed $card-border-light;
}

.screenshot-placeholder .icon {
  @include icon-large;
  margin-bottom: $spacing-md;
}

.screenshot-placeholder p {
  font-size: $font-size-body-large;
  font-weight: bold;
}

.feature-item .desc {
  @include caption-text;
  text-align: center;
}

.tech-stack {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xxl $spacing-xxl + 5px;
  border: 2px solid $card-border-default;
}

.tech-stack h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
}

.stack-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-lg;
}

.stack-item {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-md;
  padding: $spacing-lg $spacing-xl - 2px;
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  border: 1px solid $card-border-light;
}

.badge {
  display: inline-block;
  padding: $spacing-xs $spacing-sm;
  border-radius: 20px;
  font-size: $font-size-body-small;
  font-weight: bold;
  min-width: 70px;
  text-align: center;
  
  &.backend {
    background: linear-gradient(135deg, $primary-gradient-start, $primary-gradient-end);
    color: $text-white;
  }
  
  &.frontend {
    background: linear-gradient(135deg, #f093fb, #f5576c);
    color: $text-white;
  }
  
  &.ai {
    background: linear-gradient(135deg, #4facfe, #00f2fe);
    color: $text-white;
  }
  
  &.desktop {
    background: linear-gradient(135deg, #43e97b, #38f9d7);
    color: $text-white;
  }
}

.stack-item p {
  font-size: $font-size-body;
  flex: 1;
}
</style>
