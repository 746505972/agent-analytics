<template>
  <div class="normality-test-config">
    <div class="normality-test-config-content">
      <!-- 方法描述 -->
      <div class="method-description">
        <p>正态性检验用于检验数据是否符合正态分布。许多统计方法（如T检验、方差分析等）都要求数据满足正态性假设。</p>
        <p>当数据不满足正态分布时，应考虑使用非参数检验方法。</p>
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

      <div class="config-section">
        <div class="form-group">
          <label class="section-title">检验方法</label>
          <select 
            v-model="localConfig.method" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="shapiro">Shapiro-Wilk检验</option>
            <option value="normaltest">D'Agostino检验</option>
          </select>
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
            <option value="">不使用分组</option>
            <option 
              v-for="column in categoricalColumns" 
              :key="column" 
              :value="column"
            >
              {{ column }}
            </option>
          </select>
          <p class="help-text">选择分组列后，将对每个组分别进行正态性检验</p>
        </div>
      </div>

      <!-- 检验方法说明 -->
      <div class="method-description">
        <div v-if="localConfig.method === 'shapiro'">
          <h4>Shapiro-Wilk检验</h4>
          <p>Shapiro-Wilk检验是检验正态性最常用的方法之一，适用于小样本数据（通常n&lt;5000,n&lt;50最佳）。该方法对各种偏离正态性的敏感度较高。</p>
          <p>原假设(H₀)：样本数据来自正态分布的总体</p>
          <p>备择假设(H₁)：样本数据不是来自正态分布的总体</p>
        </div>
        <div v-else>
          <h4>D'Agostino检验</h4>
          <p>D'Agostino检验基于数据的偏度和峰度进行检验，适用于中等或大样本数据。对于大样本数据更为稳健。</p>
          <p>原假设(H₀)：样本数据来自正态分布的总体</p>
          <p>备择假设(H₁)：样本数据不是来自正态分布的总体</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NormalityTestConfig",
  props: {
    config: {
      type: Object,
      default: () => ({
        method: 'shapiro',
        alpha: 0.05,
        groupBy: ''
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
.normality-test-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.normality-test-config-content {
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
  color: #333;
}

.method-description p {
  margin: 0 0 5px 0;
}

.help-text {
  font-size: 12px;
  color: #888;
  margin-top: 5px;
  margin-bottom: 0;
}
</style>