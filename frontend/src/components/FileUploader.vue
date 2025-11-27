<template>
  <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
    <div class="upload-content">
      <form id="upload-form">
        <img src="../assets/images/upload-icon.svg" alt="上传图标" class="upload-icon">
        <div class="upload-text">
          点击上传或将文件拖拽到这里上传
        </div>
      </form>
      <input
        id="file-input"
        class="file-input"
        type="file"
        name="dataFile"
        @change="handleFileSelect"
        accept=".csv,.xls,.xlsx"
      >
      <div class="upload-hint">
        <span>支持xls、xlsx、csv文件</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileUploader',
  emits: ['file-selected'],
  methods: {
    triggerFileInput() {
      document.getElementById('file-input').click()
    },

    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.$emit('file-selected', file)
      }
    },

    handleDrop(event) {
      const file = event.dataTransfer.files[0]
      if (file) {
        // 检查文件类型
        const allowedTypes = [
          'text/csv',
          'application/vnd.ms-excel',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'application/octet-stream'
        ]

        if (allowedTypes.includes(file.type) || this.isValidFileType(file.name)) {
          this.$emit('file-selected', file)
        } else {
          // 传递错误信息
          this.$emit('file-error', '不支持的文件类型，请上传正确的数据文件')
        }
      }
    },

    isValidFileType(filename) {
      // Todo: 添加更多文件类型检查
      const extensions = ['.csv', '.xls', '.xlsx']
      return extensions.some(ext => filename.toLowerCase().endsWith(ext))
    }
  }
}
</script>

<style scoped>
.upload-area {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
  background: rgba(122, 204, 233, 0.09);
}

.upload-area:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.1);
}

.upload-content {
  text-align: center;
}

.upload-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 20px;
}

.upload-text {
  color: #409eff;
  font-size: 18px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.upload-area:hover .upload-text {
  color: #66b1ff;
}

.file-input {
  display: none;
}

.upload-hint {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  color: #909399;
  font-size: 14px;
}

.upload-hint a {
  color: #409eff;
  text-decoration: none;
}

.upload-hint a:hover {
  text-decoration: underline;
}
</style>