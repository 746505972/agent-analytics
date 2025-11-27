<template>
  <div class="param-config-section">
    <div v-if="currentMethod === 'add_header' && headerEditMode !== 'remove'">
      <h3>设置列名</h3>
      <div class="add-header-content">
        <div class="column-inputs">
          <div 
            v-for="(column, index) in selectedFileColumns" 
            :key="index" 
            class="column-input-item"
          >
            <input 
              :id="'column-' + index"
              v-model="newColumnNames[index]" 
              :placeholder="'列' + (index + 1)"
              type="text"
            />
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="currentMethod === 'invalid_samples'">
      <h3>设置参数</h3>
      <div class="add-header-content">
        <div class="data-cleaning-options">
          <div class="option-row">
            <label>
              <input 
                type="checkbox" 
                v-model="removeDuplicates"
                @change="updateInvalidSamplesParams"
              /> 去除重复行
            </label>
          </div>
          <div class="option-row">
            <label>
              <input
                type="checkbox"
                v-model="removeDuplicatesCols"
                @change="updateInvalidSamplesParams"
              /> 去除重复列
            </label>
          </div>
          <div class="option-row">
            <label>
              <input
                type="checkbox"
                v-model="removeConstantCols"
                @change="updateInvalidSamplesParams"
              /> 去除唯一值列
            </label>
          </div>
          <h3>设置阈值，删除缺失超出阈值的行列</h3>
          <p>阈值为0-1之间的小数，默认为1时不删除</p>
          <div class="option-row">
            <label>
              行缺失阈值:
              <input 
                type="number" 
                v-model="rowMissingThreshold" 
                min="0" 
                max="1" 
                step="0.01"
                class="threshold-input"
                @change="updateInvalidSamplesParams"
              />
            </label>
          </div>
          <div class="option-row">
            <label>
              列缺失阈值:
              <input 
                type="number" 
                v-model="columnMissingThreshold" 
                min="0" 
                max="1" 
                step="0.01"
                class="threshold-input"
                @change="updateInvalidSamplesParams"
              />
            </label>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="currentMethod === 'missing_value_interpolation'">
      <h3>插值参数设置</h3>
      <div class="add-header-content">
        <div class="interpolation-options">
          <div class="option-row">
            <label>
              插值方法:
              <select v-model="interpolationMethod" class="interpolation-method-select" @change="updateInterpolationParams">
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

          <div class="option-row" v-if="interpolationMethod === 'constant'">
            <label>
              填充值:
              <input
                type="text"
                v-model="fillValue"
                placeholder="请输入填充值"
                class="input-value"
                aria-label="填充值"
                @input="updateInterpolationParams"
              />
            </label>
          </div>

          <div class="option-row" v-if="interpolationMethod === 'knn'">
            <label>
              KNN邻居数:
              <input
                type="number"
                v-model="knnNeighbors"
                min="1"
                max="10"
                class="input-value"
                @input="updateInterpolationParams"
              />
            </label>
          </div>
          <!-- 方法介绍 -->
          <div class="method-description" v-if="interpolationMethod">
            <p v-if="interpolationMethod === 'linear'">
              线性插值使用线性函数来估算缺失值。它会在已知数据点之间画一条直线，并使用这条直线来估计缺失值。
              这种方法适用于数值型数据，假设数据在局部范围内呈线性变化。
            </p>
            <p v-else-if="interpolationMethod === 'ffill'">
              前向填充使用前面最近的有效值来填充缺失值。对于时间序列数据特别有用，
              因为它假设有连续性的数据点具有相似的值。
            </p>
            <p v-else-if="interpolationMethod === 'bfill'">
              后向填充使用后面最近的有效值来填充缺失值。这种方法也适用于时间序列数据，
              特别是在数据趋势是反向的情况下。
            </p>
            <p v-else-if="interpolationMethod === 'mean'">
              均值填充使用每列的平均值来填充该列的缺失值。这是一种简单而常用的方法，
              适用于数值型数据，但可能会降低数据的方差。
            </p>
            <p v-else-if="interpolationMethod === 'median'">
              中位数填充使用每列的中位数来填充该列的缺失值。相比均值填充，它对异常值更鲁棒，
              是处理偏态分布数据的一个更好选择。
            </p>
            <p v-else-if="interpolationMethod === 'constant'">
              常量填充使用指定的固定值来填充所有缺失值。这种方法非常直接，
              但在后续分析中可能会影响数据的真实分布。
            </p>
            <p v-else-if="interpolationMethod === 'knn'">
              KNN（K最近邻）插值使用机器学习方法，基于最相似的k个样本来估算缺失值。
              它会考虑其他列的信息来预测缺失值，因此需要所有列参与计算。
              这就是为什么KNN方法会对全体列进行插值的原因。
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ParameterConfig",
  props: {
    currentMethod: {
      type: String,
      required: true
    },
    selectedFileColumns: {
      type: Array,
      required: true
    },
    headerEditMode: {
      type: [Boolean, String],
      default: false
    },
    newColumnNames: {
      type: Array,
      default: () => []
    },
    removeDuplicates: {
      type: Boolean,
      default: false
    },
    removeDuplicatesCols: {
      type: Boolean,
      default: false
    },
    removeConstantCols: {
      type: Boolean,
      default: false
    },
    rowMissingThreshold: {
      type: Number,
      default: 1
    },
    columnMissingThreshold: {
      type: Number,
      default: 1
    },
    interpolationMethod: {
      type: String,
      default: 'linear'
    },
    fillValue: {
      type: String,
      default: ''
    },
    knnNeighbors: {
      type: Number,
      default: 5
    }
  },
  emits: [
    'update:newColumnNames',
    'update:removeDuplicates',
    'update:removeDuplicatesCols',
    'update:removeConstantCols',
    'update:rowMissingThreshold',
    'update:columnMissingThreshold',
    'update:interpolationMethod',
    'update:fillValue',
    'update:knnNeighbors'
  ],
  methods: {
    updateInterpolationParams() {
      this.$emit('update:interpolationMethod', this.interpolationMethod);
      this.$emit('update:fillValue', this.fillValue);
      this.$emit('update:knnNeighbors', this.knnNeighbors);
    },
    updateInvalidSamplesParams() {
      this.$emit('update:removeDuplicates', this.removeDuplicates);
      this.$emit('update:removeDuplicatesCols', this.removeDuplicatesCols);
      this.$emit('update:removeConstantCols', this.removeConstantCols);
      this.$emit('update:rowMissingThreshold', this.rowMissingThreshold);
      this.$emit('update:columnMissingThreshold', this.columnMissingThreshold);
    }
  },
  watch: {
    newColumnNames: {
      handler(newVal) {
        this.$emit('update:newColumnNames', newVal);
      },
      deep: true
    }
  }
}
</script>

<style scoped>
/* 添加标题行区域样式 */
.param-config-section {
  background: white;
  padding: 20px;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
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

.column-inputs {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.column-input-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
  margin-bottom: 0;
}

.column-input-item label {
  width: 100px;
  margin-right: 10px;
  color: #606266;
}

.column-input-item input {
  flex: 1;
  padding: 8px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
}

/* 数据清洗选项样式 */
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