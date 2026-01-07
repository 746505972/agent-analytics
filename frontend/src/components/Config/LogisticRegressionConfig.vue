<template>
  <div class="logistic-regression-config">
    <div class="logistic-regression-type-selector">
      <h3>逻辑回归方法</h3>
      <div class="radio-group">
        <label class="radio-label">
          <input 
            type="radio" 
            value="logistic" 
            v-model="localConfig.method"
            @change="onConfigChange"
          >
          逻辑回归
        </label>
      </div>
    </div>

    <div class="logistic-regression-config-content">
      <!-- 方法描述 -->
      <div class="method-description">
        <p>逻辑回归：用于二分类或多分类问题，通过逻辑函数将线性回归输出映射到0-1区间，表示概率。</p>
        <p class="formula">公式：P(Y=1|X) = 1 / (1 + e^(-(β₀ + β₁X₁ + ... + βₙXₙ)))</p>
        <p class="formula-desc">其中X是自变量，β是参数，P(Y=1|X)是给定X条件下Y=1的概率</p>
      </div>

      <!-- 因变量选择 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">因变量 (Y)</label>
          <select
            v-model="localConfig.y_column"
            @change="onConfigChange"
            class="form-control">
            <option value="">请选择</option>
            <option
              v-for="col in availableColumns"
              :key="col"
              :value="col"
            >
              {{ col }}
            </option>
          </select>
        </div>
      </div>

      <!-- 正则化参数 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">正则化强度 (C)</label>
          <input 
            type="number" 
            v-model.number="localConfig.params.C"
            @input="onConfigChange"
            step="0.1"
            min="0.01"
            class="form-control"
            :title="'正则化强度的倒数，值越小正则化越强'"
          >
          <p class="form-help-text">
            正则化强度的倒数，值越小正则化越强
          </p>
        </div>
      </div>

      <!-- 算法选择 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">优化算法</label>
          <select 
            v-model="localConfig.solver" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="lbfgs">L-BFGS</option>
            <option value="liblinear">Liblinear</option>
            <option value="newton-cg">Newton-CG</option>
            <option value="sag">SAG</option>
            <option value="saga">SAGA</option>
          </select>
        </div>
      </div>

      <!-- 迭代次数 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">最大迭代次数</label>
          <input 
            type="number" 
            v-model.number="localConfig.params.max_iter"
            @input="onConfigChange"
            min="100"
            step="100"
            class="form-control"
          >
        </div>
      </div>

      <!-- 高级参数 -->
      <div class="config-section">
        <div class="form-group">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="localConfig.params.fit_intercept" 
              @change="onConfigChange"
            > 拟合截距
          </label>
        </div>
        <div class="form-group">
          <label class="section-title">类别权重</label>
          <select 
            v-model="localConfig.params.class_weight" 
            @change="onConfigChange"
            class="form-control"
          >
            <option :value="null">无</option>
            <option value="balanced">平衡</option>
          </select>
        </div>
        <div class="form-group">
          <label class="section-title">收敛容差</label>
          <input 
            type="number" 
            v-model.number="localConfig.params.tol"
            @input="onConfigChange"
            step="0.0001"
            min="0.0001"
            class="form-control"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LogisticRegressionConfig',
  props: {
    config: {
      type: Object,
      default: () => ({
        y_column: '',
        method: 'logistic',
        solver: 'lbfgs',
        params: {
          C: 1.0,
          max_iter: 1000,
          tol: 0.0001,
          fit_intercept: true,
          class_weight: null
        }
      })
    },
    availableColumns: {
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
    }
  },
  methods: {
    onConfigChange() {
      this.$emit('update:config', { ...this.localConfig });
    }
  },
  mounted() {
    this.$emit('update:config', this.localConfig);
  }
};
</script>

<style scoped>
.logistic-regression-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.logistic-regression-type-selector {
  margin-bottom: 20px;
}

.logistic-regression-type-selector h3 {
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
  font-weight: normal;
  cursor: pointer;
  margin-right: 15px;
}

.radio-label input[type="radio"] {
  margin-right: 5px;
}

.logistic-regression-config-content {
  flex: 1;
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

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 5px;
}

.method-description {
  background-color: #f5f5f5;
  border-left: 4px solid #409eff;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.method-description p {
  margin: 0 0 5px 0;
}

.method-description .formula {
  font-family: 'Cambria Math', 'Arial Unicode MS', serif;
  margin: 5px 0;
}

.method-description .formula-desc {
  font-size: 12px;
  color: #888;
  margin: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}
</style>