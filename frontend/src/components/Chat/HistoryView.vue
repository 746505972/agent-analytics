<template>
  <div class="history-view">
    <div class="history-list">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="history-item"
        @click="onSessionClick(session.id)"
      >
        <div class="history-content">
          <div class="history-name">
            {{ session.name }}
          </div>
          <div class="history-date">{{ formatTime(session.createdAt) }}</div>
        </div>
        <button
          @click.stop="onDeleteSession(session.id)"
          class="delete-history-btn"
          title="删除历史记录"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
            <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import {formatTime} from "@/utils/formatTime";

export default {
  name: "HistoryView",
  props: {
    sessions: {
      type: Array,
      required: true
    }
  },
  emits: ['sessionClick', 'deleteSession'],
  methods: {
    formatTime,
    onSessionClick(sessionId) {
      this.$emit('sessionClick', sessionId);
    },
    onDeleteSession(sessionId) {
      this.$emit('deleteSession', sessionId);
    },
  }
}
</script>

<style scoped>
.history-view {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: background-color 0.2s;
}

.history-item:hover {
  background-color: #e6e9f0;
}

.history-name {
  flex: 1;
  font-size: 14px;
  color: #303133;
}

.delete-history-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  margin-left: 10px;
  color: #f56c6c;
  border-radius: 4px;
}

.delete-history-btn:hover {
  background-color: #f56c6c;
  color: white;
}

/* 历史记录内容容器 */
.history-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* 历史记录日期样式 */
.history-date {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  text-align: left;
}
</style>