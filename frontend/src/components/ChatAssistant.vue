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
              :title="'复制文本'"
            >
              <img src="@/assets/images/copy.svg" alt="复制" width="12px" height="12px"/>
            </button>
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
import '@/styles/chat.css'

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
                      console.log(accumulatedContent)
                      
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

    onAddClick() {
      // 用于将localStorage里的分析结果添加到agent上下文中。
      // 待实现
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
