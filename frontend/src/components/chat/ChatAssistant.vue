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
    chatMessages: {
      type: Array,
      required: true
    },
    selectedFile: {
      type: String,
      default: null
    },
    isWaitingForResponse: {
      type: Boolean,
      default: false
    },
    userInput: {
      type: String,
      default: ""
    }
  },
  emits: ['send-message', 'clear-history', 'update:userInput'],
  methods: {
    renderMarkdown(content) {
      if (!content) return '';
      return marked.parse(content);
    },
    
    sendMessage() {
      this.$emit('send-message');
    },
    
    clearChatHistory() {
      this.$emit('clear-history');
    },
    
    copyMessageText(text) {
      navigator.clipboard.writeText(text).then(() => {
        // 添加视觉反馈
        console.log('文本已复制到剪贴板');
        // 创建一个临时的提示元素
        this.showCopyNotification('文本已复制到剪贴板');
      }).catch(err => {
        console.error('复制失败:', err);
        this.showCopyNotification('复制失败: ' + err.message, true);
      });
    },
    
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
      `;
      
      // 添加到页面
      document.body.appendChild(notification);
      
      // 3秒后移除
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 3000);
    }
  },
  watch: {
    userInput(newVal) {
      this.$emit('update:userInput', newVal);
    }
  }
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