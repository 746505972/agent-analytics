<template>
  <div class="result-content">
    <!-- 基本信息分析结果 -->
    <div v-if="currentMethod === 'basic_info' && datasetDetails" class="analysis-section">
      <BasicInfoResult :dataset-details="datasetDetails" />
    </div>
    
    <!-- 统计摘要分析结果 -->
    <div v-else-if="currentMethod === 'statistical_summary' && datasetDetails" class="analysis-section">
      <StatisticalSummaryResult :dataset-details="datasetDetails" />
    </div>
    
    <!-- 数据可视化分析结果 -->
    <div v-else-if="currentMethod === 'visualization'" class="analysis-section">
      <h3>数据可视化</h3>
      <p>此功能正在开发中...</p>
    </div>
    
    <!-- 机器学习分析结果 -->
    <div v-else-if="currentMethod === 'ml_analysis'" class="analysis-section">
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
</template>

<script>
import BasicInfoResult from './AnalyseResult/BasicInfoResult.vue';
import StatisticalSummaryResult from './AnalyseResult/StatisticalSummaryResult.vue';

export default {
  name: "ResultContent",
  components: {
    BasicInfoResult,
    StatisticalSummaryResult
  },
  props: {
    currentMethod: {
      type: String,
      required: true
    },
    datasetDetails: {
      type: Object,
      default: null
    },
    loadingDetails: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style scoped>
.result-content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
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
</style>