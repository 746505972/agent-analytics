<template>
  <div class="slide-content">
    <h2 class="slide-title">实验与效果分析</h2>
    
    <!-- 导航按钮 -->
    <button class="nav-btn left" @click="prevSlide" :disabled="currentIndex === 0">
      <span>◀</span>
    </button>
    <button class="nav-btn right" @click="nextSlide" :disabled="currentIndex === totalSlides - 1">
      <span>▶</span>
    </button>
    
    <!-- 卡片容器 -->
    <div class="cards-container">
      <!-- 第一部分：对比表格 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 0" class="card-section">
          <div class="comparison-table">
            <div class="table-header">
              <div class="header-cell empty"></div>
              <div class="header-cell highlight">传统 Python 分析流程</div>
              <div class="header-cell success">本系统（LLM-Agent）</div>
            </div>
            
            <div class="table-row">
              <div class="cell label">总耗时</div>
              <div class="cell traditional">20+ 分钟<br><small>环境配置、编码、调试</small></div>
              <div class="cell our-system success">< 5 分钟<br><small>自然语言交互</small></div>
            </div>
            
            <div class="table-row">
              <div class="cell label">操作步骤</div>
              <div class="cell traditional">繁琐<br><small>多工具切换，手动编码</small></div>
              <div class="cell our-system success">简化<br><small>自动化执行</small></div>
            </div>
            
            <div class="table-row">
              <div class="cell label">认知负担</div>
              <div class="cell traditional">高<br><small>需编程与统计知识</small></div>
              <div class="cell our-system success">低<br><small>零代码基础</small></div>
            </div>
            
            <div class="table-row">
              <div class="cell label">自动化程度</div>
              <div class="cell traditional">低<br><small>人工规划全流程</small></div>
              <div class="cell our-system success">高<br><small>Agent 自主决策</small></div>
            </div>
          </div>
        </div>
      </transition>
      
      <!-- 第二部分：关键指标 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 1" class="card-section">
          <div class="metrics">
<!--            <h3>关键指标提升</h3>-->
            <div class="metrics-grid">
              <div class="metric-item">
                <div class="percentage">⬇️ 75%</div>
                <p>时间成本降低</p>
                <small class="metric-detail">20min → &lt;5min</small>
              </div>
              
              <div class="metric-item">
                <div class="percentage">⬆️ 4x</div>
                <p>分析效率提升</p>
                <small class="metric-detail">自动化执行</small>
              </div>
              
              <div class="metric-item">
                <div class="percentage">✅ 100%</div>
                <p>零代码要求</p>
                <small class="metric-detail">自然语言交互</small>
              </div>
            </div>
            
            <div class="workflow-timeline">
              <h4>完整分析流程（&lt;5分钟）</h4>
              <div class="timeline-steps">
                <div class="step">
                  <span class="step-time">30s</span>
                  <p>上传数据文件</p>
                </div>
                <div class="step">
                  <span class="step-time">~1min</span>
                  <p>自动识别缺失值与分布问题</p>
                </div>
                <div class="step">
                  <span class="step-time">自动</span>
                  <p>中位数插值清洗</p>
                </div>
                <div class="step">
                  <span class="step-time">40s</span>
                  <p>XGBoost建模+特征排序</p>
                </div>
                <div class="step">
                  <span class="step-time">手动</span>
                  <p>生成结构化报告</p>
                </div>
              </div>
            </div>
            
            <div class="cost-info">
              <p>💡 Token消耗：约200K（qwen-plus模型），处于可接受范围</p>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExperimentsSlide',
  data() {
    return {
      currentIndex: 0,
      totalSlides: 2,
      slideDirection: 'slide-next'
    }
  },
  methods: {
    nextSlide() {
      if (this.currentIndex < this.totalSlides - 1) {
        this.slideDirection = 'slide-next'
        this.currentIndex++
      }
    },
    prevSlide() {
      if (this.currentIndex > 0) {
        this.slideDirection = 'slide-prev'
        this.currentIndex--
      }
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.slide-title {
  @extend .slide-title;
}

// 卡片容器
.cards-container {
  position: relative;
  width: 100%;
  height: 600px;
  margin-top: 40px;
}

// 卡片区域
.card-section {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

// 导航按钮
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(79, 164, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(79, 164, 255, 0.4);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
  
  span {
    font-size: 24px;
    color: #4fa4ff;
    font-weight: bold;
  }
  
  &:hover:not(:disabled) {
    background: rgba(79, 164, 255, 0.4);
    transform: translateY(-50%) scale(1.1);
  }
  
  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
  
  &.left {
    left: 20px;
  }
  
  &.right {
    right: 20px;
  }
}

// 切换动画 - 向右滑动（下一页）
.slide-next-enter-active,
.slide-next-leave-active {
  transition: all 0.5s ease;
  position: absolute;
  width: 100%;
}

.slide-next-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.slide-next-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

// 切换动画 - 向左滑动（上一页）
.slide-prev-enter-active,
.slide-prev-leave-active {
  transition: all 0.5s ease;
  position: absolute;
  width: 100%;
}

.slide-prev-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}

.slide-prev-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.comparison-table {
  margin-bottom: $spacing-xxl + 5px;
  border-radius: $border-radius-lg;
  overflow: hidden;
  border: 2px solid $card-border-default;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 3fr 3fr;
  background: rgba(255, 255, 255, 0.15);
}

.header-cell {
  padding: $spacing-md;
  font-size: $font-size-heading - 2px;
  font-weight: bold;
  text-align: center;
  border-right: 1px solid $card-border-light;
}

.header-cell.empty {
  background: transparent;
}

.header-cell.highlight {
  background: rgba(239, 68, 68, 0.3);
}

.header-cell.success {
  background: rgba(34, 197, 94, 0.3);
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 3fr 3fr;
  border-bottom: 1px solid $card-border-light;
}

.table-row:last-child {
  border-bottom: none;
}

.cell {
  padding: $spacing-lg;
  text-align: center;
  border-right: 1px solid $card-border-light;
}

.cell.label {
  font-weight: bold;
  font-size: $font-size-heading - 2px;
  background: rgba(255, 255, 255, 0.05);
}

.cell.traditional {
  background: rgba(239, 68, 68, 0.1);
}

.cell.our-system {
  background: rgba(34, 197, 94, 0.1);
}

.cell.success {
  color: #4ade80;
  font-weight: bold;
}

.cell small {
  font-size: $font-size-body-small;
  opacity: 0.8;
  font-weight: normal;
}

.metrics {
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-xl;
  padding: $spacing-xxl $spacing-xxl + 5px;
  border: 2px solid $card-border-default;
}

.metrics h3 {
  font-size: $font-size-heading + 10px;
  margin-bottom: $spacing-xl - 2px;
  text-align: center;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-xl;
}

.metric-item {
  text-align: center;
  background: $card-bg-default;
  backdrop-filter: $backdrop-blur;
  border-radius: $border-radius-lg;
  padding: $spacing-md - 2px;
  border: 2px solid $card-border-default;
  transition: all $transition-fast;
  
  &:hover {
    transform: scale(1.05);
    background: $card-bg-hover;
  }
}

.percentage {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: $spacing-md;
}

.metric-item p {
  font-size: $font-size-body-large;
  opacity: 0.9;
}

.metric-detail {
  display: block;
  font-size: $font-size-body-small;
  opacity: 0.7;
  margin-top: $spacing-sm;
}

.workflow-timeline {
  margin-top: $spacing-xl;
  padding: $spacing-lg;
  background: rgba(255, 255, 255, 0.05);
  border-radius: $border-radius-lg;
  border: 1px solid $card-border-light;
}

.workflow-timeline h4 {
  font-size: $font-size-heading;
  margin-bottom: $spacing-md;
  text-align: center;
  color: #60a5fa;
}

.timeline-steps {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: $spacing-md;
}

.step {
  text-align: center;
  padding: $spacing-md;
  background: rgba(255, 255, 255, 0.08);
  border-radius: $border-radius-md;
  transition: all $transition-fast;
  
  &:hover {
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.12);
  }
}

.step-time {
  display: block;
  font-size: $font-size-heading - 4px;
  font-weight: bold;
  color: #fbbf24;
  margin-bottom: $spacing-sm;
}

.step p {
  font-size: $font-size-body-small;
  line-height: 1.4;
}

.cost-info {
  margin-top: $spacing-lg;
  padding: $spacing-md;
  background: rgba(96, 165, 250, 0.1);
  border-radius: $border-radius-md;
  border-left: 4px solid #60a5fa;
  
  p {
    font-size: $font-size-body;
    margin: 0;
    text-align: center;
  }
}
</style>
