<template>
  <div class="wordcloud-result">
    <div v-if="wordcloudData" class="result-content">
      <div class="wordcloud-image-container">
        <div class="image-header">
          <h3>词云图像</h3>
          <button @click="downloadImage" class="download-button">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20">
                <path fill="none" d="M0 0h24v24H0z"></path>
                <path fill="currentColor" d="M1 14.5a6.496 6.496 0 0 1 3.064-5.519 8.001 8.001 0 0 1 15.872 0 6.5 6.5 0 0 1-2.936 12L7 21c-3.356-.274-6-3.078-6-6.5zm15.848 4.487a4.5 4.5 0 0 0 2.03-8.309l-.807-.503-.12-.942a6.001 6.001 0 0 0-11.903 0l-.12.942-.805.503a4.5 4.5 0 0 0 2.029 8.309l.173.013h9.35l.173-.013zM13 12h3l-4 5-4-5h3V8h2v4z"></path>
              </svg>
            下载图片
          </button>
        </div>
        <img 
          :src="getImageUrlWithTimestamp(wordcloudData.image_path)" 
          :alt="`词云分析 - ${wordcloudData.column}`"
          class="wordcloud-image"
          ref="wordcloudImage"
        />
      </div>
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
export default {
  name: "WordCloudResult",
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
    getImageUrl(imagePath) {
      // 确保图片路径正确，去除开头的斜杠（如果有的话）
      if (imagePath.startsWith('/')) {
        return imagePath;
      }
      return '/' + imagePath;
    },

    getImageUrlWithTimestamp(imagePath) {
      if (!imagePath) return '';
      // 添加时间戳以避免浏览器缓存
      const timestamp = Date.now();
      const url = this.getImageUrl(imagePath);
      return `${url}?t=${timestamp}`;
    },

    downloadImage() {
      const imageUrl = this.getImageUrlWithTimestamp(this.wordcloudData.image_path);
      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = `wordcloud-${this.wordcloudData.column}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
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
  flex-wrap: wrap;
  gap: 30px;
}

.wordcloud-image-container {
  flex: 1;
  min-width: 300px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
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

.wordcloud-image {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.wordcloud-info {
  flex: 1;
  min-width: 300px;
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
  
  .wordcloud-image-container,
  .wordcloud-info {
    min-width: 100%;
  }
}
</style>