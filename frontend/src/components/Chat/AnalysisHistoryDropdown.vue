<template>
  <div class="analysis-history-dropdown" v-click-outside="closeDropdown" >
    <div v-if="showDropdown" class="dropdown-content">
      <div
        v-for="(historyItem, index) in analysisHistory"
        :key="index"
        class="history-item"
        @click="selectAnalysisHistory(historyItem)"
      >
        <span class="history-method">{{ historyItem.name }}{{ historyItem.id }}</span>
        <span class="history-status" :class="{ selected: isHistoryItemSelected(historyItem) }">
          {{ isHistoryItemSelected(historyItem) ? '已选择' : '未选择' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import clickOutside from "@/utils/clickOutside";

export default {
  name: "AnalysisHistoryDropdown",
  directives: { clickOutside },
  props: {
    analysisHistory: {
      type: Array,
      default: () => []
    },
    selectedAnalysisHistory: {
      type: Array,
      default: () => []
    },
    showDropdown: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:showDropdown', 'selectHistory', 'removeHistory'],
  methods: {
    // 选择分析历史
    selectAnalysisHistory(historyItem) {
      // 检查是否已经选择过这个历史项
      const existingIndex = this.selectedAnalysisHistory.findIndex(
        item => item.id === historyItem.id && item.method === historyItem.method
      );
      
      if (existingIndex === -1) {
        // 如果未选择，则发出select事件
        this.$emit('selectHistory', { ...historyItem });
      } else {
        // 如果已选择，则发出remove事件
        this.$emit('removeHistory', { ...historyItem });
      }
      // 保持下拉框打开状态
      this.$emit('update:showDropdown', true);
    },
    
    // 检查分析历史是否已被选中
    isHistoryItemSelected(historyItem) {
      return this.selectedAnalysisHistory.some(
        item => item.id === historyItem.id && item.method === historyItem.method
      );
    },
    
    closeDropdown() {
      this.$emit('update:showDropdown', false);
    }
  }
}
</script>

<style scoped>
/* 分析历史下拉框样式 */
.analysis-history-dropdown {
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 10px;
}

.dropdown-content {
  position: relative;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  z-index: 1000;
  max-height: 150px;
  width: 100%;
  overflow-y: auto;
  user-select: none;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 6px;
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  transition: background-color 0.3s;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background-color: #f5f7fa;
}

.history-method {
  font-size: 14px;
  color: #606266;
}

.history-status {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
}

.history-status.selected {
  background-color: #409eff;
  color: white;
}

.history-status:not(.selected) {
  background-color: #909399;
  color: white;
}
</style>