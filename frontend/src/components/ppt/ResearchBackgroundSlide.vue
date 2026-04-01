<template>
  <div class="slide-content">
    <h2 class="slide-title">研究背景与问题</h2>
    
    <!-- 导航按钮 -->
    <button class="nav-btn left" @click="prevSlide" :disabled="currentIndex === 0">
      <span>◀</span>
    </button>
    <button class="nav-btn right" @click="nextSlide" :disabled="currentIndex === totalSlides - 1">
      <span>▶</span>
    </button>
    
    <!-- 卡片容器 -->
    <div class="cards-container">
      <!-- 第一部分：重要性 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 0" class="card-section">
          <div class="info-card highlight">
            <div class="card-icon">📊</div>
            <h3>数据分析的重要性</h3>
            <p>大数据时代，数据分析已成为政府治理、商业决策、科学研究与工程实践的重要支撑手段</p>
          </div>
        </div>
      </transition>
      
      <!-- 第二部分：三个问题 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 1" class="card-section">
          <div class="info-card">
            <div class="card-problem">⚠️</div>
            <h3>非专业用户：门槛高</h3>
            <ul class="problem-list">
              <li>需要编程基础 + 统计学 + 机器学习知识</li>
              <li>分析流程复杂：数据读取→清洗→特征分析→建模→可视化→报告</li>
              <li>现有低代码工具仍依赖菜单配置，学习成本高</li>
            </ul>
          </div>
          <div class="info-card">
            <div class="card-problem">🔄</div>
            <h3>专业人员：重复劳动</h3>
            <ul class="problem-list">
              <li>大量时间消耗在探索性分析、调参、可视化等重复流程</li>
              <li>自动化程度有限，手动操作易引入额外成本</li>
            </ul>
          </div>
          <div class="info-card">
            <div class="card-problem">🧩</div>
            <h3>工具生态：碎片化</h3>
            <ul class="problem-list">
              <li>统计方法、机器学习、可视化工具分散在不同平台</li>
              <li>缺乏统一调度机制，依赖人工串联</li>
            </ul>
          </div>
        </div>
      </transition>
      
      <!-- 第三部分：解决方案 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 2" class="card-section">
          <div class="info-card question wide">
            <div class="card-icon">💡</div>
            <h3>LLM-Agent 带来的新机遇</h3>
            <p class="highlight-text">大语言模型的 Function Calling 能力使 Agent 能够承担决策角色</p>
            <p class="question-sub">构建以 LLM-Agent 为核心的自适应数据分析系统</p>
          </div>
        </div>
      </transition>
    </div>

  </div>
</template>

<script>
export default {
  name: 'ResearchBackgroundSlide',
  data() {
    return {
      currentIndex: 0,
      totalSlides: 3,
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

.info-card {
  @extend .info-card;
  width: 300px;
  height: 300px;
  
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

.highlight-text {
  @extend .highlight-text;
}

.question-sub {
  @extend .question-sub;
}

// 卡片容器
.cards-container {
  position: relative;
  width: 100%;
  height: 500px;
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
  gap: 20px;
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
    color: $text-blue;
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
</style>
