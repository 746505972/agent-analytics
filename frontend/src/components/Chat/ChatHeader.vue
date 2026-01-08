<script>
export default {
  name: "ChatHeader",
  data() {
    return {
      isShowingHistory: false
    }
  },
  methods: {
    toggleHistoryView() {
      this.isShowingHistory = !this.isShowingHistory
      this.$emit('toggleHistoryView', this.isShowingHistory)
    },
    createNewSession() {
      this.$emit('createNewSession')
    }
  },
  props: {
    isHistoryShowing: Boolean
  },
}
</script>

<template>
  <div class="chat-header">
    <div class="header-left">
      <h2>数据分析助手</h2>
    </div>
    <div class="header-right">
      <!-- 历史记录按钮 -->
      <button @click="toggleHistoryView" class="history-btn" :class="{ active: isShowingHistory }" title="查看历史记录">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
          <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
        </svg>
      </button>
      <button @click="createNewSession" class="new-session-btn" title="新建会话">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.chat-header h2 {
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 20px;
  color: #303133;
}

/* 多会话UI样式 */
.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.new-session-btn{
  padding: 5px;
  background-color: #f0f0f0;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.new-session-btn:hover{
  background-color: #e6e6e6;
}

/* 历史记录按钮样式 */
.history-btn {
  padding: 5px;
  background-color: #f0f0f0;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-btn:hover {
  background-color: #e6e6e6;
}

.history-btn.active {
  background-color: #409eff;
  color: white;
}

</style>