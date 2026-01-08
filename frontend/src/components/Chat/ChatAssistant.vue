<template>
  <div class="chat-section">
    <ChatHeader 
      v-model:is-showing-history="isShowingHistory"
      @toggleHistoryView="toggleHistoryView" 
      @createNewSession="createNewSession" 
    />
    <!-- 历史记录视图 -->
    <div v-if="isShowingHistory" class="chat-box">
      <HistoryView
        :sessions="sessions"
        @sessionClick="switchToSession"
        @deleteSession="deleteSession"
      />
    </div>
    <!-- 聊天视图 -->
    <div v-else class="chat-box">
      <div class="chat-view">
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
            <div v-else class="message-content-wrapper">
              <div v-html="renderMarkdown(message.content)" class="message-content"></div>
              <button
                v-if="message.content"
                @click="copyMessageText(message.content)"
                class="copy-button"
                :class="{ copied: message.copied }"
                :title="'复制文本'"
              >
                <img src="../../assets/images/copy.svg" alt="复制" width="12px" height="12px"/>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="input-area">
        <div class="messageBox">
          <textarea
            type="text" 
            placeholder="输入您的分析需求..." 
            v-model="userInput"
            @keyup.enter="sendMessage"
            :disabled="!selectedFile || isWaitingForResponse"
            required
            id="messageInput"
          />
          <div class="fileUploadWrapper">
            <label>
              <svg @click="onAddClick" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 337 337">
                <circle
                  stroke-width="20"
                  stroke="#6c6c6c"
                  fill="none"
                  r="158.5"
                  cy="168.5"
                  cx="168.5"
                ></circle>
                <path
                  stroke-linecap="round"
                  stroke-width="25"
                  stroke="#6c6c6c"
                  d="M167.759 79V259"
                ></path>
                <path
                  stroke-linecap="round"
                  stroke-width="25"
                  stroke="#6c6c6c"
                  d="M79 167.138H259"
                ></path>
              </svg>
              <span class="tooltip">添加历史</span>
            </label>
          </div>
          <button @click="sendMessage" :disabled="!selectedFile || isWaitingForResponse" id="sendButton">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 664 663">
              <path
                fill="none"
                d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
              ></path>
              <path
                stroke-linejoin="round"
                stroke-linecap="round"
                stroke-width="33.67"
                stroke="#6c6c6c"
                d="M646.293 331.888L17.7538 17.6187L155.245 331.888M646.293 331.888L17.753 646.157L155.245 331.888M646.293 331.888L318.735 330.228L155.245 331.888"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import ChatHeader from "@/components/Chat/ChatHeader.vue";
import HistoryView from "@/components/Chat/HistoryView.vue";

export default {
  name: "ChatAssistant",
  components: {ChatHeader, HistoryView},
  props: {
    selectedFile: {
      type: String,
      default: null
    },
    files: {
      type: Array,
      default: () => []
    }
  },
  emits: ['refresh-files'],
  data() {
    return {
      userInput: "",
      // 会话管理相关数据
      sessions: [],
      currentSessionId: null,
      isWaitingForResponse: false,
      isShowingHistory: false // 新增：是否显示历史记录视图
    }
  },
  computed: {
    // 当前会话对象
    currentSession() {
      if (!this.currentSessionId) {
        return null;
      }
      return this.sessions.find(session => session.id === this.currentSessionId);
    },
    // 当前会话的消息记录
    chatMessages() {
      if (this.currentSession) {
        return this.currentSession.messages;
      }
      return [
        {
          type: "received",
          content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
        }
      ];
    }
  },
  async created() {
    // 在组件创建时调用测试接口获取session_id
    await this.initializeSessionID();
    
    // 初始化多会话
    this.initializeSessions();
  },
  methods: {
    // 生成唯一会话ID
    generateSessionId() {
      return 'session_' + Date.now();
    },
    
    // 创建新会话
    createNewSession() {
      // 如果当前会话名为"新会话"，则不创建新会话
      if (this.sessions[0]?.name === '新会话') {
        return;
      }
      
      const newSessionId = this.generateSessionId();
      const newSession = {
        id: newSessionId,
        name: '新会话',
        createdAt: new Date().toISOString(),
        messages: [
          {
            type: "received",
            content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
          }
        ]
      };
      
      this.sessions.unshift(newSession);
      this.currentSessionId = newSessionId;
      
      // 保存会话到localStorage
      this.saveSessions();
      
      return newSessionId;
    },
    
    // 切换到指定会话
    switchToSession(sessionId) {
      const session = this.sessions.find(s => s.id === sessionId);
      if (session) {
        this.currentSessionId = sessionId;
        // 保存当前会话ID到localStorage以保持状态
        localStorage.setItem('currentSessionId', sessionId);
        // 切换回聊天视图
        this.isShowingHistory = false;
      }
    },
    
    // 删除指定会话
    deleteSession(sessionId) {
      
      const sessionIndex = this.sessions.findIndex(s => s.id === sessionId);
      if (sessionIndex !== -1) {
        this.sessions.splice(sessionIndex, 1);
        
        // 如果删除的是当前会话
        if (this.currentSessionId === sessionId) {
          if (this.sessions.length > 0) {
            // 切换到第一个会话
            this.currentSessionId = this.sessions[0].id;
          } else {
            // 如果没有其他会话，清除当前会话ID
            this.currentSessionId = null;
            // 从localStorage中移除currentSessionId
            localStorage.removeItem('currentSessionId');
          }
        }
        
        this.saveSessions();
        
        // 如果删除了所有会话，创建一个新会话
        if (this.sessions.length === 0) {
          this.createNewSession();
        }
      }
    },
    
    // 保存所有会话到localStorage
    saveSessions() {
      localStorage.setItem('chatSessions', JSON.stringify(this.sessions));
      if (this.currentSessionId) {
        localStorage.setItem('currentSessionId', this.currentSessionId);
      }
    },
    
    // 添加初始化session的方法
    async initializeSessionID() {
      try {
        const response = await fetch('/chat/test', {
          method: 'POST',
          credentials: 'include'
        });
        if (!response.ok) {
          console.error('Failed to initialize session, status:', response.status);
        }
      } catch (error) {
        console.error('Error initializing session:', error);
      }
    },
    
    // 添加Markdown渲染方法
    renderMarkdown(content) {
      if (!content) return '';
      return marked.parse(content);
    },
    
    async sendMessage() {
      if (this.userInput.trim() === "" || this.isWaitingForResponse) {
        return;
      }
      
      // 确保当前会话存在
      if (!this.currentSession) {
        this.createNewSession();
      }
      
      // 添加用户消息到当前会话的聊天记录
      const userMessage = {
        type: "sent",
        content: this.userInput
      };
      
      this.currentSession.messages.push(userMessage);
      const userQuery = this.userInput;
      this.userInput = "";
      this.isWaitingForResponse = true;
      
      // 添加AI回复占位符
      const aiMessageIndex = this.currentSession.messages.length;
      this.currentSession.messages.push({
        type: "received",
        content: ""
      });
      
      // 保存会话到localStorage
      this.saveSessions();
      
      try {
        // 准备请求数据
        const requestData = {
          message: userQuery,
          data_id: this.selectedFile,
          history: this.currentSession.messages.slice(0, -1) // 不包括刚添加的AI回复占位符
        };

        // 如果是第一次查询，先调用生成标题的API
        if (this.currentSession.name === '新会话') {
          try {
            const titleResponse = await fetch('/chat/generate_title', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(requestData),
              credentials: 'include'
            });
            
            if (titleResponse.ok) {
              const titleData = await titleResponse.json();
              // 更新会话名称
              this.currentSession.name = titleData.title;
              this.saveSessions();
            }
          } catch (titleError) {
            console.error('生成会话标题失败:', titleError);
          }
        }
        
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
          let toolCalls = [];
          
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
                      this.currentSession.messages[aiMessageIndex].content = accumulatedContent;
                      
                      // 强制更新DOM以实现实时显示效果
                      await this.$nextTick();
                      
                      // 滚动到底部
                      const messagesContainer = document.querySelector('.messages');
                      if (messagesContainer) {
                        messagesContainer.scrollTop = messagesContainer.scrollHeight;
                      }
                    } else if (parsed.tool_calls !== undefined) {
                      // 处理工具调用信息
                      toolCalls = parsed.tool_calls;
                      
                      // 如果产生新文件，需要刷新文件列表并选中新文件
                      for (const toolCall of toolCalls) {
                        if (['add_header_tool','remove_first_row_tool','modify_header_row_tool',
                        'delete_columns_tool','remove_invalid_samples_tool','handle_missing_values_tool',
                        'dimensionless_processing_tool','scientific_calculation_tool',
                        'one_hot_encoding_tool','text_to_numeric_or_datetime_tool'].includes(toolCall.name)) {
                          // 显示工具调用通知
                          const toolInfo = `工具调用:\n${toolCall.name}`;
                          this.showCopyNotification(toolInfo, false);
                          // TODO: 工具名反映射回中文
                          // 等待一段时间后刷新文件列表
                          setTimeout(async () => {
                            // 触发父组件刷新文件列表的事件
                            this.$emit('refresh-files');
                            
                            // 显示通知
                            this.showCopyNotification(`工具执行成功，请在文件列表中查看新文件`, false);
                          }, 500);
                        } else {
                          // 显示其他工具调用信息的通知
                          const toolInfo = `工具调用:\n${toolCall.name}`;
                          this.showCopyNotification(toolInfo, false);
                        }
                      }
                    } else if (parsed.error) {
                      this.currentSession.messages[aiMessageIndex].content = `错误: ${parsed.error}`;
                      done = true;
                    }
                  } catch (e) {
                    // 即使解析失败，也尝试显示原始内容
                    this.currentSession.messages[aiMessageIndex].content = `解析错误: ${data}`;
                    
                    // 强制更新DOM
                    await this.$nextTick();
                  }
                }
              }
            }
          }
        } else {
          this.currentSession.messages[aiMessageIndex].content = `抱歉，无法连接到AI助手。状态码: ${response.status}`;
        }
      } catch (error) {
        this.currentSession.messages[aiMessageIndex].content = `抱歉，处理您的请求时出现错误: ${error.message}`;
      } finally {
        this.isWaitingForResponse = false;
        // 保存会话到localStorage
        this.saveSessions();
      }
    },
    
    // 复制消息文本
    copyMessageText(text) {
      // 检查 Clipboard API 是否可用
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
          // 添加视觉反馈
          console.log('文本已复制到剪贴板');
          // 创建一个临时的提示元素
          this.showCopyNotification('文本已复制到剪贴板');
        }).catch(err => {
          console.error('复制失败:', err);
          this.showCopyNotification('复制失败: ' + err.message, true);
        });
      } else {
        // 降级处理：使用传统的 execCommand 方法
        try {
          const textArea = document.createElement('textarea');
          textArea.value = text;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand('copy');
          document.body.removeChild(textArea);
          this.showCopyNotification('文本已复制到剪贴板');
        } catch (err) {
          console.error('复制失败:', err);
          this.showCopyNotification('复制失败: ' + err.message, true);
        }
      }
    },
    
    // 显示复制通知
    showCopyNotification(message, isError = false) {
      // 创建或获取通知容器
      let notificationContainer = document.getElementById('notification-container');
      if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = `
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 2000;
          display: flex;
          flex-direction: column;
          gap: 10px;
        `;
        document.body.appendChild(notificationContainer);
      }
      
      // 创建通知元素
      const notification = document.createElement('div');
      notification.textContent = message;
      notification.style.cssText = `
        padding: 12px 20px;
        background-color: ${isError ? '#f56c6c' : '#67c23a'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        font-size: 14px;
        max-width: 300px;
        animation: slideIn 0.3s ease-out;
      `;
      
      // 添加到通知容器
      notificationContainer.appendChild(notification);
      
      // 3秒后移除
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
          
          // 如果容器为空，移除容器
          if (notificationContainer.children.length === 0) {
            if (notificationContainer.parentNode) {
              notificationContainer.parentNode.removeChild(notificationContainer);
            }
          }
        }
      }, 3000);
    },

    // 初始化会话
    initializeSessions() {
      // 从localStorage加载现有会话
      const savedSessions = localStorage.getItem('chatSessions');
      if (savedSessions) {
        try {
          this.sessions = JSON.parse(savedSessions);
          
          // 获取上次活动的会话ID
          const lastSessionId = localStorage.getItem('currentSessionId');
          
          // 检查是否有有效的会话ID
          if (lastSessionId && this.sessions.some(session => session.id === lastSessionId)) {
            this.currentSessionId = lastSessionId;
          } else if (this.sessions.length > 0) {
            // 如果没有有效的会话ID，使用第一个会话
            this.currentSessionId = this.sessions[0].id;
          } else {
            // 如果没有任何会话，创建一个新会话
            this.createNewSession();
          }
        } catch (e) {
          console.error("解析会话数据失败:", e);
          // 如果解析失败，创建一个新会话
          this.sessions = [];
          this.createNewSession();
        }
      } else {
        // 如果没有保存的会话，创建一个新会话
        this.createNewSession();
      }
    },
    
    onAddClick() {
      // 用于将localStorage里的分析结果添加到agent上下文中。
      // 待实现
    },
    
    // 切换历史记录视图
    toggleHistoryView() {
      this.isShowingHistory = !this.isShowingHistory;
    }

  },
}
</script>

<style scoped>
.chat-section {
  background: white;
  border-radius: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-section h2 {
  margin-top: 10px;
  margin-bottom: 10px;
  color: #303133;
}

.chat-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 500px;
  height: 100%;
}

.messages {
  flex: 1;
  padding: 20px 20px 0 20px;
  overflow-y: auto;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 4px;
}

.message.sent {
  background-color: #409eff;
  color: white;
  margin-left: auto;
  max-width: 80%;
}

.message.received {
  max-width: 100%;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.message-content-wrapper {
  position: relative;
}

.copy-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 4px 4px;
  font-size: 12px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.message:hover .copy-button {
  opacity: 1;
}

.copy-button:hover {
  background-color: rgba(64, 158, 255, 0.7);
  color: white;
}

.copy-button.copied {
  background-color: #67c23a;
  color: white;
  opacity: 1;
}

.typing-indicator {
  display: inline-block;
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
  padding: 0 10px 10px 10px;
}

.messageBox {
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}
.messageBox:focus-within {
  border: 1px solid #409eff;
}
.fileUploadWrapper {
  width: fit-content;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Arial, Helvetica, sans-serif;
  padding: 5px;
}

.fileUploadWrapper label {
  cursor: pointer;
  width: fit-content;
  height: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.fileUploadWrapper label svg {
  height: 18px;
}
.fileUploadWrapper label svg path {
  transition: all 0.3s;
  stroke: #606266;
}
.fileUploadWrapper label svg circle {
  transition: all 0.3s;
  stroke: #606266;
}
.fileUploadWrapper label:hover svg path {
  stroke: #409eff;
}
.fileUploadWrapper label:hover svg circle {
  stroke: #409eff;
  fill: #f5f7fa;
}
.fileUploadWrapper label:hover .tooltip {
  display: block;
  opacity: 1;
}
.tooltip {
  position: absolute;
  top: -40px;
  display: none;
  opacity: 0;
  font-size: 10px;
  text-wrap: nowrap;
  background-color: #ffffff;
  padding: 6px 10px;
  border-radius: 5px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.596);
  transition: all 0.3s;
}
#messageInput {
  width: 200px;
  height: 100%;
  background-color: transparent;
  outline: none;
  border: none;
  padding: 5px 0 5px 5px;
  color: #606266;
  flex: 1;
  white-space: pre-wrap;      /* 保留空格并允许换行 */
  overflow-wrap: break-word;  /* 现代标准的换行属性 */
  resize: none;               /* 如果不需要用户调整大小 */
  overflow-y: auto;           /* 内容过多时显示垂直滚动条 */
}
#messageInput:focus ~ #sendButton svg path,
#messageInput:valid ~ #sendButton svg path {
  stroke: #409eff;
}

#sendButton {
  width: fit-content;
  height: 100%;
  background-color: transparent;
  outline: none;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  padding: 5px;
}
#sendButton svg {
  height: 18px;
}
#sendButton svg path {
  transition: all 0.3s;
  stroke: #606266;
}
#sendButton:hover svg path {
  stroke: #409eff;
}

/* 保持原有的按钮样式 */
#sendButton:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 聊天视图样式 */
.chat-view {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Markdown 表格样式 */
.message.received :deep(table) {
  border-collapse: collapse;
  margin: 15px 0;
  font-size: 0.9em;
  font-family: sans-serif;
  min-width: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 0;
}

.message.received :deep(table th),
.message.received :deep(table td) {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  text-align: left;
}

.message.received :deep(table th) {
  background-color: #f5f7fa;
  font-weight: 600;
}

.message.received :deep(table tbody tr:nth-of-type(even)) {
  background-color: #f8f9fa;
}

.message.received :deep(table tbody tr:hover) {
  background-color: #f0f2f5;
}

/* Markdown 代码块样式 */
.message.received :deep(code) {
  background-color: #f6f8fa;
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.875em;
  font-family: 'SFMono-Regular', Consolas, 'Courier New', monospace;
  color: #24292f;
}

.message.received :deep(pre) {
  background-color: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  border: 1px solid #d0d7de;
}

.message.received :deep(pre code) {
  background-color: transparent;
  padding: 0;
  font-size: 0.875em;
  color: #24292f;
}

</style>