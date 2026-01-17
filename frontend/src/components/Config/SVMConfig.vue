<template>
  <div class="svm-config-container">
    <h4>SVM 参数配置</h4>
    
    <div class="config-section">
      <label class="config-label">任务类型</label>
      <select 
        class="config-input" 
        :value="localConfig.task_type" 
        @input="$emit('update:config', { ...localConfig, task_type: $event.target.value })"
      >
        <option value="classification">分类 (Classification)</option>
        <option value="regression">回归 (Regression)</option>
      </select>
    </div>

    <div class="config-section">
      <label class="config-label">目标列 (Y)</label>
      <select 
        class="config-input" 
        :value="localConfig.y_column" 
        @input="$emit('update:config', { ...localConfig, y_column: $event.target.value })"
      >
        <option value="">请选择目标列</option>
        <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
      </select>
    </div>

    <div class="config-section">
      <label class="config-label">核函数类型</label>
      <select 
        class="config-input" 
        :value="localConfig.kernel" 
        @input="$emit('update:config', { ...localConfig, kernel: $event.target.value })"
      >
        <option value="rbf">RBF (径向基函数)</option>
        <option value="linear">Linear (线性)</option>
        <option value="poly">Polynomial (多项式)</option>
        <option value="sigmoid">Sigmoid</option>
      </select>
    </div>

    <div class="config-section">
      <label class="config-label">正则化参数 C</label>
      <input 
        type="number" 
        class="config-input" 
        :value="localConfig.C" 
        @input="$emit('update:config', { ...localConfig, C: parseFloat($event.target.value) || 1.0 })"
        step="0.1"
        min="0.01"
        placeholder="默认: 1.0"
      />
      <small class="help-text">C值越大，对误分类的惩罚越大</small>
    </div>

    <div class="config-section">
      <label class="config-label">Gamma 参数</label>
      <select 
        class="config-input" 
        :value="localConfig.gamma" 
        @input="$emit('update:config', { ...localConfig, gamma: $event.target.value })"
      >
        <option value="scale">scale (1/(n_features * X.var()))</option>
        <option value="auto">auto (1/n_features)</option>
        <option value="0.1">0.1</option>
        <option value="0.01">0.01</option>
        <option value="0.001">0.001</option>
      </select>
      <small class="help-text">仅对 RBF, Polynomial 和 Sigmoid 核函数有效</small>
    </div>

    <div v-if="localConfig.kernel === 'poly'" class="config-section">
      <label class="config-label">多项式度数 (Degree)</label>
      <input 
        type="number" 
        class="config-input" 
        :value="localConfig.degree" 
        @input="$emit('update:config', { ...localConfig, degree: parseInt($event.target.value) || 3 })"
        min="1"
        max="10"
        placeholder="默认: 3"
      />
      <small class="help-text">仅对 Polynomial 核函数有效</small>
    </div>

    <div v-if="['poly', 'sigmoid'].includes(localConfig.kernel)" class="config-section">
      <label class="config-label">Coefficient 0</label>
      <input 
        type="number" 
        class="config-input" 
        :value="localConfig.coef0" 
        @input="$emit('update:config', { ...localConfig, coef0: parseFloat($event.target.value) || 0.0 })"
        step="0.1"
        placeholder="默认: 0.0"
      />
      <small class="help-text">仅对 Polynomial 和 Sigmoid 核函数有效</small>
    </div>

    <div class="config-section">
      <label class="config-label">容忍度 (Tolerance)</label>
      <input 
        type="number" 
        class="config-input" 
        :value="localConfig.tol" 
        @input="$emit('update:config', { ...localConfig, tol: parseFloat($event.target.value) || 1e-3 })"
        step="1e-4"
        min="1e-6"
        placeholder="默认: 0.001"
      />
      <small class="help-text">停止准则的容忍度</small>
    </div>

    <div class="config-section">
      <label class="config-label">最大迭代次数</label>
      <input 
        type="number" 
        class="config-input" 
        :value="localConfig.max_iter" 
        @input="$emit('update:config', { ...localConfig, max_iter: parseInt($event.target.value) || -1 })"
        placeholder="默认: -1 (无限制)"
      />
      <small class="help-text">-1 表示无限制</small>
    </div>

    <div class="config-section">
      <label class="config-label">使用启发式收缩</label>
      <select 
        class="config-input" 
        :value="localConfig.shrinking" 
        @input="$emit('update:config', { ...localConfig, shrinking: $event.target.value === 'true' })"
      >
        <option :value="true">是</option>
        <option :value="false">否</option>
      </select>
    </div>

    <div v-if="localConfig.task_type === 'classification'" class="config-section">
      <label class="config-label">启用概率预测</label>
      <select 
        class="config-input" 
        :value="localConfig.probability" 
        @input="$emit('update:config', { ...localConfig, probability: $event.target.value === 'true' })"
      >
        <option :value="true">是</option>
        <option :value="false">否</option>
      </select>
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
  }
};
</script>

<style scoped>
.svm-config-container {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.config-section {
  margin-bottom: 20px;
}

.config-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #495057;
}

.config-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
}

.config-input:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.help-text {
  display: block;
  color: #6c757d;
  font-size: 0.875em;
  margin-top: 4px;
}
</style>