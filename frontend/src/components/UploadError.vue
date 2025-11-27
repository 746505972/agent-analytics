<template>
  <div class="error-overlay">
    <div class="error-message">
      <div class="error-header">
        <slot name="header">
          <h3>上传失败</h3>
        </slot>
      </div>
      
      <div class="error-content">
        <slot name="content">
          <p><slot></slot></p>
        </slot>
      </div>
      
      <div class="error-footer">
        <slot name="footer">
          <button @click="$emit('close')">确定</button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UploadError",
  emits: ['close']
}
</script>

<style scoped>
.error-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.error-message {
  background: white;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  max-width: 400px;
}

.error-header h3 {
  color: #f56c6c;
  margin-bottom: 15px;
}

.error-content p {
  color: #606266;
  margin-bottom: 20px;
}

.error-footer button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>