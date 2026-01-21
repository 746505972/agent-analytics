<template>
  <div class="decision-tree-config">
    <h3>决策树配置</h3>
    
    <!-- 方法描述 -->
    <div class="method-description">
      <p>决策树 (Decision Tree) 是一种树形结构的分类和回归方法，通过一系列规则对数据进行分割，形成易于理解的决策路径。它通过递归地选择最优分割点，将数据集划分为更纯净的子集。</p>
      <h4>主要特点：</h4>
      <ul>
        <li>直观易懂：生成的模型具有良好的可解释性</li>
        <li>无需预处理：不需要对数据进行归一化或标准化</li>
        <li>处理混合数据：可以处理数值型和类别型数据</li>
        <li>自动特征选择：在分割过程中自动选择重要特征</li>
      </ul>
    </div>
    
    <!-- 任务类型选择 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">任务类型</label>
        <select 
          v-model="localConfig.task_type" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="auto">自动判断</option>
          <option value="classification">分类</option>
          <option value="regression">回归</option>
        </select>
      </div>
    </div>

    <!-- Y列选择 -->
    <div class="config-section" v-if="columns && columns.length > 0">
      <div class="form-group">
        <label class="section-title">因变量 (Y列)</label>
        <select 
          v-model="localConfig.y_column" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="">请选择</option>
          <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
        </select>
      </div>
    </div>

    <!-- 分割标准选择 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">分割标准</label>
        <select 
          v-model="localConfig.criterion" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="">默认</option>
          <!-- 分类任务标准 -->
          <optgroup label="分类任务标准" v-if="localConfig.task_type === 'classification' || localConfig.task_type === 'auto'">
            <option value="gini">基尼不纯度 (Gini Impurity)</option>
            <option value="entropy">信息熵 (Entropy)</option>
          </optgroup>
          <!-- 回归任务标准 -->
          <optgroup label="回归任务标准" v-if="localConfig.task_type === 'regression' || localConfig.task_type === 'auto'">
            <option value="squared_error">平方误差 (Squared Error)</option>
            <option value="absolute_error">绝对误差 (Absolute Error)</option>
            <option value="friedman_mse">Friedman MSE</option>
            <option value="poisson">泊松偏差 (Poisson)</option>
          </optgroup>
        </select>
      </div>
      <p class="form-help-text">分割准则：选择使信息增益最大（或基尼不纯度减少最多）的特征和分割点</p>
      <p class="form-help-text">对于分类：信息增益 = 熵(父节点) - Σ(子节点权重 × 熵(子节点))</p>
      <p class="form-help-text">对于回归：选择使方差减少最多的分割点</p>
    </div>

    <!-- 模型参数配置 -->
    <div class="config-section">
      <h4>模型参数</h4>
      
      <!-- 树的最大深度 -->
      <div class="form-group">
        <label class="section-title">树的最大深度 (max_depth)</label>
        <input 
          type="number" 
          v-model.number="localConfig.max_depth" 
          class="form-control"
          min="1"
          max="50"
          @input="updateConfig"
          placeholder="留空表示无限制"
        />
        <p class="form-help-text">控制树的最大深度，防止过拟合。较小的值可能导致欠拟合，较大的值可能导致过拟合。</p>
      </div>

      <!-- 内部节点分裂所需的最小样本数 -->
      <div class="form-group">
        <label class="section-title">内部节点分裂最小样本数 (min_samples_split)</label>
        <input 
          type="number" 
          v-model.number="localConfig.min_samples_split" 
          class="form-control"
          min="2"
          @input="updateConfig"
        />
        <p class="form-help-text">内部节点进行分裂所需的最小样本数。较大的值有助于防止过拟合。</p>
      </div>

      <!-- 叶节点所需的最小样本数 -->
      <div class="form-group">
        <label class="section-title">叶节点最小样本数 (min_samples_leaf)</label>
        <input 
          type="number" 
          v-model.number="localConfig.min_samples_leaf" 
          class="form-control"
          min="1"
          @input="updateConfig"
        />
        <p class="form-help-text">叶节点所需的最小样本数。较大的值有助于防止过拟合。</p>
      </div>

      <!-- 寻找最佳分割时考虑的特征数量 -->
      <div class="form-group">
        <label class="section-title">特征数量策略 (max_features)</label>
        <select 
          v-model="localConfig.max_features" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="">使用所有特征</option>
          <option value="sqrt">sqrt(n_features)</option>
          <option value="log2">log2(n_features)</option>
        </select>
        <p class="form-help-text">寻找最佳分割时考虑的特征数量。较小的值有助于防止过拟合。</p>
      </div>

      <!-- 随机种子 -->
      <div class="form-group">
        <label class="section-title">随机种子 (random_state)</label>
        <input 
          type="number" 
          v-model.number="localConfig.random_state" 
          class="form-control"
          min="0"
          @input="updateConfig"
        />
        <p class="form-help-text">控制随机性，确保结果可重现</p>
      </div>
    </div>

    <!-- 其他参数 -->
    <div class="config-section">
      <h4>其他参数</h4>
      <div class="form-group">
        <label class="section-title">其他决策树参数 (JSON格式)</label>
        <textarea 
          v-model="localConfig.params" 
          class="form-control"
          placeholder='例如: {"min_impurity_decrease": 0.01, "ccp_alpha": 0.0}'
          @input="updateParams"
          rows="4"
        ></textarea>
        <p class="form-help-text">以JSON格式输入其他决策树参数</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DecisionTreeConfig",
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
    }
  },
  watch: {
    config: {
      handler(newConfig) {
        this.localConfig = { ...newConfig }
      },
      deep: true
    }
  },
  methods: {
    updateConfig() {
      this.$emit('update:config', { ...this.localConfig })
    },
    updateParams() {
      try {
        // 尝试解析JSON
        if (this.localConfig.params && typeof this.localConfig.params === 'string') {
          this.localConfig.params = JSON.parse(this.localConfig.params)
        }
        this.updateConfig()
      } catch (e) {
        // 如果解析失败，保留原始字符串（如果需要的话）
        // this.localConfig.params = this.localConfig.params
        this.updateConfig()
      }
    }
  }
}
</script>

<style scoped>
.decision-tree-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
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

.method-description ul {
  margin: 5px 0;
  padding-left: 20px;
}

.radio-label input[type="radio"] {
  margin-right: 5px;
}

.form-help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}
</style>