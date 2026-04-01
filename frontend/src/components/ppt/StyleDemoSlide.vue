<template>
  <div class="slide-content">
    <h2 class="slide-title">PPT 样式系统演示</h2>
    
    <!-- 卡片类型演示 -->
    <div class="content-grid">
      <div class="info-card">
        <div class="icon-large">📊</div>
        <h3>默认卡片</h3>
        <p>标准的信息卡片样式</p>
      </div>
      
      <div class="info-card highlight">
        <div class="icon-large">✨</div>
        <h3>高亮卡片</h3>
        <p>用于强调重要内容</p>
      </div>
      
      <div class="info-card question">
        <div class="icon-large">❓</div>
        <h3>问题卡片</h3>
        <p>用于提出问题或思考</p>
      </div>
    </div>
    
    <!-- 工具盒子演示 -->
    <div class="tools-grid" style="margin-top: 30px;">
      <div class="tool-box">
        <div class="icon-small">🔧</div>
        <p>工具一</p>
      </div>
      <div class="tool-box">
        <div class="icon-small">⚙️</div>
        <p>工具二</p>
      </div>
      <div class="tool-box">
        <div class="icon-small">🎯</div>
        <p>工具三</p>
      </div>
      <div class="tool-box">
        <div class="icon-small">📈</div>
        <p>工具四</p>
      </div>
    </div>
    
    <!-- 模块卡片演示 -->
    <div class="modules-description">
      <div class="module-card">
        <h4>模块 A</h4>
        <p>功能描述文字</p>
      </div>
      <div class="module-card">
        <h4>模块 B</h4>
        <p>功能描述文字</p>
      </div>
      <div class="module-card">
        <h4>模块 C</h4>
        <p>功能描述文字</p>
      </div>
      <div class="module-card">
        <h4>模块 D</h4>
        <p>功能描述文字</p>
      </div>
    </div>
    
    <!-- 列表样式演示 -->
    <div style="margin-top: 30px; max-width: 600px; margin-left: auto; margin-right: auto;">
      <h3 style="text-align: center; margin-bottom: 15px;">列表样式示例</h3>
      <ul class="problem-list">
        <li>第一点内容说明</li>
        <li>第二点内容说明</li>
        <li>第三点内容说明</li>
      </ul>
    </div>
    
    <!-- 问题文本演示 -->
    <div style="text-align: center; margin-top: 20px;">
      <p class="question-text">这是一个问题文本示例</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StyleDemoSlide'
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

.tools-grid {
  @extend .tools-grid;
}

.tool-box {
  @extend .tool-box;
}

.modules-description {
  @extend .modules-description;
}

.module-card {
  @extend .module-card;
}

.problem-list {
  @extend .problem-list;
}

.question-text {
  @extend .question-text;
}
</style>
