<template>
  <div class="slide-content title-slide">
    <h1 class="title">基于 Agent 的数据分析与报告系统</h1>
    <p class="subtitle">Agent Analytics Platform</p>
    <div class="presenter-info">
      <p class="presenter">演示者：</p>
      <p class="date">{{ currentDate }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TitleSlide',
  data() {
    return {
      currentDate: new Date().toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.title-slide {
  text-align: center;
}
</style>
