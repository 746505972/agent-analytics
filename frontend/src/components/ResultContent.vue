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
      <TTestResult :dataset-details="datasetDetails" />
    </div>
    
    <!-- F检验结果 -->
    <div v-else-if="currentMethod === 'f_test' && datasetDetails" class="analysis-section">
      <FTestResult :dataset-details="datasetDetails" />
    </div>
    
    <!-- 正态性检验结果 -->
    <div v-else-if="currentMethod === 'normality_test' && datasetDetails" class="analysis-section">
      <NormalityTestResult :dataset-details="datasetDetails" />
    </div>

    <!-- 卡方检验结果 -->
    <div v-else-if="currentMethod === 'chi_square_test' && datasetDetails" class="analysis-section">
      <ChiSquareTestResult :dataset-details="datasetDetails" />
    </div>

    <!-- 非参数检验结果 -->
    <div v-else-if="currentMethod === 'non_parametric_test' && datasetDetails" class="analysis-section">
      <NonParametricTestResult :dataset-details="datasetDetails" />
    </div>

    <!-- 线性回归结果 -->
    <div v-else-if="currentMethod === 'linear_regression' && datasetDetails" class="analysis-section">
      <LinearRegressionResult :datasetDetails="datasetDetails" />
    </div>

    <!-- 逻辑回归结果 -->
    <div v-else-if="currentMethod === 'logistic_regression' && datasetDetails" class="analysis-section">
      <LogisticRegressionResult :datasetDetails="datasetDetails" />
    </div>

    <!-- 词云分析结果 -->
    <div v-else-if="currentMethod === 'text_analysis' && datasetDetails" class="analysis-section">
      <WordCloudResult :dataset-details="datasetDetails" />
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
    <Waiting v-else-if="isWaitingForResponse"/>

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
import NormalityTestResult from './AnalyseResult/NormalityTestResult.vue';
import VisualizationPanel from './Charts/VisualizationPanel.vue';
import WordCloudResult from './AnalyseResult/WordCloudResult.vue';
import SentimentAnalysisResult from "@/components/AnalyseResult/SentimentAnalysisResult.vue";
import FTestResult from "@/components/AnalyseResult/FTestResult.vue";
import ChiSquareTestResult from "@/components/AnalyseResult/ChiSquareTestResult.vue";
import NonParametricTestResult from "@/components/AnalyseResult/NonParametricTestResult.vue";
import LinearRegressionResult from "@/components/AnalyseResult/LinearRegressionResult.vue";
import Waiting from "@/components/Waiting.vue";
import LogisticRegressionResult from "@/components/AnalyseResult/LogisticRegressionResult.vue";

export default {
  name: "ResultContent",
  components: {
    Waiting,
    ChiSquareTestResult,
    FTestResult,
    SentimentAnalysisResult,
    BasicInfoResult,
    StatisticalSummaryResult,
    CorrelationAnalysisResult,
    TTestResult,
    NormalityTestResult,
    VisualizationPanel,
    WordCloudResult,
    NonParametricTestResult,
    LinearRegressionResult,
    LogisticRegressionResult
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
    isWaitingForResponse: {
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

</style>