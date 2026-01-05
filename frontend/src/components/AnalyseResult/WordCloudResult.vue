<template>
  <div class="wordcloud-result" v-if="datasetDetails.resultMethod === 'text_analysis'">
    <div v-if="wordcloudData" class="result-content">
      <!-- 图表显示在上方 -->
      <div class="chart-container">
        <BackendChartResult
          :chartPath="wordcloudData.chart_path"
          ref="backendChartResult"
        />
      </div>

      <!-- 信息面板在下方 -->
      <div class="wordcloud-info">
        <h3>分析信息</h3>
        <div class="info-card">
          <div class="info-item">
            <span class="info-label">分析列:</span>
            <span class="info-value">{{ wordcloudData.column }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">总词数:</span>
            <span class="info-value">{{ wordcloudData.total_words }}</span>
          </div>
        </div>
        
        <div class="top-words">
          <h4>高频词汇</h4>
          <div class="words-container">
            <div 
              v-for="(count, word, index) in topWords" 
              :key="index" 
              class="word-item"
            >
              <span class="word-text">{{ word }}</span>
              <span class="word-count">{{ count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BackendChartResult from "../Charts/BackendChartResult.vue";

export default {
  name: "WordCloudResult",
  components: {
    BackendChartResult
  },
  props: {
    datasetDetails: {
      type: Object,
      default: () => null
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    }
  },
  methods: {
    downloadImage() {
      // 对于pyecharts生成的图表，我们可能需要通过后端API获取图片
      // 或者使用html2canvas等库将图表转换为图片下载
      if (this.wordcloudData?.chart_path) {
        // 尝试直接下载图表HTML文件或通过后端API下载图片
        const link = document.createElement('a');
        link.href = this.wordcloudData.chart_path;
        link.download = `wordcloud-${this.wordcloudData.column}.html`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  },
  computed: {
    wordcloudData() {
      return this.datasetDetails || null;
    },
    
    topWords() {
      if (!this.wordcloudData?.top_words) return {};
      return this.wordcloudData.top_words;
    }
  }
};
</script>

<style scoped>
.wordcloud-result {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.wordcloud-result h3 {
  margin-top: 0;
  color: #303133;
  font-weight: 600;
}

.loading, .error {
  text-align: center;
}

.loading p, .error p {
  font-size: 16px;
  color: #606266;
  margin-top: 20px;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #409eff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-content {
  display: flex;
  flex-direction: column; /* 改为垂直布局 */
  gap: 30px;
}

.chart-container {
  flex: 1;
  width: 100%; /* 确保宽度占满容器 */
}

.image-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.image-header h3 {
  margin: 0;
}

.download-button {
  background: linear-gradient(0deg, rgb(65, 159, 255) 0%, rgba(78, 208, 255, 0.72) 100%);
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.3s;
}

.download-button:hover {
  background-color: #66b1ff;
}

.chart-container .chart-container {
  height: 500px;
}

.wordcloud-info {
  flex: 1;
  min-width: 300px;
  width: 100%; /* 确保宽度占满容器 */
}

.info-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #606266;
}

.info-value {
  font-weight: 600;
  color: #303133;
}

.wordcloud-info h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
  font-size: 18px;
}

.words-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.word-item {
  background: #ecf5ff;
  border-radius: 20px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.word-text {
  font-weight: 500;
  color: #409eff;
}

.word-count {
  background: #409eff;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 12px;
  min-width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .result-content {
    flex-direction: column;
  }
  
  .chart-container,
  .wordcloud-info {
    min-width: 100%;
  }
}
</style>