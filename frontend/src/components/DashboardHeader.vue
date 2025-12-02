<template>
  <div class="dashboard-header">
    <div class="header-content">
      <div class="file-selector-trigger" @click="$emit('toggle-file-section')">
        <h3>选择分析文件</h3>
        <span class="toggle-icon">{{ isFileSectionCollapsed ? '+' : '-' }}</span>
      </div>
      <div v-if="selectedFile" class="selected-file-info" @click="$emit('show-preview')">
        当前选中: {{ getSelectedFileName() }}
      </div>
      <h2>欢迎使用 Agent-Analytics 智能数据分析平台</h2>
      <a href="https://github.com/746505972/agent-analytics" target="_blank" class="github-link">
        <img src="@/assets/images/github-original.svg" width="20" alt="GitHub">
      </a>
    </div>
  </div>
  
  <!-- 分析历史区域 -->
  <div class="analysis-history" v-if="analysisHistory.length > 0">
    <div class="history-title">分析历史:</div>
    <div class="history-buttons">
      <div
        v-for="(historyItem, index) in analysisHistory"
        :key="index"
        class="history-item"
        :class="{ active: isHistoryItemActive(historyItem) }"
      >
        <button
          @click="$emit('load-analysis-from-history', historyItem)"
          class="history-button"
        >
          {{ getMethodName(historyItem.method) }}{{ index + 1 }}
        </button>
        <button
          @click="$emit('remove-from-history', index)"
          class="delete-history-button"
        >
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashboardHeader",
  props: {
    isFileSectionCollapsed: {
      type: Boolean,
      required: true
    },
    selectedFile: {
      type: [String, null],
      required: true
    },
    files: {
      type: Array,
      required: true
    },
    analysisHistory: {
      type: Array,
      required: true
    },
    currentMethod: {
      type: String,
      required: true
    }
  },
  emits: [
    'toggle-file-section',
    'load-analysis-from-history',
    'remove-from-history'
  ],
  methods: {
    getSelectedFileName() {
      const file = this.files.find(f => f.data_id === this.selectedFile);
      return file ? file.filename : "无";
    },
    
    // 添加获取方法名称的方法
    getMethodName(methodId) {
      const methods = {
        'basic_info': '基本信息',
        'statistical_summary': '统计摘要',
        'correlation_analysis': '相关性分析',
        'distribution_analysis': '分布分析',
        'visualization': '数据可视化',
        'ml_analysis': '机器学习分析',
        'clustering': '聚类分析',
        'classification': '分类分析',
        'regression': '回归分析',
        'text_analysis': '文本分析',
        'sentiment_analysis': '情感分析',
        'invalid_samples': '无效样本',
        'data_transformation': '数据转换',
        'add_header': '添加/修改标题行',
        'delete_columns': '删除列',
      };
      return methods[methodId] || '未知分析';
    },
    
    isHistoryItemActive(historyItem) {
      return this.selectedFile === historyItem.dataId && this.currentMethod === historyItem.method;
    }
  }
}
</script>

<style scoped>
.dashboard-header {
  text-align: center;
  padding: 10px 0 10px 0;
  border-bottom: 1px solid #ebeef5;
  position: relative;
}

/* 分析历史区域样式 */
.analysis-history {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.history-title {
  font-weight: bold;
  margin-right: 15px;
  color: #303133;
}

.history-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.history-item {
  display: flex;
  align-items: center;
}

.history-item:not(.active) .history-button {
  background-color: #909399; /* 灰色 */
  color: #ffffff;
}

.history-item:not(.active) .history-button:hover {
  background-color: #a0a3a9;
}

.history-button {
  padding: 5px 10px;
  background-color: #409eff; /* 蓝色 */
  color: white;
  border: none;
  border-radius: 4px 0 0 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.history-button:hover {
  background-color: #66b1ff;
}

.delete-history-button {
  padding: 5px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.delete-history-button:hover {
  background-color: #ff4d4f;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 30px;
  position: relative;
}

.selected-file-info {
  display: flex;
  color: #909399;
  font-size: 14px;
  white-space: nowrap;
  cursor: pointer;
}

.file-selector-trigger {
  display: flex;
  align-items: center;
  gap: 40px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #f5f7fa;
  transition: background-color 0.3s;
  position: relative;
  z-index: 101;
  user-select: none
}

.file-selector-trigger:hover {
  background-color: #e1e6ee;
}

.file-selector-trigger h3 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.dashboard-header h2 {
  color: #303133;
  margin: 0;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 10px;
  }
}
</style>