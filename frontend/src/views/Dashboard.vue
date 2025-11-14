<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>欢迎使用 Agent-Analytics 智能数据分析平台</h2>
    </div>
    
    <div class="dashboard-content">
      <!-- 左侧：文件选择区域 -->
      <div class="file-selection-section">
        <h2>选择分析文件</h2>
        <div class="file-list-container">
          <div v-if="files.length === 0" class="no-files">
            暂无上传文件，请先上传文件
          </div>
          <div v-else class="file-list">
            <div 
              v-for="file in files" 
              :key="file.data_id"
              class="file-item"
              :class="{ selected: selectedFile === file.data_id }"
              @click="selectFile(file.data_id)"
            >
              <div class="file-name">{{ file.filename }}</div>
              <div class="file-info">
                <span>行数: {{ file.rows }}</span>
                <span>列数: {{ file.columns }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="file-actions">
          <router-link to="/upload" class="upload-button">上传新文件</router-link>
        </div>
      </div>
      
      <!-- 右侧：聊天分析区域 -->
      <div class="chat-section">
        <h2>数据分析助手</h2>
        <div class="chat-box">
          <div class="messages">
            <div 
              v-for="(message, index) in chatMessages" 
              :key="index"
              class="message"
              :class="message.type"
            >
              {{ message.content }}
            </div>
          </div>
          <div class="input-area">
            <input 
              type="text" 
              placeholder="输入您的分析需求..." 
              v-model="userInput"
              @keyup.enter="sendMessage"
              :disabled="!selectedFile"
            />
            <button @click="sendMessage" :disabled="!selectedFile">发送</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      files: [],
      selectedFile: null,
      userInput: "",
      chatMessages: [
        {
          type: "received",
          content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
        }
      ]
    }
  },
  async mounted() {
    await this.loadUploadedFiles();
  },
  methods: {
    async loadUploadedFiles() {
      // 调用后端API获取用户上传的文件列表
      try {
        const response = await fetch('http://localhost:8000/user/files', {
          credentials: 'include' // 包含cookies，用于session管理
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            this.files = result.data;
          } else {
            console.error("获取文件列表失败:", result.error);
          }
        } else {
          console.error("获取文件列表失败，状态码:", response.status);
        }
      } catch (error) {
        console.error("加载文件列表失败:", error);
      }
    },
    
    selectFile(fileId) {
      this.selectedFile = fileId;
      // 可以在这里添加选中文件后的操作
    },
    
    sendMessage() {
      if (this.userInput.trim() !== "" && this.selectedFile) {
        // 添加用户消息到聊天记录
        this.chatMessages.push({
          type: "sent",
          content: this.userInput
        });
        
        // 这里应该调用后端API处理用户消息
        // 模拟回复
        setTimeout(() => {
          this.chatMessages.push({
            type: "received",
            content: `已收到您的分析请求: "${this.userInput}"。正在分析文件 "${this.getSelectedFileName()}"...`
          });
        }, 500);
        
        this.userInput = "";
      }
    },
    
    getSelectedFileName() {
      const file = this.files.find(f => f.data_id === this.selectedFile);
      return file ? file.filename : "";
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #303133;
  margin-bottom: 10px;
}

.dashboard-header p {
  color: #606266;
  font-size: 16px;
}

.dashboard-content {
  display: flex;
  gap: 30px;
}

.file-selection-section {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.file-selection-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
}

.file-list-container {
  min-height: 300px;
}

.no-files {
  text-align: center;
  color: #909399;
  padding: 40px 20px;
}

.file-list {
  max-height: 350px;
  overflow-y: auto;
}

.file-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.file-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 6px 0 rgba(64, 158, 255, 0.2);
}

.file-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.file-name {
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.file-info {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #909399;
}

.file-actions {
  margin-top: 20px;
  text-align: center;
}

.upload-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #66b1ff;
}

.chat-section {
  flex: 2;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chat-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
}

.chat-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  height: 500px;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 4px;
  max-width: 80%;
}

.message.sent {
  background-color: #409eff;
  color: white;
  margin-left: auto;
}

.message.received {
  background-color: #f5f5f5;
  color: #303133;
}

.input-area {
  display: flex;
  padding: 20px;
  border-top: 1px solid #ddd;
}

.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.input-area input:disabled {
  background-color: #f5f7fa;
  cursor: not-allowed;
}

.input-area button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-area button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .dashboard-content {
    flex-direction: column;
  }
  
  .file-selection-section,
  .chat-section {
    width: 100%;
  }
}
</style>