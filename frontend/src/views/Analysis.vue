<template>
  <div class="analysis-container">
    <div class="analysis-header">
      <div class="header-left">
        <router-link to="/dashboard" class="back-link">返回仪表板</router-link>
      </div>
      <div class="header-center">
        <h2>{{ getMethodName(analysisMethod) }}分析结果</h2>
      </div>
      <div class="header-right">
        <span class="file-name">{{ documentName }}</span>
      </div>
    </div>
    
    <div class="analysis-content">
      <!-- 基本信息分析结果 -->
      <div v-if="analysisMethod === 'basic_info' && datasetDetails" class="analysis-section">
        <div class="basic-info-details">
          <h3>数据集基本信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">文件名:</span>
              <span class="info-value">{{ datasetDetails.filename }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">行数:</span>
              <span class="info-value">{{ datasetDetails.rows }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">列数:</span>
              <span class="info-value">{{ datasetDetails.columns }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">完整性:</span>
              <span class="info-value">{{ (datasetDetails.completeness * 100).toFixed(2) }}%</span>
            </div>
          </div>
          
          <h4>列信息:</h4>
          <div class="column-details">
            <div 
              v-for="(dtype, columnName) in datasetDetails.dtypes" 
              :key="columnName"
              class="column-item"
            >
              <span class="column-name">{{ columnName }}</span>
              <span class="column-type">{{ dtype }}</span>
            </div>
          </div>
          
          <h4>前5行数据预览:</h4>
          <div class="data-preview">
            <table>
              <thead>
                <tr>
                  <th v-for="col in datasetDetails.column_names" :key="col">{{ col }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in datasetDetails.head" :key="index">
                  <td v-for="col in datasetDetails.column_names" :key="col">{{ row[col] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      <!-- 统计摘要分析结果 -->
      <div v-else-if="analysisMethod === 'statistical_summary'" class="analysis-section">
        <h3>统计摘要</h3>
        <p>此功能正在开发中...</p>
      </div>
      
      <!-- 数据可视化分析结果 -->
      <div v-else-if="analysisMethod === 'visualization'" class="analysis-section">
        <h3>数据可视化</h3>
        <p>此功能正在开发中...</p>
      </div>
      
      <!-- 机器学习分析结果 -->
      <div v-else-if="analysisMethod === 'ml_analysis'" class="analysis-section">
        <h3>机器学习分析</h3>
        <p>此功能正在开发中...</p>
      </div>
      
      <!-- 加载状态 -->
      <div v-else-if="loadingDetails" class="analysis-section">
        <div class="loading-spinner">加载分析结果中...</div>
      </div>
      
      <!-- 错误状态 -->
      <div v-else class="analysis-section">
        <p>无法加载分析结果</p>
      </div>
    </div>
    
    <!-- 右侧：聊天分析区域 -->
    <div class="chat-section">
      <div class="chat-header">
        <h2>数据分析助手</h2>
        <button @click="clearChatHistory" class="clear-chat-btn">清除历史记录</button>
      </div>
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
            <div v-else v-html="renderMarkdown(message.content)" class="message-content"></div>
          </div>
        </div>
        <div class="input-area">
          <input 
            type="text" 
            placeholder="输入您的分析需求..." 
            v-model="userInput"
            @keyup.enter="sendMessage"
            :disabled="isWaitingForResponse"
          />
          <button @click="sendMessage" :disabled="isWaitingForResponse">发送</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';

export default {
  name: 'Analysis',
  data() {
    return {
      documentName: '',
      dataId: '',
      analysisMethod: '',
      
      // 数据集详情
      datasetDetails: null,
      loadingDetails: false,
      
      // 聊天相关
      userInput: "",
      chatMessages: [
        {
          type: "received",
          content: "您好！我是您的数据分析助手，我可以帮您解读分析结果或进行进一步分析。"
        }
      ],
      isWaitingForResponse: false
    }
  },
  async mounted() {
    // 从路由参数获取dataId和分析方法
    this.dataId = this.$route.query.data_id || ''
    this.analysisMethod = this.$route.query.method || ''
    
    if (this.dataId && this.analysisMethod) {
      // 根据分析方法加载相应的结果
      await this.loadAnalysisResult()
    }
    
    // 设置默认文档名
    this.documentName = this.dataId ? `${this.dataId}.csv` : '未命名文件'
    
    // 恢复聊天记录
    this.restoreChatMessages();
  },
  methods: {
    // 添加Markdown渲染方法
    renderMarkdown(content) {
      if (!content) return '';
      return marked.parse(content);
    },
    
    async loadAnalysisResult() {
      if (!this.dataId || !this.analysisMethod) return;
      
      this.loadingDetails = true;
      try {
        if (this.analysisMethod === 'basic_info') {
          const response = await fetch(`/data/${this.dataId}/details`, {
            credentials: 'include'
          });
          
          if (response.ok) {
            const result = await response.json();
            if (result.success) {
              this.datasetDetails = result.data;
              this.documentName = result.data.filename;
            } else {
              console.error("获取分析结果失败:", result.error);
            }
          } else {
            console.error("获取分析结果失败，状态码:", response.status);
          }
        }
        // 其他分析方法可以在这里添加
      } catch (error) {
        console.error("加载分析结果失败:", error);
      } finally {
        this.loadingDetails = false;
      }
    },
    
    getMethodName(methodId) {
      const methods = {
        'basic_info': '基本信息',
        'statistical_summary': '统计摘要',
        'visualization': '数据可视化',
        'ml_analysis': '机器学习分析'
      };
      return methods[methodId] || '未知分析';
    },
    
    // 新增方法：恢复聊天记录
    restoreChatMessages() {
      const savedChatMessages = localStorage.getItem('dashboardChatMessages');
      if (savedChatMessages) {
        try {
          this.chatMessages = JSON.parse(savedChatMessages);
        } catch (e) {
          console.error("解析保存的聊天记录失败:", e);
        }
      }
    },
    
    clearChatHistory() {
      if (confirm('确定要清除聊天历史记录吗？')) {
        // 重置聊天记录为初始状态
        this.chatMessages = [
          {
            type: "received",
            content: "您好！我是您的数据分析助手，我可以帮您解读分析结果或进行进一步分析。"
          }
        ];
        // 清除localStorage中的聊天记录
        localStorage.removeItem('dashboardChatMessages');
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
      
      // 保存聊天记录到localStorage
      localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      
      // 添加AI回复占位符
      const aiMessageIndex = this.chatMessages.length;
      this.chatMessages.push({
        type: "received",
        content: ""
      });
      
      // 保存聊天记录到localStorage
      localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      
      try {
        // 准备请求数据
        const requestData = {
          message: userQuery,
          data_id: this.dataId,
          history: this.chatMessages.slice(0, -1) // 不包括刚添加的AI回复占位符
        };
        
        // 发起流式请求
        const response = await fetch('/chat/stream', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData),
          credentials: 'include'
        });
        
        if (response.ok && response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let done = false;
          let accumulatedContent = "";
          
          // 逐步接收流式响应
          while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            
            if (value) {
              const chunk = decoder.decode(value, { stream: true });
              const lines = chunk.split('\n');
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  
                  if (data === '[DONE]') {
                    done = true;
                    break;
                  }
                  
                  try {
                    const parsed = JSON.parse(data);
                    if (parsed.content !== undefined) {
                      accumulatedContent += parsed.content;
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
                }
              }
            }
          }
        } else {
          console.error("响应失败，状态码:", response.status);
          this.chatMessages[aiMessageIndex].content = `抱歉，无法连接到AI助手。状态码: ${response.status}`;
        }
      } catch (error) {
        console.error("发送消息时发生错误:", error);
        this.chatMessages[aiMessageIndex].content = `抱歉，处理您的请求时出现错误: ${error.message}`;
      } finally {
        this.isWaitingForResponse = false;
        // 保存聊天记录到localStorage
        localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      }
    }
  },
  
  // 在组件销毁前保存聊天记录
  beforeUnmount() {
    localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
  }
}
</script>

<style scoped>
.analysis-container {
  display: flex;
  height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

.analysis-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0 20px;
  z-index: 100;
}

.header-left {
  flex: 1;
}

.back-link {
  color: #409eff;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}

.header-center h2 {
  margin: 0;
  color: #303133;
}

.header-right {
  flex: 1;
  text-align: right;
}

.file-name {
  color: #606266;
  font-size: 14px;
}

.analysis-content {
  flex: 3;
  margin-top: 80px;
  margin-right: 20px;
  overflow-y: auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.analysis-section {
  min-height: 500px;
}

.loading-spinner {
  text-align: center;
  padding: 50px;
  color: #409eff;
  font-size: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.info-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.info-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.column-details {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.column-item {
  display: flex;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
}

.column-name {
  font-weight: bold;
  margin-right: 8px;
  color: #303133;
}

.column-type {
  color: #606266;
}

.data-preview {
  overflow-x: auto;
}

.data-preview table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.data-preview th,
.data-preview td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  white-space: nowrap;
}

.data-preview th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.chat-section {
  flex: 2;
  margin-top: 80px;
  background: white;
  border-radius: 8px;
  padding: 20px;

  display: flex;
  flex-direction: column;
}

.chat-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chat-header h2 {
  margin: 0;
  color: #303133;
}

.clear-chat-btn {
  padding: 5px 10px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.clear-chat-btn:hover {
  background-color: #ff4d4f;
}

.chat-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  height: 100%;
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

.message-content :deep(p) {
  margin: 0 0 10px 0;
}

.message-content :deep(ul),
.message-content :deep(ol) {
  margin: 10px 0;
  padding-left: 20px;
}

.message-content :deep(li) {
  margin-bottom: 5px;
}

.message-content :deep(strong) {
  font-weight: bold;
}

.message-content :deep(em) {
  font-style: italic;
}

.message-content :deep(code) {
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}

.message-content :deep(pre) {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.message-content :deep(pre > code) {
  background: none;
  padding: 0;
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
  .analysis-container {
    flex-direction: column;
  }
  
  .analysis-content {
    margin-right: 0;
    margin-bottom: 20px;
  }
  
  .chat-section {
    margin-top: 20px;
  }
}
</style>
