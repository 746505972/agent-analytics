<template>
  <div class="param-config-section">
    <h3>设置参数</h3>
    <div class="add-header-content">
      <div class="data-cleaning-options">
        <div class="option-row">
          <label>
            <input 
              type="checkbox" 
              v-model="localConfig.removeDuplicates"
              @change="onConfigChange"
            /> 去除重复行
          </label>
        </div>
        <div class="option-row">
          <label>
            <input
              type="checkbox"
              v-model="localConfig.removeDuplicatesCols"
              @change="onConfigChange"
            /> 去除重复列
          </label>
        </div>
        <div class="option-row">
          <label>
            <input
              type="checkbox"
              v-model="localConfig.removeConstantCols"
              @change="onConfigChange"
            /> 去除唯一值列（常量列）
          </label>
        </div>
        <h3>设置阈值，删除缺失超出阈值的行列</h3>
        <p>阈值为0-1之间的小数，默认为1时不删除</p>
        <div class="option-row">
          <label>
            行缺失阈值:
            <input 
              type="number" 
              v-model.number="localConfig.rowMissingThreshold" 
              @input="onConfigChange"
              min="0" 
              max="1" 
              step="0.01"
              class="threshold-input"
            />
          </label>
        </div>
        <div class="option-row">
          <label>
            列缺失阈值:
            <input 
              type="number" 
              v-model.number="localConfig.columnMissingThreshold" 
              @input="onConfigChange"
              min="0" 
              max="1" 
              step="0.01"
              class="threshold-input"
            />
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InvalidSamplesConfig",
  props: {
    config: {
      type: Object,
      default: () => ({
        removeDuplicates: false,
        removeDuplicatesCols: false,
        removeConstantCols: false,
        rowMissingThreshold: 1,
        columnMissingThreshold: 1
      })
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
  },
  methods: {
    onConfigChange() {
      this.$emit('update:config', { ...this.localConfig });
    }
  }
}
</script>

<style scoped>
.param-config-section {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.param-config-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.add-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.data-cleaning-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-row {
  display: flex;
  align-items: center;
}

.option-row label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: normal;
  margin: 0;
}

.threshold-input {
  width: 80px;
  padding: 5px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>