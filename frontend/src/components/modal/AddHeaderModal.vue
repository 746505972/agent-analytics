<template>
  <div class="add-header-modal">
    <div class="add-header-modal-content">
      <div class="add-header-modal-header">
        <h3>添加标题行</h3>
        <button class="close-button" @click="closeModal">×</button>
      </div>
      <div class="add-header-modal-body">
        <p>正在为文件添加标题行，请稍候...</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddHeaderModal",
  emits: ['close'],
  methods: {
    closeModal() {
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
/* 添加标题行弹窗样式 */
.add-header-modal {
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

.add-header-modal-content {
  background: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  padding: 20px;
}

.add-header-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.add-header-modal-header h3 {
  margin: 0;
  color: #303133;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
}

.add-header-modal-body {
  text-align: center;
  padding: 20px 0;
}
</style>