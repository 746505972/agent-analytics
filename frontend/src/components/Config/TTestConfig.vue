<template>
  <div class="t-test-config">
    <div class="t-test-type-selector">
      <h3>T检验类型</h3>
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

    <div class="t-test-config-content">
      <!-- 方法描述 -->
      <div class="method-description" v-if="localConfig.testType === 'one_sample'">
        <p>单样本T检验：用于检验单个样本的均值是否与已知的总体均值有显著差异。适用于样本数据符合正态分布的情况。</p>
        <p class="formula">公式：t = (x̄ - μ) / (s / √n)</p>
        <p class="formula-desc">其中x̄是样本均值，μ是假设的总体均值，s是样本标准差，n是样本数量</p>
      </div>
      <div class="method-description" v-else-if="localConfig.testType === 'independent'">
        <p>独立样本T检验：用于检验两个独立样本的均值是否有显著差异。适用于两组数据相互独立且符合正态分布的情况。</p>
        <p class="formula">公式：t = (x̄₁ - x̄₂) / √[(s₁²/n₁) + (s₂²/n₂)]</p>
        <p class="formula-desc">其中x̄₁和x̄₂分别是两组样本的均值，s₁和s₂是标准差，n₁和n₂是样本数量</p>
      </div>
      <div class="method-description" v-else-if="localConfig.testType === 'paired'">
        <p>配对样本T检验：用于检验同一组对象在不同条件下的均值是否有显著差异。适用于两组数据存在配对关系的情况。</p>
        <p class="formula">公式：t = x̄d / (sd / √n)</p>
        <p class="formula-desc">其中x̄d是配对数据差值的均值，sd是差值的标准差，n是配对数</p>
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

      <!-- 单样本T检验参数 -->
      <div v-if="localConfig.testType === 'one_sample'" class="config-section">
        <div class="form-group">
          <label class="section-title">总体均值 (μ)</label>
          <input 
            type="number" 
            v-model.number="localConfig.popmean" 
            @input="onConfigChange"
            step="0.1"
            class="form-control"
          >
        </div>
      </div>

      <!-- 独立样本T检验参数 -->
      <div v-if="localConfig.testType === 'independent'" class="config-section">
        <div class="form-group">
          <label class="section-title">分组列</label>
          <select 
            v-model="localConfig.groupCol" 
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
        </div>
        
        <div class="form-group">
          <label class="checkbox-label">
            <input 
              type="checkbox" 
              v-model="localConfig.equalVar" 
              @change="onConfigChange"
            > 假设方差相等
          </label>
        </div>
      </div>

      <div class="config-section">
        <div class="form-group">
          <label class="section-title">正态性检验方法</label>
          <select 
            v-model="localConfig.normalityMethod" 
            @change="onConfigChange"
            class="form-control"
          >
            <option value="shapiro">Shapiro-Wilk检验</option>
            <option value="normaltest">D'Agostino检验</option>
          </select>
        </div>
      </div>

      <!-- 正态性检验说明 -->
      <div class="method-description">
        <div v-if="localConfig.normalityMethod === 'shapiro'">
          <p>Shapiro-Wilk检验：适用于小样本数据（通常n&lt;5000,n&lt;50最佳），是检验正态性最常用的方法之一。该方法对各种偏离正态性的敏感度较高。</p>
        </div>
        <div v-else>
          <p>D'Agostino检验：基于数据的偏度和峰度进行检验，适用于中等或大样本数据。对于大样本数据更为稳健。</p>
        </div>
        <h4>为什么要进行正态性检验？</h4>
        <p>T检验是一种参数检验方法，它假设数据服从正态分布。如果数据严重偏离正态分布，T检验的结果可能不可靠。因此，在进行T检验之前，我们需要通过正态性检验来验证数据是否满足正态分布假设。</p>



      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TTestConfig",
  props: {
    config: {
      type: Object,
      default: () => ({
        testType: 'one_sample',
        alpha: 0.05,
        popmean: 0,
        groupCol: '',
        equalVar: true,
        normalityMethod: 'shapiro'
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
        { value: 'one_sample', label: '单样本T检验' },
        { value: 'independent', label: '独立样本T检验' },
        { value: 'paired', label: '配对样本T检验' }
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
.t-test-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.t-test-type-selector {
  margin-bottom: 20px;
}

.t-test-type-selector h3 {
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

.t-test-config-content {
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