<template>
  <div class="f-test-config">
    <div class="f-test-config-content">
      <!-- 方法描述 -->
      <div class="method-description">
        <p>F检验主要用于检验多个样本的方差是否相等或进行方差分析(ANOVA)。它可以帮助判断不同组之间的均值是否存在显著差异。</p>
        <p>当数据满足正态性和方差齐性假设时，F检验的结果更加可靠。</p>
      </div>

      <div class="config-section">
        <div class="form-group">
          <label class="section-title">显著性水平 (α)</label>
          <input 
            type="number" 
            v-model.number="localConfig.alpha" 
            @input="onConfigChange"
            min="0.001" 
            max="0.1" 
            step="0.001"
            class="form-control"
          >
        </div>
      </div>

      <!-- 分组选项 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">分组列（可选）</label>
          <select 
            v-model="localConfig.groupBy" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="">不使用分组（方差齐性检验）</option>
            <option 
              v-for="column in categoricalColumns" 
              :key="column" 
              :value="column"
            >
              {{ column }}
            </option>
          </select>
          <p class="help-text">选择分组列后，将进行方差分析(ANOVA)；否则进行方差齐性检验</p>
        </div>
      </div>

      <!-- 检验方法说明 -->
      <div class="method-description">
        <div v-if="!localConfig.groupBy">
          <h4>方差齐性检验</h4>
          <p>方差齐性检验用于检验多个样本的方差是否相等。这是许多统计方法（如ANOVA、t检验）的重要前提条件。</p>
          <p>我们使用Levene检验来进行方差齐性检验，这种方法对数据的正态性假设要求较低，较为稳健。</p>
          <p>原假设(H₀)：各组数据的方差相等</p>
          <p>备择假设(H₁)：至少有两组数据的方差不相等</p>
        </div>
        <div v-else>
          <h4>方差分析(ANOVA)</h4>
          <p>方差分析用于检验三个或更多组的均值是否存在显著差异。它通过比较组间方差和组内方差来判断组间差异是否显著。</p>
          <p>原假设(H₀)：所有组的均值相等</p>
          <p>备择假设(H₁)：至少有两个组的均值不相等</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FTestConfig",
  props: {
    config: {
      type: Object,
      default: () => ({
        groupBy: '',
        alpha: 0.05
      })
    },
    categoricalColumns: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localConfig: { ...this.config }
    };
  },
  watch: {
    config: {
      handler(newConfig) {
        this.localConfig = { ...newConfig };
      },
      deep: true
    },
    categoricalColumns: {
      handler(newColumns) {
        // 检查当前选择的分组列是否仍在新的列列表中
        if (this.localConfig.groupBy && !newColumns.includes(this.localConfig.groupBy)) {
          // 如果不在，重置为不分组
          this.localConfig.groupBy = '';
          this.onConfigChange();
        }
      },
      immediate: true
    }
  },
  methods: {
    onConfigChange() {
      this.$emit('update:config', { ...this.localConfig });
    }
  }
};
</script>

<style scoped>
.f-test-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.f-test-config-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.config-section {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #606266;
}

.section-title {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #409eff;
}

.help-text {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
}

.method-description {
  background-color: #f5f5f5;
  border-left: 4px solid #409eff;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.method-description h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #303133;
}

.method-description p {
  margin: 0 0 5px 0;
}
</style>