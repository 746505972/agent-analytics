<template>
  <div class="xgboost-config">
    <h4>XGBoost配置</h4>
    
    <!-- 任务类型选择 -->
    <div class="config-item">
      <label for="task-type" class="config-label">任务类型:</label>
      <select 
        id="task-type" 
        v-model="localConfig.task_type" 
        class="config-select"
        @change="updateConfig"
      >
        <option value="auto">自动判断</option>
        <option value="classification">分类</option>
        <option value="regression">回归</option>
      </select>
    </div>

    <!-- Y列选择 -->
    <div class="config-item" v-if="columns && columns.length > 0">
      <label for="y-column" class="config-label">因变量 (Y列):</label>
      <select 
        id="y-column" 
        v-model="localConfig.y_column" 
        class="config-select"
        @change="updateConfig"
      >
        <option value="">请选择</option>
        <option v-for="column in columns" :key="column" :value="column">{{ column }}</option>
      </select>
    </div>

    <!-- 目标函数选择 -->
    <div class="config-item">
      <label for="objective" class="config-label">目标函数:</label>
      <select 
        id="objective" 
        v-model="localConfig.objective" 
        class="config-select"
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

    <!-- 模型参数配置 -->
    <div class="config-section">
      <h5>模型参数</h5>
      
      <!-- 树的数量 -->
      <div class="config-item">
        <label for="n-estimators" class="config-label">树的数量 (n_estimators):</label>
        <input 
          type="number" 
          id="n-estimators" 
          v-model.number="localConfig.n_estimators" 
          class="config-input"
          min="1"
          max="1000"
          @input="updateConfig"
        />
      </div>

      <!-- 树的最大深度 -->
      <div class="config-item">
        <label for="max-depth" class="config-label">树的最大深度 (max_depth):</label>
        <input 
          type="number" 
          id="max-depth" 
          v-model.number="localConfig.max_depth" 
          class="config-input"
          min="1"
          max="20"
          @input="updateConfig"
        />
      </div>

      <!-- 学习率 -->
      <div class="config-item">
        <label for="learning-rate" class="config-label">学习率 (learning_rate):</label>
        <input 
          type="number" 
          id="learning-rate" 
          v-model.number="localConfig.learning_rate" 
          class="config-input"
          step="0.01"
          min="0.001"
          max="1"
          @input="updateConfig"
        />
      </div>

      <!-- 子样本比例 -->
      <div class="config-item">
        <label for="subsample" class="config-label">子样本比例 (subsample):</label>
        <input 
          type="number" 
          id="subsample" 
          v-model.number="localConfig.subsample" 
          class="config-input"
          step="0.01"
          min="0.1"
          max="1"
          @input="updateConfig"
        />
      </div>

      <!-- 特征比例 -->
      <div class="config-item">
        <label for="colsample-bytree" class="config-label">每棵树特征比例 (colsample_bytree):</label>
        <input 
          type="number" 
          id="colsample-bytree" 
          v-model.number="localConfig.colsample_bytree" 
          class="config-input"
          step="0.01"
          min="0.1"
          max="1"
          @input="updateConfig"
        />
      </div>

      <!-- 随机种子 -->
      <div class="config-item">
        <label for="random-state" class="config-label">随机种子 (random_state):</label>
        <input 
          type="number" 
          id="random-state" 
          v-model.number="localConfig.random_state" 
          class="config-input"
          min="0"
          @input="updateConfig"
        />
      </div>
    </div>

    <!-- 其他参数 -->
    <div class="config-section">
      <h5>其他参数</h5>
      <div class="config-item">
        <label for="other-params" class="config-label">其他XGBoost参数 (JSON格式):</label>
        <textarea 
          id="other-params" 
          v-model="localConfig.params" 
          class="config-textarea"
          placeholder='例如: {"gamma": 0.1, "min_child_weight": 1}'
          @input="updateParams"
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
  mounted() {
    // 初始化时如果params是对象，则转换为字符串
    if (typeof this.localConfig.params === 'object' && this.localConfig.params !== null) {
      this.localConfig.paramsStr = JSON.stringify(this.localConfig.params, null, 2)
    } else {
      this.localConfig.paramsStr = this.localConfig.params || '{}'
    }
  },
  methods: {
    updateConfig() {
      this.$emit('update:config', { ...this.localConfig })
    },
    updateParams(event) {
      try {
        // 尝试解析JSON
        const parsed = JSON.parse(event.target.value)
        this.localConfig.params = parsed
        this.updateConfig()
      } catch (e) {
        // 如果解析失败，保留原始字符串
        console.warn('Invalid JSON in other params')
      }
    }
  }
}
</script>

<style scoped>
.xgboost-config {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.config-item {
  margin-bottom: 15px;
}

.config-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #606266;
}

.config-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
  font-size: 14px;
}

.config-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.config-textarea {
  width: 100%;
  height: 100px;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  font-family: monospace;
  resize: vertical;
}

.config-section {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e4e7ed;
}

.config-section h5 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
}
</style>