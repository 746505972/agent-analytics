<template>
  <div class="wordcloud-config">
    <h3>词云配置</h3>
    <div class="config-item">
      <label>选择文本列：</label>
      <select 
        v-model="selectedColumn" 
        @change="onColumnChange"
        class="column-select"
      >
        <option value="" disabled>请选择一列</option>
        <option 
          v-for="column in textColumns" 
          :key="column" 
          :value="column"
        >
          {{ column }}
        </option>
      </select>
      <p class="help-text">请选择包含文本数据的一列用于生成词云</p>
    </div>
    
    <div class="config-item">
      <label>最大词数：</label>
      <input 
        type="number" 
        v-model.number="maxWords" 
        @change="onConfigChange"
        min="10" 
        max="500" 
        class="number-input"
      />
    </div>
    
    <div class="config-item">
      <label>图片宽度：</label>
      <input 
        type="number" 
        v-model.number="width" 
        @change="onConfigChange"
        min="200" 
        max="3000" 
        class="number-input"
      />
      <p class="help-text">词云图片的宽度（像素）</p>
    </div>
    
    <div class="config-item">
      <label>图片高度：</label>
      <input 
        type="number" 
        v-model.number="height" 
        @change="onConfigChange"
        min="200" 
        max="3000" 
        class="number-input"
      />
      <p class="help-text">词云图片的高度（像素）</p>
    </div>
    
    <div class="config-item">
      <label>背景颜色：</label>
      <input 
        type="color" 
        v-model="backgroundColor" 
        @change="onConfigChange"
        class="color-picker"
      />
    </div>
    
    <div class="config-item">
      <label>自定义停用词（每行一个）：</label>
      <textarea
        v-model="stopwordsText"
        @change="onConfigChange"
        placeholder="每行输入一个停用词"
        class="stopwords-textarea"
      ></textarea>
      <p class="help-text">这些词语将在生成词云时被忽略</p>
    </div>
    
    <div class="config-item">
      <label>蒙版形状：</label>
      <select 
        v-model="maskShape" 
        @change="onConfigChange"
        class="shape-select"
      >
        <option value="default">默认</option>
        <option value="circle">圆形</option>
        <option value="heart">心形</option>
        <option value="star">星形</option>
        <option value="cloud">云朵形</option>
      </select>
    </div>

    <div class="config-item">
      <label>最大字体大小：</label>
      <input
        type="number"
        v-model.number="maxFontSize"
        @change="onConfigChange"
        min="10"
        max="500"
        class="number-input"
      />
    </div>

    <div class="config-item">
      <label>最小字体大小：</label>
      <input
        type="number"
        v-model.number="minFontSize"
        @change="onConfigChange"
        min="1"
        max="100"
        class="number-input"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "WordCloudConfig",
  props: {
    selectedFileColumns: {
      type: Array,
      default: () => []
    },
    wordcloudConfig: {
      type: Object,
      default: () => ({
        column: "",
        maxWords: 200,
        width: 1600,
        height: 900,
        backgroundColor: "#ffffff",
        maxFontSize: 200,
        minFontSize: 10,
        stopwords: [],
        maskShape: "default"
      })
    }
  },
  emits: ["update:wordcloudConfig"],
  data() {
    return {
      selectedColumn: this.wordcloudConfig.column || "",
      maxWords: this.wordcloudConfig.maxWords || 200,
      width: this.wordcloudConfig.width || 1600,
      height: this.wordcloudConfig.height || 900,
      backgroundColor: this.wordcloudConfig.backgroundColor || "#ffffff",
      maxFontSize: this.wordcloudConfig.maxFontSize || 200,
      minFontSize: this.wordcloudConfig.minFontSize || 10,
      stopwordsText: this.wordcloudConfig.stopwords ? this.wordcloudConfig.stopwords.join('\n') : "",
      maskShape: this.wordcloudConfig.maskShape || "default"
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
    onColumnChange() {
      this.onConfigChange();
    },
    
    onConfigChange() {
      const config = {
        column: this.selectedColumn,
        maxWords: this.maxWords,
        width: this.width,
        height: this.height,
        backgroundColor: this.backgroundColor,
        maxFontSize: this.maxFontSize,
        minFontSize: this.minFontSize,
        stopwords: this.stopwordsText ? this.stopwordsText.split('\n').filter(w => w.trim() !== '') : [],
        maskShape: this.maskShape
      };
      this.$emit("update:wordcloudConfig", config);
    }
  },
  watch: {
    wordcloudConfig: {
      handler(newConfig) {
        this.selectedColumn = newConfig.column || "";
        this.maxWords = newConfig.maxWords || 200;
        this.width = newConfig.width || 1600;
        this.height = newConfig.height || 900;
        this.backgroundColor = newConfig.backgroundColor || "#ffffff";
        this.maxFontSize = newConfig.maxFontSize || 200;
        this.minFontSize = newConfig.minFontSize || 10;
        this.stopwordsText = newConfig.stopwords ? newConfig.stopwords.join('\n') : "";
        this.maskShape = newConfig.maskShape || "default";
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.wordcloud-config {
  padding: 20px;
  background: white;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.wordcloud-config h3 {
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

.column-select,
.shape-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.column-select:focus,
.shape-select:focus {
  outline: none;
  border-color: #409eff;
}

.number-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.number-input:focus {
  outline: none;
  border-color: #409eff;
}

.color-picker {
  width: 100%;
  height: 40px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.stopwords-textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
}

.stopwords-textarea:focus {
  outline: none;
  border-color: #409eff;
}

.help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}
</style>