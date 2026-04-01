<template>
  <div class="ppt-container">
    <!-- 幻灯片内容 -->
    <div 
      v-for="(slideComponent, index) in slides" 
      :key="index"
      class="slide" 
      :class="{ 'active': currentSlide === index }"
    >
      <component :is="slideComponent" />
    </div>

    <!-- 导航控制 -->
    <div class="navigation-controls">
      <div class="slide-indicators">
        <span 
          v-for="(slide, index) in totalSlides" 
          :key="index"
          class="indicator"
          :class="{ active: currentSlide === index }"
          @click="goToSlide(index)"
        >{{slide}}</span>
      </div>
    </div>

    <!-- 进度条 -->
    <div class="progress-bar">
      <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
    </div>

    <!-- 退出提示（桌面端可用esc，不显示） -->
    <div class="exit-hint">
      <button class="exit-button" @click="goToDashboard" title="返回系统界面">
        ↩️
      </button>
    </div>
  </div>
</template>

<script>
import { markRaw } from 'vue'
import { slidesConfig } from '@/components/ppt'
import { pptState } from '@/utils/pptStateManager'

export default {
  name: 'PPTPresentation',
  data() {
    return {
      currentSlide: 0,
      slides: slidesConfig.map(slide => markRaw(slide.component))
    }
  },
  computed: {
    totalSlides() {
      return this.slides.length
    },
    progressPercentage() {
      return ((this.currentSlide + 1) / this.totalSlides) * 100
    }
  },
  mounted() {
    // 恢复保存的状态
    this.currentSlide = pptState.restoreState()
    // 监听键盘事件
    document.addEventListener('keydown', this.handleKeydown)
    // 监听页面可见性变化
    // document.addEventListener('visibilitychange', this.handleVisibilityChange)
    // 监听鼠标滚轮事件
    document.addEventListener('wheel', this.handleWheel, { passive: false })
  },
  beforeUnmount() {
    // 清理事件监听
    document.removeEventListener('keydown', this.handleKeydown)
    // document.removeEventListener('visibilitychange', this.handleVisibilityChange)
    document.removeEventListener('wheel', this.handleWheel)
  },
  methods: {
    // handleVisibilityChange() {
    //   // 当页面从隐藏变为可见时，确保焦点在正确位置
    //   if (document.visibilityState === 'visible') {
    //     // 可以在这里添加一些恢复逻辑
    //     console.log('PPT 页面已恢复可见')
    //   }
    // },
    handleKeydown(event) {
      // 如果页面不可见，不处理键盘事件
      if (document.hidden) {
        return
      }
      
      // ESC 键返回主界面
      if (event.key === 'Escape' || event.key === 'ArrowUp' || event.key === 'ArrowDown') {
        this.goToDashboard()
        return
      }
      
      // 左右箭头或空格键切换幻灯片
      if (event.key === 'ArrowRight' || event.key === ' ' || event.key === 'Enter') {
        this.nextSlide()
      } else if (event.key === 'ArrowLeft') {
        this.previousSlide()
      }
    },
    handleWheel(event) {
      // 如果页面不可见，不处理滚轮事件
      if (document.hidden) {
        return
      }
      
      // 阻止默认的滚动行为
      event.preventDefault()
      
      // 根据滚轮方向切换幻灯片
      if (event.deltaY > 0 || event.deltaX > 0) {
        // 向下或向右滚动 - 下一页
        this.nextSlide()
      } else if (event.deltaY < 0 || event.deltaX < 0) {
        // 向上或向左滚动 - 上一页
        this.previousSlide()
      }
    },
    nextSlide() {
      if (this.currentSlide < this.totalSlides - 1) {
        this.currentSlide++
        this.saveCurrentState()
      }
    },
    previousSlide() {
      if (this.currentSlide > 0) {
        this.currentSlide--
        this.saveCurrentState()
      }
    },
    goToSlide(index) {
      this.currentSlide = index
      this.saveCurrentState()
    },
    goToDashboard() {
      this.$router.push('/dashboard')
    },
    saveCurrentState() {
      // 保存当前幻灯片状态
      pptState.saveState(this.currentSlide)
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.ppt-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, $primary-gradient-start 0%, $primary-gradient-end 100%);
  overflow: hidden;
  position: relative;
}

.slide {
  display: none;
  width: 100%;
  height: 100%;
  padding: 30px 40px;
  @include fade-in;
  
  &.active {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  max-width: 1400px;
  margin: 0 auto;
  color: $text-white;
}

/* 导航控制 */
.navigation-controls {
  position: fixed;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 20px;
  z-index: 100;
}

.slide-indicators {
  display: flex;
  gap: 12px;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all $transition-fast;
  font-size: 8px;
  color: $text-white;
  display: flex;
  justify-content: center;
  align-items: center;

  
  &:hover {
    background: rgba(255, 255, 255, 0.5);
    transform: scale(1.2);
  }
  
  &.active {
    background: rgba(255, 255, 255, 0.8);
    width: 30px;
    border-radius: 6px;
    color: $text-grey;
  }
}

/* 进度条 */
.progress-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  z-index: 100;
  overflow: hidden;
}

.progress {
  height: 100%;
  border-radius: 0 999px 999px 0;
  /* 流动色彩渐变 */
  background: linear-gradient(
    45deg,
    #ededed,
    rgba(144, 147, 153, 0.4),
    #ededed,
  );
  background-size: 300% 100%;
  /* 应用流动动画 */
  animation: flowing-progress 5s linear infinite;
  transition: width $transition-fast;
}

/* 流动色彩动画 */
@keyframes flowing-progress {
  0% {
    background-position: 300% 50%;
  }
  100% {
    background-position: 30% 50%;
  }
}

@media (max-width: 768px) {
  .ppt-container {
    padding: 20px;
  }
  
  .slide {
    padding: 40px 20px;
  }

  /* 退出按钮 */
  .exit-hint {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 100;
  }

  .exit-button {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: white;
    font-size: 16px;
    padding: 6px 12px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .exit-button:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.05);
  }
}
</style>
