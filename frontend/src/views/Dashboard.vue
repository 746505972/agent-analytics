<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>欢迎使用 Agent-Analytics 智能数据分析平台</h2>
    </div>
    
    <div class="dashboard-content">
      <!-- 左侧：文件选择区域 -->
      <div class="file-selection-section">
        <div class="section-header" @click="toggleFileSection">
          <h2>选择分析文件</h2>
          <span class="toggle-icon">{{ isFileSectionCollapsed ? '+' : '-' }}</span>
        </div>
        
        <div v-show="!isFileSectionCollapsed" class="file-section-content">
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
                <div class="file-name">
                  {{ file.filename }}
                  <span class="delete-file" @click.stop="deleteFile(file.data_id)">×</span>
                </div>
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
      </div>
      
      <!-- 左侧：列名显示区域 -->
      <div v-if="selectedFile && selectedFileColumns.length > 0" class="column-list-section">
        <h3>列名列表</h3>
        <ul class="column-list">
          <li v-for="(column, index) in selectedFileColumns" :key="index" class="column-item">
            {{ column }}
          </li>
        </ul>
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
              <span v-if="message.type === 'received' && message.content === '' && isWaitingForResponse" class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </span>
              <span v-else>{{ message.content }}</span>
            </div>
          </div>
          <div class="input-area">
            <input 
              type="text" 
              placeholder="输入您的分析需求..." 
              v-model="userInput"
              @keyup.enter="sendMessage"
              :disabled="!selectedFile || isWaitingForResponse"
            />
            <button @click="sendMessage" :disabled="!selectedFile || isWaitingForResponse">发送</button>
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
      selectedFileColumns: [],
      userInput: "",
      chatMessages: [
        {
          type: "received",
          content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
        }
      ],
      isFileSectionCollapsed: false,
      isWaitingForResponse: false
    }
  },
  async mounted() {
    await this.loadUploadedFiles();
  },
  methods: {
    toggleFileSection() {
      this.isFileSectionCollapsed = !this.isFileSectionCollapsed;
    },
    
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
    
    async deleteFile(fileId) {
      if (!confirm('确定要删除这个文件吗？')) {
        return;
      }
      
      try {
        const response = await fetch(`http://localhost:8000/data/${fileId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            // 从文件列表中移除已删除的文件
            this.files = this.files.filter(file => file.data_id !== fileId);
            
            // 如果删除的是当前选中的文件，清空选中状态和列名
            if (this.selectedFile === fileId) {
              this.selectedFile = null;
              this.selectedFileColumns = [];
            }
            
            console.log('文件删除成功');
          } else {
            console.error('删除失败:', result.error);
          }
        } else {
          console.error('删除请求失败，状态码:', response.status);
        }
      } catch (error) {
        console.error('删除文件时发生错误:', error);
      }
    },
    
    async selectFile(fileId) {
      this.selectedFile = fileId;
      
      // 获取选中文件的列名
      try {
        const response = await fetch(`http://localhost:8000/data/${fileId}/info`, {
          credentials: 'include'
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            this.selectedFileColumns = result.data.column_names;
          } else {
            console.error("获取列名失败:", result.error);
            this.selectedFileColumns = [];
          }
        } else {
          console.error("获取列名失败，状态码:", response.status);
          this.selectedFileColumns = [];
        }
      } catch (error) {
        console.error("加载列名失败:", error);
        this.selectedFileColumns = [];
      }
    },
    
    async sendMessage() {
      if (this.userInput.trim() === "" || this.isWaitingForResponse) {
        return;
      }
      
      // 添加用户消息到聊天记录
      const userMessage = {
        type: "sent",
        content: this.userInput
      };
      
      this.chatMessages.push(userMessage);
      const userQuery = this.userInput;
      this.userInput = "";
      this.isWaitingForResponse = true;
      
      // 添加AI回复占位符
      const aiMessageIndex = this.chatMessages.length;
      this.chatMessages.push({
        type: "received",
        content: ""
      });
      
      try {
        // 准备请求数据
        const requestData = {
          message: userQuery,
          data_id: this.selectedFile,
          history: this.chatMessages.slice(0, -1) // 不包括刚添加的AI回复占位符
        };
        
        console.log("发送请求数据:", requestData);
        
        // 发起流式请求
        const response = await fetch('http://localhost:8000/chat/stream', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData),
          credentials: 'include'
        });
        
        console.log("收到响应:", response);
        
        if (response.ok && response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let done = false;
          let accumulatedContent = "";
          
          console.log("开始读取流式响应");
          
          // 逐步接收流式响应
          while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            
            if (value) {
              const chunk = decoder.decode(value, { stream: true });
              console.log("收到原始数据块:", JSON.stringify(chunk));
              const lines = chunk.split('\n');
              
              for (const line of lines) {
                console.log("处理行:", JSON.stringify(line));
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  console.log("解析数据:", JSON.stringify(data));
                  
                  if (data === '[DONE]') {
                    console.log("接收完成");
                    done = true;
                    break;
                  }
                  
                  try {
                    const parsed = JSON.parse(data);
                    console.log("解析后的数据:", parsed);
                    if (parsed.content !== undefined) {
                      accumulatedContent += parsed.content;
                      console.log("更新内容:", accumulatedContent);
                      // 更新AI回复内容
                      this.chatMessages[aiMessageIndex].content = accumulatedContent;
                      // 滚动到底部
                      this.$nextTick(() => {
                        const messagesContainer = document.querySelector('.messages');
                        if (messagesContainer) {
                          messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        }
                      });
                    } else if (parsed.error) {
                      console.error("流式响应错误:", parsed.error);
                      this.chatMessages[aiMessageIndex].content = `错误: ${parsed.error}`;
                      done = true;
                    }
                  } catch (e) {
                    console.error("解析流数据错误:", e, "原始数据:", data);
                    // 即使解析失败，也尝试显示原始内容
                    this.chatMessages[aiMessageIndex].content = `解析错误: ${data}`;
                  }
                } else {
                  // 处理不以 'data: ' 开头的行，可能是错误信息
                  if (line.trim() !== '') {
                    console.log("处理非data行:", line);
                    try {
                      const parsed = JSON.parse(line);
                      if (parsed.error) {
                        console.error("直接错误响应:", parsed.error);
                        this.chatMessages[aiMessageIndex].content = `错误: ${parsed.error}`;
                        done = true;
                      }
                    } catch (e) {
                      console.log("非JSON格式行，跳过");
                    }
                  }
                  console.log("跳过非data行:", line);
                }
              }
            } else {
              console.log("收到空值");
            }
          }
          console.log("流处理完成，最终内容:", accumulatedContent);
        } else {
          console.error("响应失败，状态码:", response.status);
          this.chatMessages[aiMessageIndex].content = `抱歉，无法连接到AI助手。状态码: ${response.status}`;
        }
      } catch (error) {
        console.error("发送消息时发生错误:", error);
        this.chatMessages[aiMessageIndex].content = `抱歉，处理您的请求时出现错误: ${error.message}`;
      } finally {
        this.isWaitingForResponse = false;
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
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  cursor: pointer;
  border-bottom: 1px solid #ebeef5;
}

.section-header h2 {
  margin: 0;
  color: #303133;
}

.toggle-icon {
  font-size: 20px;
  font-weight: bold;
  color: #909399;
}

.file-section-content {
  padding: 0 20px 20px 20px;
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
  position: relative;
  padding-right: 20px;
}

.delete-file {
  position: absolute;
  right: 0;
  top: 0;
  color: #909399;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.delete-file:hover {
  color: #f56c6c;
  background-color: #fef0f0;
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

.column-list-section {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  max-height: 300px;
  overflow-y: auto;
}

.column-list-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.column-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.column-item {
  padding: 8px 12px;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
}

.column-item:last-child {
  border-bottom: none;
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

.typing-indicator {
  display: inline-block;
  width: 20px;
  height: 20px;
  position: relative;
}

.typing-indicator span {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #409eff;
  margin: 0 2px;
  animation: typing 1s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
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