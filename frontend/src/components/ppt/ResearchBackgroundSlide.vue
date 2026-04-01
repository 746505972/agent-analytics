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
      
      <!-- 第三部分：现有解决方案不足 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 2" class="card-section">
          <div class="info-card large-size">
            <div class="card-problem">📛</div>
            <h3>传统数据分析工具的不足</h3>
            <p class="highlight-text">核心局限：操作驱动、缺乏智能化</p>
            <ul class="problem-list">
              <li><strong>高使用门槛：</strong>依赖用户具备统计学知识与分析经验，需手动选择方法、配置参数，难以支持从问题到结果的全流程自动化</li>
              <li><strong>缺乏流程建模能力：</strong>以"单次分析任务"为单位，难以支持多步骤、复杂分析任务的整体建模与管理</li>
              <li><strong>交互与解释能力弱：</strong>无法理解自然语言，问题表达与操作转换成本高；结果缺乏自动化解释与报告生成，不利于非专业用户理解业务意义</li>
            </ul>
          </div>
          <div class="info-card large-size">
            <div class="card-problem">🤖</div>
            <h3>自动化机器学习（AutoML）的局限</h3>
            <p class="highlight-text">核心局限：模型中心、忽略分析全过程</p>
            <ul class="problem-list">
              <li><strong>对数据预处理支持不足：</strong>多数系统假设数据已清洗，缺乏对数据质量与理解环节的关注</li>
              <li><strong>优化目标单一：</strong>以预测性能为核心，难以融合具体业务语义与动态分析意图</li>
              <li><strong>可解释性有限：</strong>虽引入部分解释技术，但整体缺乏对分析过程的系统性说明与结果解释能力，难以实现"自动分析"而非仅"自动建模"</li>
            </ul>
          </div>
          <div class="info-card large-size">
            <div class="card-problem">💻</div>
            <h3>编程环境数据分析方式的不足</h3>
            <p class="highlight-text">核心局限：代码依赖、语义鸿沟</p>
            <ul class="problem-list">
              <li><strong>技术门槛高：</strong>要求用户具备编程能力与算法基础，需手动实现数据处理、建模、调试等各环节，自动化程度低</li>
              <li><strong>语义表达困难：</strong>分析意图需转换为具体代码，问题定义与实现过程存在鸿沟，不利于分析经验的复用与共享</li>
              <li><strong>结果表达不友好：</strong>缺乏自动化解释机制，分析逻辑隐含在代码中，对非专业用户不友好，难以形成标准化、可复现的分析流程</li>
            </ul>
          </div>
        </div>
      </transition>

      <!-- 第四部分：大语言模型的新进展 -->
      <transition :name="slideDirection">
        <div v-if="currentIndex === 3" class="card-section">
          <div class="info-card question wide-card">
            <div class="card-icon">💡</div>
            <h3>大语言模型带来的新进展</h3>
            <p class="question-text">
            大语言模型的 Function Calling 能力，使其具备调用外部工具的能力
            </p>
            <ul class="problem-list">
              <li>能够理解自然语言分析需求</li>
              <li>可以在一定程度上执行分析任务</li>
              <li>已有系统尝试用于数据分析场景</li>
            </ul>
            <p class="question-sub">
            但仍存在流程不可控、分析路径不清晰等问题
            </p>
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
      totalSlides: 4,
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
  width: 380px;
  height: 300px;
  
  h3 {
    @extend h3;
  }
  
  p {
    @extend p;
  }
}

.info-card.large-size {
  width: 500px;
  height: 400px;
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
