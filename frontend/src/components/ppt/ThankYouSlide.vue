<template>
  <div class="slide-content title-slide">
    <h1 class="title">感谢观看</h1>
    <p class="subtitle">Q & A</p>
    <div class="contact-info">
      <p>欢迎提问与交流！</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ThankYouSlide'
}
</script>

<style scoped lang="scss">
@use '@/components/ppt/styles' as *;

.title-slide {
  text-align: center;
}

.title {
  @include title-text;
  margin-bottom: $spacing-huge;
}

.subtitle {
  @include subtitle-text;
  margin-bottom: $spacing-huge;
}

.contact-info {
  margin-top: $spacing-huge;
  font-size: $font-size-presenter;
}
</style>
