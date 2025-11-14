<template>
  <div class="upload-container">
    <div class="indexheader">
      <div class="inner">
        <div class="header-left">
          <router-link to="/dashboard" class="back-link">
            <span>返回</span>
          </router-link>
        </div>
        <div class="header-right">
          <router-link class="hollow-button" to="/analysis">
            进入分析
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="upload-box">
      <div class="upload-steps">
        <div class="step-item active-step">
          <span>1</span>
          上传文件
        </div>
        <hr>
        <div class="step-item">
          <span>2</span>
          数据预览
        </div>
      </div>
      
      <div class="upload-section">
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
              accept=".csv,.xls,.xlsx,.sav,.dta,.sas7bdat"
            >
            <div class="upload-hint">
              <span>支持xls、xlsx、csv文件</span>
            </div>
          </div>
        </div>

        <ul class="upload-instructions">
          <li>
            <h3>导入说明：</h3>
          </li>
          <li>不含合并单元格</li>
          <li>不能缺失标题行</li>
          <li>日期字段需包含年月日（如2021/1/1），或年月日时分秒（如2021/1/1 00:00:00）</li>
        </ul>
      </div>

      <div class="example-section">
        <h2>
          <img src="../assets/images/table-icon.svg" alt="表格图标">
          表格示例
        </h2>
        <div class="example-table-container">
          <table class="example-table">
            <thead>
              <tr>
                <th>编号</th>
                <th>性别</th>
                <th>年龄</th>
                <th>学历</th>
                <th>年收入</th>
                <th>日期</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>1</td>
                <td>32</td>
                <td>本科</td>
                <td>2</td>
                <td>2021/8/12</td>
              </tr>
              <tr>
                <td>2</td>
                <td>1</td>
                <td>28</td>
                <td>硕士</td>
                <td>3</td>
                <td>2021/8/13</td>
              </tr>
              <tr>
                <td>3</td>
                <td>2</td>
                <td>35</td>
                <td>本科</td>
                <td>4</td>
                <td>2021/8/14</td>
              </tr>
              <tr>
                <td>4</td>
                <td>2</td>
                <td>40</td>
                <td>博士</td>
                <td>5</td>
                <td>2021/8/15</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">文件上传中...</div>
    </div>

    <div v-if="uploadError" class="error-overlay">
      <div class="error-message">
        <h3>上传失败</h3>
        <p>{{ uploadError }}</p>
        <button @click="clearError">确定</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Upload',
  data() {
    return {
      isLoading: false,
      selectedFile: null,
      uploadError: null
    }
  },
  methods: {
    triggerFileInput() {
      document.getElementById('file-input').click()
    },

    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
        this.uploadFile(file)
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
          this.selectedFile = file
          this.uploadFile(file)
        } else {
          this.uploadError = '不支持的文件类型，请上传正确的数据文件'
        }
      }
    },

    isValidFileType(filename) {
      // Todo: 添加更多文件类型检查
      const extensions = ['.csv', '.xls', '.xlsx']
      return extensions.some(ext => filename.toLowerCase().endsWith(ext))
    },

    async uploadFile(file) {
      // 文件大小检查 (100MB)
      if (file.size > 100 * 1024 * 1024) {
        this.uploadError = '文件大小超过100MB限制'
        return
      }

      this.isLoading = true
      this.uploadError = null

      try {
        // 创建 FormData 对象
        const formData = new FormData()
        formData.append('file', file)

        // 发送文件到后端
        const response = await fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData
        })

        const result = await response.json()

        if (result.success) {
          // 保存 data_id 到本地存储
          localStorage.setItem('currentDataId', result.data.data_id)

          // 上传完成后跳转到数据预览页面
          this.$router.push({
            path: '/preview',
            query: { dataId: result.data.data_id }
          })
        } else {
          this.uploadError = result.error || '上传失败'
        }
      } catch (error) {
        console.error('上传文件时出错:', error)
        this.uploadError = '网络错误，请检查后端服务是否运行'
      } finally {
        this.isLoading = false
      }
    },

    clearError() {
      this.uploadError = null
    }
  }
}
</script>

<style scoped>
.upload-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.indexheader {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 15px 0;
}

.inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left .back-link {
  text-decoration: none;
  color: #333;
  font-size: 16px;
}

.header-right .hollow-button {
  display: inline-block;
  padding: 8px 16px;
  border: 1px solid #409eff;
  color: #409eff;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
}

.header-right .hollow-button:hover {
  background-color: #409eff;
  color: white;
}

.upload-box {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}

.upload-steps {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.step-item {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #909399;
}

.step-item.active-step {
  color: #409eff;
}

.step-item span {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f5f5f5;
  margin-right: 10px;
  font-weight: bold;
}

.step-item.active-step span {
  background-color: #409eff;
  color: white;
}

.upload-steps hr {
  flex: 1;
  margin: 0 20px;
  border: none;
  height: 1px;
  background-color: #ebeef5;
}

.upload-section {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

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

.upload-instructions {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  list-style: none;
}

.upload-instructions li {
  padding: 5px 0;
  color: #606266;
  line-height: 1.6;
}

.upload-instructions h3 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 18px;
}

.example-section h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  color: #303133;
  margin-bottom: 20px;
}

.example-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  overflow-x: auto;
}

.example-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.example-table th,
.example-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.example-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #606266;
}

.example-table tbody tr:hover {
  background-color: #f5f7fa;
}

.loading-overlay {
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

.loading-spinner {
  width: 50px;
  height: 50px;
  color: white;
  font-size: 16px;
}

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

.error-message h3 {
  color: #f56c6c;
  margin-bottom: 15px;
}

.error-message p {
  color: #606266;
  margin-bottom: 20px;
}

.error-message button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .upload-section {
    flex-direction: column;
  }
  
  .inner {
    flex-direction: column;
    gap: 15px;
  }
  
  .upload-steps {
    flex-direction: column;
    gap: 15px;
  }
  
  .upload-steps hr {
    width: 100%;
  }
  
  .example-table {
    font-size: 12px;
  }
  
  .example-table th,
  .example-table td {
    padding: 8px 10px;
  }
}
</style>