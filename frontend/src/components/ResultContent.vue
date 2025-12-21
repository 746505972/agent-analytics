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
    
    <!-- 相关性分析结果 -->
    <div v-else-if="currentMethod === 'correlation_analysis' && datasetDetails" class="analysis-section">
      <CorrelationAnalysisResult :dataset-details="datasetDetails" />
    </div>
    
    <!-- T检验结果 -->
    <div v-else-if="currentMethod === 't_test' && datasetDetails" class="analysis-section">
      <TTestResult :datasetDetails="datasetDetails" />
    </div>
    
    <!-- 词云分析结果 -->
    <div v-else-if="currentMethod === 'text_analysis' && datasetDetails" class="analysis-section">
      <WordCloudResult :data="datasetDetails" />
    </div>
    
    <!-- 数据可视化结果 -->
    <div v-else-if="(currentMethod === 'line_chart' || currentMethod === 'data_visualization') && datasetDetails" class="analysis-section">
      <VisualizationPanel :dataset-details="datasetDetails" />
    </div>

    <!-- 情感分析结果 -->
    <div v-else-if="currentMethod === 'sentiment_analysis' && datasetDetails" class="analysis-section">
      <SentimentAnalysisResult :dataset-details="datasetDetails" />
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
import CorrelationAnalysisResult from './AnalyseResult/CorrelationAnalysisResult.vue';
import TTestResult from './AnalyseResult/TTestResult.vue';
import VisualizationPanel from './Charts/VisualizationPanel.vue';
import WordCloudResult from './AnalyseResult/WordCloudResult.vue';
import SentimentAnalysisResult from "@/components/AnalyseResult/SentimentAnalysisResult.vue";

export default {
  name: "ResultContent",
  components: {
    SentimentAnalysisResult,
    BasicInfoResult,
    StatisticalSummaryResult,
    CorrelationAnalysisResult,
    TTestResult,
    VisualizationPanel,
    WordCloudResult
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