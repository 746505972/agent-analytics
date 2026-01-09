<template>
  <div class="history-buttons">
    <div
      v-for="(historyItem, index) in selectedAnalysisHistory"
      :key="index"
    >
      <div class="history-button">
        {{ historyItem.name }}{{ historyItem.id }}
        <button class="delete-history-button"
          @click="removeSelectedHistory(index)">×</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HistoryButtons",
  props: {
    selectedAnalysisHistory: {
      type: Array,
      default: () => []
    }
  },
  emits: ['remove-selected-history'],
  methods: {
    removeSelectedHistory(index) {
      this.$emit('remove-selected-history', index);
    }
  }
}
</script>

<style scoped>
.history-button {
  padding: 2px;
  background-color: rgba(144, 147, 153, 0.4);
  border: none;
  border-radius: 4px;
  font-size: 10px;
  transition: background-color 0.3s;
  user-select: none;
  flex: 0 0 auto; /* 防止flex项目收缩 */
}

.history-button:hover {
  background-color: #66b1ff;
}

.delete-history-button {
  font-size: 10px;
  border: none;
  background-color: unset;
  cursor: pointer;
}

.delete-history-button:hover {
  color: #ff4d4f;
}

.history-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: nowrap; /* 改为不换行，强制横向滚动 */
  max-height: 40px; /* 设置最大高度 */
  padding: 2px 10px;
  overflow-x: auto;
  overflow-y: hidden; /* 隐藏垂直滚动条 */
  white-space: nowrap; /* 防止项目换行 */
}

</style>