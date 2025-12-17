<template>
  <div class="wordcloud-result">
    <h3>词云分析结果</h3>
    <div v-if="loading" class="loading">
      <p>正在生成词云...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>生成词云时出错: {{ error }}</p>
    </div>
    <div v-else-if="wordcloudData" class="result-content">
      <div class="wordcloud-image-container">
        <img 
          :src="getImageUrl(wordcloudData.image_path)" 
          :alt="`词云分析 - ${wordcloudData.column}`"
          class="wordcloud-image"
        />
      </div>
      <div class="wordcloud-info">
        <h4>分析信息</h4>
        <p><strong>分析列:</strong> {{ wordcloudData.column }}</p>
        <p><strong>总词数:</strong> {{ wordcloudData.total_words }}</p>
        <div class="top-words">
          <h4>高频词汇</h4>
          <ul>
            <li v-for="(count, word, index) in topWords" :key="index">
              {{ word }} ({{ count }})
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WordCloudResult",
  props: {
    data: {
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
    }
  },
  computed: {
    wordcloudData() {
      return this.data || null;
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
  padding: 20px;
}

.wordcloud-result h3 {
  margin-top: 0;
  color: #303133;
}

.loading, .error {
  text-align: center;
  padding: 40px 20px;
}

.loading p, .error p {
  font-size: 16px;
  color: #606266;
}

.result-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.wordcloud-image-container {
  flex: 1;
  min-width: 300px;
}

.wordcloud-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.wordcloud-info {
  flex: 1;
  min-width: 300px;
}

.wordcloud-info h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.wordcloud-info p {
  margin-bottom: 10px;
  color: #606266;
}

.top-words ul {
  list-style-type: none;
  padding: 0;
}

.top-words li {
  padding: 5px 0;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
}

.top-words li:last-child {
  border-bottom: none;
}
</style>