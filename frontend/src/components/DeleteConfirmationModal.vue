<template>
  <div class="danger-window" v-if="visible">
    <div class="danger-box">
      <div class="top-header">
        <h2>提示</h2>
        <button class="icon-button inputno" @click="cancelDelete"></button>
      </div>
      <div class="ml36">
        <h3 class="warning">是否确定删除？</h3>
        <p>数据删除后不能恢复，请确认！</p>
      </div>
      <div>
        <button class="red-button inputyes" @click="confirmDelete">删除</button>
        <button class="noborder-button inputno" @click="cancelDelete">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeleteConfirmationModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    confirmDelete() {
      this.$emit('confirm');
    },
    cancelDelete() {
      this.$emit('cancel');
    }
  }
}
</script>

<style scoped>
.danger-window {
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

.danger-box {
  background: white;
  border-radius: 6px;
  width: 350px;
  padding: 15px;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.top-header h2 {
  font-size: 16px;
  color: #303133;
}

.icon-button {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #909399;
}

.ml36 {
  margin-left: 30px;
  margin-bottom: 15px;
}

.ml36 .warning {
  color: #e6a23c;
  font-size: 14px;
  margin-bottom: 8px;
}

.ml36 p {
  color: #606266;
  font-size: 13px;
}

.red-button {
  padding: 8px 16px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 8px;
  font-size: 13px;
}

.red-button:hover {
  background-color: #f78989;
}

.noborder-button {
  padding: 8px 16px;
  background: none;
  color: #606266;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
}

.noborder-button:hover {
  color: #409eff;
}
</style>