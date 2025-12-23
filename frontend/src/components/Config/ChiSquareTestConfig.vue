<template>
  <div class="chi-square-test-config">
    <div class="chi-square-test-config-content">
      <!-- 方法描述 -->
      <div class="method-description">
        <p>卡方检验主要用于检验分类变量之间的独立性或拟合优度。它可以帮助判断两个分类变量是否相关，或者观测频数与期望频数是否存在显著差异。</p>
        <p>卡方检验适用于分类数据，对于连续数据需要先进行离散化处理。</p>
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
            <option value="">不使用分组（拟合优度检验）</option>
            <option 
              v-for="column in categoricalColumns" 
              :key="column" 
              :value="column"
            >
              {{ column }}
            </option>
          </select>
          <p class="help-text">选择分组列后，将进行独立性检验；否则进行拟合优度检验</p>
        </div>
      </div>

      <!-- 检验方法说明 -->
      <div class="method-description">
        <div v-if="!localConfig.groupBy">
          <h4>拟合优度检验</h4>
          <p>拟合优度检验用于检验观测频数与期望频数是否一致。默认检验各类别的观测频数是否均匀分布。</p>
          <p>原假设(H₀)：观测频数与期望频数一致</p>
          <p>备择假设(H₁)：观测频数与期望频数不一致</p>
        </div>
        <div v-else>
          <h4>独立性检验</h4>
          <p>独立性检验用于检验两个分类变量是否相互独立。通过构建列联表来分析两个变量之间的关联性。</p>
          <p>原假设(H₀)：两个变量相互独立</p>
          <p>备择假设(H₁)：两个变量不独立（存在关联）</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChiSquareTestConfig",
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
.chi-square-test-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.chi-square-test-config-content {
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