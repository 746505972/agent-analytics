<template>
  <div class="xgboost-config">
    <h3>XGBoost配置</h3>
    
    <!-- 方法描述 -->
    <div class="method-description">
      <p>XGBoost (Extreme Gradient Boosting) 是一种高效的梯度提升算法实现，广泛应用于机器学习竞赛和实际项目中。它通过对多个弱预测模型(通常是决策树)的组合来构建强预测模型。</p>
      <p class="formula">公式：ŷᵢ = w₀ + Σᵢ₌₁ᵀ fₜ(xᵢ), 其中 fₜ ∈ F</p>
      <p class="formula-desc">其中ŷᵢ是预测值，w₀是基线预测，fₜ是第t个弱学习器，F是所有可能的弱学习器集合</p>
      <h4>主要优势：</h4>
      <ul>
        <li>高效性：具有高度优化的内存管理和计算性能</li>
        <li>准确性：采用梯度提升框架，预测精度高</li>
        <li>灵活性：支持多种目标函数和评价指标</li>
        <li>鲁棒性：内置正则化项防止过拟合</li>
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

    <!-- 目标函数选择 -->
    <div class="config-section">
      <div class="form-group">
        <label class="section-title">目标函数</label>
        <select 
          v-model="localConfig.objective" 
          class="form-control"
          @change="updateConfig"
        >
          <option value="">默认</option>
          <!-- 分类任务目标函数 -->
          <optgroup label="分类任务">
            <option value="binary:logistic">二分类 (binary:logistic)</option>
            <option value="multi:softmax">多分类 (multi:softmax)</option>
            <option value="multi:softprob">多分类概率 (multi:softprob)</option>
          </optgroup>
          <!-- 回归任务目标函数 -->
          <optgroup label="回归任务">
            <option value="reg:squarederror">回归平方损失 (reg:squarederror)</option>
            <option value="reg:squaredlogerror">回归平方对数损失 (reg:squaredlogerror)</option>
            <option value="reg:pseudohubererror">Huber回归 (reg:pseudohubererror)</option>
          </optgroup>
        </select>
      </div>
    </div>

    <!-- 模型参数配置 -->
    <div class="config-section">
      <h4>模型参数</h4>
      
      <!-- 树的数量 -->
      <div class="form-group">
        <label class="section-title">树的数量 (n_estimators)</label>
        <input 
          type="number" 
          v-model.number="localConfig.n_estimators" 
          class="form-control"
          min="1"
          max="1000"
          @input="updateConfig"
        />
      </div>

      <!-- 树的最大深度 -->
      <div class="form-group">
        <label class="section-title">树的最大深度 (max_depth)</label>
        <input 
          type="number" 
          v-model.number="localConfig.max_depth" 
          class="form-control"
          min="1"
          max="20"
          @input="updateConfig"
        />
      </div>

      <!-- 学习率 -->
      <div class="form-group">
        <label class="section-title">学习率 (learning_rate)</label>
        <input 
          type="number" 
          v-model.number="localConfig.learning_rate" 
          class="form-control"
          step="0.01"
          min="0.001"
          max="1"
          @input="updateConfig"
        />
      </div>

      <!-- 子样本比例 -->
      <div class="form-group">
        <label class="section-title">子样本比例 (subsample)</label>
        <input 
          type="number" 
          v-model.number="localConfig.subsample" 
          class="form-control"
          step="0.01"
          min="0.1"
          max="1"
          @input="updateConfig"
        />
      </div>

      <!-- 特征比例 -->
      <div class="form-group">
        <label class="section-title">每棵树特征比例 (colsample_bytree)</label>
        <input 
          type="number" 
          v-model.number="localConfig.colsample_bytree" 
          class="form-control"
          step="0.01"
          min="0.1"
          max="1"
          @input="updateConfig"
        />
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
      </div>
    </div>

    <!-- 其他参数 -->
    <div class="config-section">
      <h4>其他参数</h4>
      <div class="form-group">
        <label class="section-title">其他XGBoost参数 (JSON格式)</label>
        <textarea 
          v-model="localConfig.params" 
          class="form-control"
          placeholder='例如: {"gamma": 0.1, "min_child_weight": 1}'
          @input="updateParams"
          rows="4"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "XGBoostConfig",
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
        this.localConfig.params = JSON.parse(this.localConfig.params)
        this.updateConfig()
      } catch (e) {
        // 如果解析失败，保留原始字符串
        // this.localConfig.params = this.localConfig.params
        this.updateConfig()
      }
    }
  }
}
</script>

<style scoped>
.xgboost-config {
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
</style>