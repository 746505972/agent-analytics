<template>
  <div class="non-parametric-test-config">
    <div class="test-type-selector">
      <h3>非参数检验类型</h3>
      <div class="radio-group">
        <label v-for="type in testTypes" :key="type.value" class="radio-label">
          <input 
            type="radio" 
            :value="type.value" 
            v-model="localConfig.testType"
            @change="onConfigChange"
          >
          {{ type.label }}
        </label>
      </div>
    </div>

    <div class="non-parametric-config-content">
      <!-- Mann-Whitney U检验配置 -->
      <div v-if="localConfig.testType === 'mannwhitney'" class="config-section">
        <div class="form-group">
          <label class="section-title">分组列</label>
          <select 
            v-model="localConfig.groupBy" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="">请选择分组列</option>
            <option 
              v-for="column in categoricalColumns" 
              :key="column" 
              :value="column"
            >
              {{ column }}
            </option>
          </select>
          <p class="help-text">选择分组列以比较两组数据的分布差异</p>
        </div>
        
        <div class="form-group">
          <label class="section-title">检验方向</label>
          <select 
            v-model="localConfig.alternative" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="two-sided">双侧检验</option>
            <option value="less">左侧检验</option>
            <option value="greater">右侧检验</option>
          </select>
          <p class="help-text">双侧检验：检验两组数据分布是否不同；左侧检验：检验第一组数据分布是否小于第二组；右侧检验：检验第一组数据分布是否大于第二组</p>
        </div>
      </div>

      <!-- Wilcoxon符号秩检验配置 -->
      <div v-else-if="localConfig.testType === 'wilcoxon'" class="config-section">
        <p class="help-text">Wilcoxon符号秩检验用于比较两个相关样本的分布，需要选择恰好两个数值列</p>
        
        <div class="form-group">
          <label class="section-title">检验方向</label>
          <select 
            v-model="localConfig.alternative" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="two-sided">双侧检验</option>
            <option value="less">左侧检验</option>
            <option value="greater">右侧检验</option>
          </select>
          <p class="help-text">双侧检验：检验两列数据分布是否不同；左侧检验：检验第一列数据分布是否小于第二列；右侧检验：检验第一列数据分布是否大于第二列</p>
        </div>
      </div>

      <!-- Kruskal-Wallis检验配置 -->
      <div v-else-if="localConfig.testType === 'kruskal'" class="config-section">
        <div class="form-group">
          <label class="section-title">分组列（可选）</label>
          <select 
            v-model="localConfig.groupBy" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="">不使用分组（多列比较）</option>
            <option 
              v-for="column in categoricalColumns" 
              :key="column" 
              :value="column"
            >
              {{ column }}
            </option>
          </select>
          <p class="help-text">选择分组列以比较多个组之间的分布差异，或不选择以比较多个数值列</p>
        </div>
      </div>

      <!-- Kolmogorov-Smirnov检验配置 -->
      <div v-else-if="localConfig.testType === 'kolmogorov_smirnov'" class="config-section">
        <div class="form-group">
          <label class="section-title">检验类型</label>
          <select 
            v-model="localConfig.groupBy" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="">单样本检验（与理论分布比较）</option>
            <option 
              v-for="column in categoricalColumns" 
              :key="column" 
              :value="column"
            >
              两样本检验（{{ column }} 分组）
            </option>
          </select>
          <p class="help-text">单样本K-S检验：检验数据是否符合理论分布；两样本K-S检验：检验两组数据分布是否相同</p>
        </div>
        
        <div v-if="!localConfig.groupBy" class="form-group">
          <label class="section-title">理论分布</label>
          <select 
            v-model="localConfig.distribution" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="norm">正态分布</option>
            <option value="uniform">均匀分布</option>
            <option value="expon">指数分布</option>
            <option value="logistic">逻辑分布</option>
          </select>
          <p class="help-text">选择用于比较的理论分布类型</p>
        </div>
      </div>

      <!-- 显著性水平配置 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">显著性水平 (α)</label>
          <input 
            type="number" 
            v-model.number="localConfig.alpha" 
            @input="onConfigChange"
            step="0.01"
            min="0.001"
            max="0.1"
            class="form-control"
          >
          <p class="help-text">通常设置为0.05，表示5%的显著性水平</p>
        </div>
      </div>

      <!-- 方法描述 -->
      <div class="method-description">
        <div v-if="localConfig.testType === 'mannwhitney'">
          <h4>Mann-Whitney U检验</h4>
          <p>Mann-Whitney U检验（也称为Wilcoxon秩和检验）是一种非参数检验方法，用于比较两个独立样本的分布是否相同。它不需要假设数据服从正态分布，适用于偏态分布或有异常值的数据。</p>
          <p>原假设(H₀)：两个样本的分布相同</p>
          <p>备择假设(H₁)：两个样本的分布不同</p>
          <p class="formula">统计量U表示一组数据值领先于另一组数据值的次数</p>
        </div>
        
        <div v-else-if="localConfig.testType === 'wilcoxon'">
          <h4>Wilcoxon符号秩检验</h4>
          <p>Wilcoxon符号秩检验是一种非参数检验方法，用于比较两个相关样本（配对数据）的分布是否相同。它适用于配对数据，不假设数据服从正态分布。</p>
          <p>原假设(H₀)：两个相关样本的分布相同</p>
          <p>备择假设(H₁)：两个相关样本的分布不同</p>
          <p class="formula">统计量W基于配对差值的秩和符号</p>
        </div>
        
        <div v-else-if="localConfig.testType === 'kruskal'">
          <h4>Kruskal-Wallis检验</h4>
          <p>Kruskal-Wallis检验是Mann-Whitney U检验的扩展，用于比较三个或更多独立样本的分布是否相同。它是单因素方差分析(ANOVA)的非参数替代方法。</p>
          <p>原假设(H₀)：所有样本的分布相同</p>
          <p>备择假设(H₁)：至少有一个样本的分布与其他样本不同</p>
          <p class="formula">统计量H基于所有样本的秩和</p>
        </div>
        
        <div v-else-if="localConfig.testType === 'kolmogorov_smirnov'">
          <h4>Kolmogorov-Smirnov检验</h4>
          <p>Kolmogorov-Smirnov检验是一种非参数检验方法，用于检验样本分布与理论分布之间的差异（单样本K-S检验），或检验两个样本是否来自同一分布（两样本K-S检验）。</p>
          <p>原假设(H₀)：样本来自指定的理论分布（单样本）或两个样本来自同一分布（两样本）</p>
          <p>备择假设(H₁)：样本不来自指定的理论分布（单样本）或两个样本来自不同分布（两样本）</p>
          <p class="formula">统计量D是经验分布函数与理论分布函数之间的最大绝对差</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NonParametricTestConfig",
  props: {
    config: {
      type: Object,
      default: () => ({
        testType: 'mannwhitney',
        groupBy: '',
        alpha: 0.05,
        alternative: 'two-sided',
        distribution: 'norm'
      })
    },
    categoricalColumns: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localConfig: { ...this.config },
      testTypes: [
        { value: 'mannwhitney', label: 'Mann-Whitney U检验' },
        { value: 'wilcoxon', label: 'Wilcoxon符号秩检验' },
        { value: 'kruskal', label: 'Kruskal-Wallis检验' },
        { value: 'kolmogorov_smirnov', label: 'Kolmogorov-Smirnov检验' }
      ]
    };
  },
  watch: {
    config: {
      handler(newConfig) {
        this.localConfig = { ...newConfig };
      },
      deep: true
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
.non-parametric-test-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.test-type-selector {
  margin-bottom: 20px;
}

.test-type-selector h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.radio-label {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #606266;
}

.radio-label input {
  margin-right: 6px;
}

.config-section {
  margin-bottom: 15px;
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
  font-size: 13px;
  color: #909399;
  margin-top: 5px;
  margin-bottom: 0;
}

.method-description {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #409eff;
}

.method-description h4 {
  margin-top: 0;
  color: #303133;
}

.method-description p {
  line-height: 1.6;
  color: #606266;
}

.formula {
  font-family: 'Courier New', monospace;
  background-color: #e6f7ff;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 14px;
  color: #1890ff;
}

.formula-desc {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 5px;
  font-style: italic;
}
</style>