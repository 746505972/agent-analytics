<template>
  <div class="linear-regression-config">
    <div class="linear-regression-type-selector">
      <h3>线性回归方法</h3>
      <div class="radio-group">
        <label v-for="method in regressionMethods" :key="method.value" class="radio-label">
          <input 
            type="radio" 
            :value="method.value" 
            v-model="localConfig.method"
            @change="onConfigChange"
          >
          {{ method.label }}
        </label>
      </div>
    </div>

    <div class="linear-regression-config-content">
      <!-- 方法描述 -->
      <div class="method-description" v-if="localConfig.method === 'ols'">
        <p>普通最小二乘法 (OLS)：通过最小化误差平方和来估计模型参数。适用于数据无多重共线性且样本量充足的情况。</p>
        <p class="formula">公式：β̂ = (XᵀX)⁻¹Xᵀy</p>
        <p class="formula-desc">其中X是自变量矩阵，y是因变量向量，β̂是参数估计值</p>
      </div>
      <div class="method-description" v-else-if="localConfig.method === 'lasso'">
        <p>Lasso回归 (L1正则化)：在OLS基础上添加L1正则化项，可以进行特征选择，使部分参数变为0。适用于高维数据和特征选择场景。</p>
        <p class="formula">公式：min ||y - Xβ||²₂ + α||β||₁</p>
        <p class="formula-desc">其中α是正则化强度，||β||₁是参数的L1范数</p>
      </div>
      <div class="method-description" v-else-if="localConfig.method === 'ridge'">
        <p>Ridge回归 (L2正则化)：在OLS基础上添加L2正则化项，可以处理多重共线性问题。适用于自变量间存在较强相关性的情况。</p>
        <p class="formula">公式：min ||y - Xβ||²₂ + α||β||²₂</p>
        <p class="formula-desc">其中α是正则化强度，||β||²₂是参数的L2范数</p>
      </div>
      <div class="method-description" v-else-if="localConfig.method === 'elastic_net'">
        <p>ElasticNet回归：结合L1和L2正则化的线性回归模型，综合了Lasso和Ridge的优点。适用于高维数据和特征间存在组效应的情况。</p>
        <p class="formula">公式：min ||y - Xβ||²₂ + αρ||β||₁ + α(1-ρ)||β||²₂</p>
        <p class="formula-desc">其中α是正则化强度，ρ是L1正则化比例，控制L1和L2正则化的平衡</p>
      </div>

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

      <div class="config-section">
        <div class="form-group">
          <label class="section-title">正则化强度 (Alpha)</label>
          <input 
            type="number" 
            v-model.number="localConfig.alpha" 
            @input="onConfigChange"
            :step="0.1"
            :min="0"
            :disabled="localConfig.method === 'ols'"
            class="form-control"
          >
          <p class="form-help-text">
            控制正则化项的强度，值越大正则化越强 (仅适用于Lasso、Ridge、ElasticNet)
          </p>
        </div>
      </div>

      <div class="config-section" v-if="localConfig.method === 'elastic_net'">
        <div class="form-group">
          <label class="section-title">L1正则化比例</label>
          <input 
            type="number" 
            v-model.number="localConfig.l1_ratio" 
            @input="onConfigChange"
            :step="0.1"
            :min="0"
            :max="1"
            class="form-control"
          >
          <p class="form-help-text">
            ElasticNet中L1正则化的比例，0表示纯Ridge，1表示纯Lasso
          </p>
        </div>
      </div>



      <div class="config-section" v-if="localConfig.method !== 'ols'">
        <div class="form-group">
          <label class="section-title">最大迭代次数</label>
          <input 
            type="number" 
            v-model.number="localConfig.params.max_iter" 
            @input="onConfigChange"
            :min="1"
            class="form-control"
          >
        </div>
      </div>

      <div class="config-section" v-if="localConfig.method !== 'ols'">
        <div class="form-group">
          <label class="section-title">收敛容差</label>
          <input 
            type="number" 
            v-model.number="localConfig.params.tol" 
            @input="onConfigChange"
            :step="0.0001"
            :min="0"
            class="form-control"
          >
        </div>
      </div>

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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LinearRegressionConfig',
  props: {
    config: {
      type: Object,
      default: () => ({
        y_column: '',
        method: 'ols',
        alpha: 1.0,
        l1_ratio: 0.5,
        params: {
          max_iter: 1000,
          tol: 0.0001,
          fit_intercept: true
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
      localConfig: { ...this.config },
      regressionMethods: [
        { value: 'ols', label: '普通最小二乘法 (OLS)' },
        { value: 'lasso', label: 'Lasso回归 (L1正则化)' },
        { value: 'ridge', label: 'Ridge回归 (L2正则化)' },
        { value: 'elastic_net', label: 'ElasticNet回归 (弹性网络)' }
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
  },
  mounted() {
    this.$emit('update:config', this.localConfig);
  }
};
</script>

<style scoped>
.linear-regression-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.linear-regression-type-selector {
  margin-bottom: 20px;
}

.linear-regression-type-selector h3 {
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

.linear-regression-config-content {
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

.form-help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
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

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin-right: 5px;
}
</style>