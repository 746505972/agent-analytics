<template>
  <div class="svm-config-container">
    <h3>SVM 参数配置</h3>
    
    <div class="svm-config-content">
      <!-- 方法描述 -->
      <div class="method-description" v-if="localConfig.task_type === 'classification'">
        <p>支持向量机分类 (SVM Classification)：一种监督学习算法，通过寻找最优超平面来分离不同类别的数据点。特别适用于高维空间中的分类问题。</p>
        <p class="formula">决策函数：f(x) = sign(Σ αᵢyᵢK(xᵢ,x) + b)</p>
        <p class="formula-desc">其中αᵢ是拉格朗日乘数，yᵢ是训练样本标签，K是核函数，b是偏置项</p>
      </div>
      <div class="method-description" v-else-if="localConfig.task_type === 'regression'">
        <p>支持向量机回归 (SVM Regression)：支持向量机也可用于回归问题，称为支持向量回归(SVR)。目标是找到一个函数，使得大部分样本都在ε-管内，同时保持函数尽可能平坦。</p>
        <p class="formula">回归函数：f(x) = Σ (αᵢ - αᵢ*)K(xᵢ,x) + b</p>
        <p class="formula-desc">其中αᵢ和αᵢ*是拉格朗日乘数，K是核函数，b是偏置项</p>
      </div>

      <!-- 任务类型选择 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">任务类型</label>
          <select 
            v-model="localConfig.task_type"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="classification">分类 (Classification)</option>
            <option value="regression">回归 (Regression)</option>
          </select>
        </div>
      </div>

      <!-- 目标列选择 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">目标列 (Y)</label>
          <select 
            v-model="localConfig.y_column"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="">请选择目标列</option>
            <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
          </select>
        </div>
      </div>

      <!-- 核函数类型 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">核函数类型</label>
          <select 
            v-model="localConfig.kernel"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="rbf">RBF (径向基函数)</option>
            <option value="linear">Linear (线性)</option>
            <option value="poly">Polynomial (多项式)</option>
            <option value="sigmoid">Sigmoid</option>
          </select>
        </div>
      </div>
      <div class="method-description">
        <div v-if="localConfig.kernel === 'linear'">
          <p><strong>线性核 (Linear)</strong>：K(x,xi) = x·xi，适用于线性可分的数据集，计算简单高效。</p>
        </div>
        <div v-if="localConfig.kernel === 'rbf'">
          <p><strong>RBF核 (径向基函数)</strong>：K(x,xi) = exp(-γ||x-xi||²)，能够处理非线性问题，是最常用的核函数之一。</p>
        </div>
        <div v-if="localConfig.kernel === 'poly'">
          <p><strong>多项式核</strong>：K(x,xi) = (γ*x·xi + r)^d，适用于适度复杂的非线性问题，d为多项式的度数。</p>
        </div>
        <div v-if="localConfig.kernel === 'sigmoid'">
          <p><strong>Sigmoid核</strong>：K(x,xi) = tanh(γ*x·xi + r)，类似神经网络中的激活函数，适用于某些特殊类型的非线性问题。</p>
        </div>
      </div>
      <!-- SVM特定参数 -->
      <div class="config-section">
        <div class="form-group">
          <label class="section-title">正则化参数 C</label>
          <input 
            type="number" 
            v-model.number="localConfig.C"
            @input="onConfigChange"
            step="0.1"
            min="0.01"
            class="form-control"
            placeholder="默认: 1.0"
          />
          <p class="form-help-text"><strong>C (正则化参数)</strong>：控制对误分类的惩罚程度，C值越大对误分类的容忍度越低，可能导致过拟合。</p>
        </div>

        <div class="form-group">
          <label class="section-title">Gamma 参数</label>
          <select 
            v-model="localConfig.gamma"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="scale">scale (1/(n_features * X.var()))</option>
            <option value="auto">auto (1/n_features)</option>
            <option value="0.1">0.1</option>
            <option value="0.01">0.01</option>
            <option value="0.001">0.001</option>
          </select>
          <p class="form-help-text"><strong>Gamma</strong>：决定单个训练样本的影响范围，gamma值越大影响范围越小，可能导致过拟合。</p>
          <p class="form-help-text">仅对 RBF, Polynomial 和 Sigmoid 核函数有效</p>
        </div>

        <!-- 多项式度数 (仅对poly核有效) -->
        <div v-if="localConfig.kernel === 'poly'" class="form-group">
          <label class="section-title">多项式度数 (Degree)</label>
          <input 
            type="number" 
            v-model.number="localConfig.degree"
            @input="onConfigChange"
            min="1"
            max="10"
            class="form-control"
            placeholder="默认: 3"
          />
          <p class="form-help-text">仅对 Polynomial 核函数有效</p>
        </div>

        <!-- Coefficient 0 (仅对poly和sigmoid核有效) -->
        <div v-if="['poly', 'sigmoid'].includes(localConfig.kernel)" class="form-group">
          <label class="section-title">Coefficient 0</label>
          <input 
            type="number" 
            v-model.number="localConfig.coef0"
            @input="onConfigChange"
            step="0.1"
            class="form-control"
            placeholder="默认: 0.0"
          />
          <p class="form-help-text">仅对 Polynomial 和 Sigmoid 核函数有效</p>
        </div>

        <div class="form-group">
          <label class="section-title">容忍度 (Tolerance)</label>
          <input 
            type="number" 
            v-model.number="localConfig.tol"
            @input="onConfigChange"
            step="1e-4"
            min="1e-6"
            class="form-control"
            placeholder="默认: 0.001"
          />
          <p class="form-help-text">停止准则的容忍度</p>
        </div>

        <div class="form-group">
          <label class="section-title">最大迭代次数</label>
          <input 
            type="number" 
            v-model.number="localConfig.max_iter"
            @input="onConfigChange"
            class="form-control"
            placeholder="默认: -1 (无限制)"
          />
          <p class="form-help-text">-1 表示无限制</p>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="localConfig.shrinking"
              @change="onConfigChange"
            >
            使用启发式收缩
          </label>
        </div>

        <!-- 概率预测 (仅对分类任务有效) -->
        <div v-if="localConfig.task_type === 'classification'" class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="localConfig.probability"
              @change="onConfigChange"
            >
            启用概率预测
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SVMConfig',
  props: {
    config: {
      type: Object,
      required: true
    },
    columns: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:config'],
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
.svm-config-container {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.svm-config-content {
  flex: 1;
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

.method-description h4 {
  margin: 0 0 5px 0;
  color: #303133;
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