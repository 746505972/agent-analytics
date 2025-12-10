<template>
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
          <div v-else class="message-content-wrapper">
            <div v-html="renderMarkdown(message.content)" class="message-content"></div>
            <button 
              v-if="message.content" 
              @click="copyMessageText(message.content)"
              class="copy-button"
              :class="{ copied: message.copied }"
              :title="message.copied ? '已复制' : '复制文本'"
            >
              {{ message.copied ? '✓ 已复制' : '复制' }}
            </button>
          </div>
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
</template>

<script>
import { marked } from 'marked';

export default {
  name: "ChatAssistant",
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
  data() {
    return {
      userInput: "",
      chatMessages: [
        {
          type: "received",
          content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
        }
      ],
      isWaitingForResponse: false
    }
  },
  async created() {
    // 在组件创建时调用测试接口获取session_id
    await this.initializeSession();
  },
  mounted() {
    // 恢复保存的聊天记录
    this.restoreChatHistory();
  },
  methods: {
    // 添加初始化session的方法
    async initializeSession() {
      try {
        const response = await fetch('/chat/test', {
          method: 'POST',
          credentials: 'include'
        });
        
        if (response.ok) {
          console.log('Session initialized successfully');
        } else {
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
          data_id: this.selectedFile,
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
                      this.chatMessages[aiMessageIndex].content = accumulatedContent;
                      // 滚动到底部并触发更新
                      await this.$nextTick(() => {
                        const messagesContainer = document.querySelector('.messages');
                        if (messagesContainer) {
                          messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        }
                      });
                                          
                      // 每累积一定字符数就强制更新DOM以实现实时显示效果
                      if (accumulatedContent.length % 5 === 0) {
                        await this.$nextTick();
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
                          const toolInfo = `工具调用详情:\n工具名称: ${toolCall.name}\n参数: ${JSON.stringify(toolCall.args, null, 2)}`;
                          this.showCopyNotification(toolInfo, false);
                          
                          // 等待一段时间后刷新文件列表
                          setTimeout(async () => {
                            // 触发父组件刷新文件列表的事件
                            this.$emit('refresh-files');
                            
                            // 显示通知
                            this.showCopyNotification(`工具执行成功，请在文件列表中查看新文件`, false);
                          }, 1000);
                        } else {
                          // 显示其他工具调用信息的通知
                          const toolInfo = `工具调用详情:\n工具名称: ${toolCall.name}\n参数: ${JSON.stringify(toolCall.args, null, 2)}`;
                          this.showCopyNotification(toolInfo, false);
                        }
                      }
                    } else if (parsed.error) {
                      this.chatMessages[aiMessageIndex].content = `错误: ${parsed.error}`;
                      done = true;
                    }
                  } catch (e) {
                    // 即使解析失败，也尝试显示原始内容
                    this.chatMessages[aiMessageIndex].content = `解析错误: ${data}`;
                    
                    // 强制更新DOM
                    await this.$nextTick();
                  }
                }
              }
            }
          }
        } else {
          this.chatMessages[aiMessageIndex].content = `抱歉，无法连接到AI助手。状态码: ${response.status}`;
        }
      } catch (error) {
        this.chatMessages[aiMessageIndex].content = `抱歉，处理您的请求时出现错误: ${error.message}`;
      } finally {
        this.isWaitingForResponse = false;
        // 保存聊天记录到localStorage
        localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      }
    },
    
    clearChatHistory() {
      if (confirm('确定要清除聊天历史记录吗？')) {
        // 重置聊天记录为初始状态
        this.chatMessages = [
          {
            type: "received",
            content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
          }
        ];
        // 清除localStorage中的聊天记录
        localStorage.removeItem('dashboardChatMessages');
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
      // 创建通知元素
      const notification = document.createElement('div');
      notification.textContent = message;
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background-color: ${isError ? '#f56c6c' : '#67c23a'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        z-index: 2000;
        font-size: 14px;
        max-width: 30%;
      `;
      
      // 添加到页面
      document.body.appendChild(notification);
      
      // 3秒后移除
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 3000);
    },
    
    restoreChatHistory() {
      // 从localStorage恢复聊天记录
      const savedMessages = localStorage.getItem('dashboardChatMessages');
      if (savedMessages) {
        try {
          this.chatMessages = JSON.parse(savedMessages);
        } catch (e) {
          console.error("解析聊天记录失败:", e);
          this.chatMessages = [
            {
              type: "received",
              content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
            }
          ];
        }
      }
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

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.chat-header h2 {
  padding-left: 20px;
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
  padding: 20px;
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
  padding: 2px 6px;
  font-size: 12px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.message:hover .copy-button {
  opacity: 1;
}

.copy-button:hover {
  background-color: #409eff;
  color: white;
}

.copy-button.copied {
  background-color: #67c23a;
  color: white;
  opacity: 1;
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
</style>