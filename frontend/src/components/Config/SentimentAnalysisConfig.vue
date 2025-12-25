<template>
  <div class="sentiment-analysis-config">
    <h3>情感分析配置</h3>
    
    <div class="config-item">
      <label>自定义停用词（每行一个）：</label>
      <textarea
        v-model="stopwordsText"
        @change="onConfigChange"
        placeholder="每行输入一个停用词"
        class="stopwords-textarea"
      ></textarea>
      <p class="help-text">这些词语将在情感分析时被忽略</p>
    </div>
    
    <div class="config-item">
      <label>网络用语映射（每行一个，格式：网络用语=含义）：</label>
      <textarea
        v-model="internetSlangText"
        @change="onConfigChange"
        placeholder="例如：智齿=支持&#10;yyds=永远的神"
        class="slang-textarea"
      ></textarea>
      <p class="help-text">自定义网络用语及其对应的标准含义</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "SentimentAnalysisConfig",
  props: {
    selectedFileColumns: {
      type: Array,
      default: () => []
    },
    sentimentConfig: {
      type: Object,
      default: () => ({
        column: "",
        stopwords: [],
        internetSlang: {}
      })
    }
  },
  emits: ["update:sentimentConfig"],
  data() {
    return {
      selectedColumn: this.sentimentConfig.column || "",
      stopwordsText: this.sentimentConfig.stopwords ? this.sentimentConfig.stopwords.join('\n') : "",
      internetSlangText: this.formatInternetSlang(this.sentimentConfig.internetSlang) || ""
    };
  },
  computed: {
    // 只显示文本类型的列
    textColumns() {
      // 在实际应用中，可能需要根据列的数据类型进行过滤
      // 这里暂时返回所有列
      return this.selectedFileColumns;
    }
  },
  methods: {
    formatInternetSlang(slangObj) {
      if (!slangObj) return "";
      return Object.entries(slangObj)
        .map(([key, value]) => `${key}=${value}`)
        .join('\n');
    },
    
    parseInternetSlang(text) {
      if (!text) return {};
      const slang = {};
      text.split('\n')
        .filter(line => line.trim() !== '' && line.includes('='))
        .forEach(line => {
          const [key, value] = line.split('=');
          if (key && value) {
            slang[key.trim()] = value.trim();
          }
        });
      return slang;
    },
    
    onColumnChange() {
      this.onConfigChange();
    },
    
    onConfigChange() {
      const config = {
        column: this.selectedColumn,
        stopwords: this.stopwordsText ? this.stopwordsText.split('\n').filter(w => w.trim() !== '') : [],
        internetSlang: this.parseInternetSlang(this.internetSlangText)
      };
      this.$emit("update:sentimentConfig", config);
    }
  },
  watch: {
    sentimentConfig: {
      handler(newConfig) {
        this.selectedColumn = newConfig.column || "";
        this.stopwordsText = newConfig.stopwords ? newConfig.stopwords.join('\n') : "";
        this.internetSlangText = this.formatInternetSlang(newConfig.internetSlang) || "";
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.sentiment-analysis-config {
  padding: 20px;
  background: white;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.sentiment-analysis-config h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
}

.config-item {
  margin-bottom: 20px;
}

.config-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #606266;
}

.column-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.column-select:focus {
  outline: none;
  border-color: #409eff;
}

.stopwords-textarea,
.slang-textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
}

.stopwords-textarea:focus,
.slang-textarea:focus {
  outline: none;
  border-color: #409eff;
}

.help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}
</style>