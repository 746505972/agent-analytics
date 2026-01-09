<template>
  <div class="param-config-section">
    <h3>插值参数设置</h3>
    <div class="add-header-content">
      <div class="interpolation-options">
        <div class="option-row">
          <label>
            插值方法:
            <select v-model="localConfig.interpolationMethod" @change="onConfigChange" class="interpolation-method-select">
              <option value="linear">线性插值</option>
              <option value="ffill">前向填充</option>
              <option value="bfill">后向填充</option>
              <option value="mean">均值填充</option>
              <option value="median">中位数填充</option>
              <option value="constant">常量填充</option>
              <option value="knn">KNN插值</option>
            </select>
          </label>
        </div>

        <div class="option-row" v-if="localConfig.interpolationMethod === 'constant'">
          <label>
            填充值:
            <input
              v-model="localConfig.fillValue"
              @input="onConfigChange"
              placeholder="请输入填充值"
              class="input-value"
              aria-label="填充值"
            />
          </label>
        </div>

        <div class="option-row" v-if="localConfig.interpolationMethod === 'knn'">
          <label>
            KNN邻居数:
            <input
              v-model.number="localConfig.knnNeighbors"
              @input="onConfigChange"
              type="number"
              min="1"
              max="10"
              class="input-value"
            />
          </label>
        </div>
        <!-- 方法介绍 -->
        <div class="method-description" v-if="localConfig.interpolationMethod">
          <p v-if="localConfig.interpolationMethod === 'linear'">
            线性插值使用线性函数来估算缺失值。它会在已知数据点之间画一条直线，并使用这条直线来估计缺失值。
            这种方法适用于数值型数据，假设数据在局部范围内呈线性变化。
          </p>
          <p v-else-if="localConfig.interpolationMethod === 'ffill'">
            前向填充使用前面最近的有效值来填充缺失值。对于时间序列数据特别有用，
            因为它假设有连续性的数据点具有相似的值。
          </p>
          <p v-else-if="localConfig.interpolationMethod === 'bfill'">
            后向填充使用后面最近的有效值来填充缺失值。这种方法也适用于时间序列数据，
            特别是在数据趋势是反向的情况下。
          </p>
          <p v-else-if="localConfig.interpolationMethod === 'mean'">
            均值填充使用每列的平均值来填充该列的缺失值。这是一种简单而常用的方法，
            适用于数值型数据，但可能会降低数据的方差。
          </p>
          <p v-else-if="localConfig.interpolationMethod === 'median'">
            中位数填充使用每列的中位数来填充该列的缺失值。相比均值填充，它对异常值更鲁棒，
            是处理偏态分布数据的一个更好选择。
          </p>
          <p v-else-if="localConfig.interpolationMethod === 'constant'">
            常量填充使用指定的固定值来填充所有缺失值。这种方法非常直接，
            但在后续分析中可能会影响数据的真实分布。
          </p>
          <p v-else-if="localConfig.interpolationMethod === 'knn'">
            KNN（K最近邻）插值使用机器学习方法，基于最相似的k个样本来估算缺失值。
            它会考虑其他列的信息来预测缺失值，因此需要所有列参与计算。
            这就是为什么KNN方法会对全体列进行插值的原因。
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MissingValueInterpolationConfig",
  props: {
    config: {
      type: Object,
      default: () => ({
        interpolationMethod: 'linear',
        fillValue: '',
        knnNeighbors: 5,
      })
    },
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

.interpolation-method-select{
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right center;
  background-size: 16px;
}

.interpolation-method-select:hover {
  border-color: #999;
}

.interpolation-method-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.interpolation-method-select:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
  opacity: 0.7;
}

.option-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.option-row label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: normal;
  margin: 0;
}

.input-value {
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: border-color 0.2s;
}

.input-value:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.method-description {
  background-color: #f8f9fa;
  border-left: 4px solid #409eff;
  padding: 12px 16px;
  margin: 15px 0;
  border-radius: 0 4px 4px 0;
}

.method-description h4 {
  margin-top: 0;
  color: #303133;
}

.method-description p {
  margin: 8px 0;
  line-height: 1.6;
  color: #606266;
  font-size: 14px;
}
</style>