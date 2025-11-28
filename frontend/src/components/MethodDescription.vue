<template>
  <div class="method-description-section">
    <div class="method-description-content">
      <div class="method-content">
        <div v-if="currentMethod === 'basic_info'">
          <h4>数据集基本信息</h4>
          <p>查看数据集的基本信息，包括行列数、列名、数据类型等。</p>
        </div>
        <div v-else-if="currentMethod === 'statistical_summary'">
          <h4>统计摘要</h4>
          <p>获取数据集的统计摘要信息，包括均值、中位数、标准差等。</p>
        </div>
        <div v-else-if="currentMethod === 'correlation_analysis'">
          <h4>相关性分析</h4>
          <p>分析数据集中各变量之间的相关性。</p>
        </div>
        <div v-else-if="currentMethod === 'distribution_analysis'">
          <h4>分布分析</h4>
          <p>分析数据集中各变量的分布情况。</p>
        </div>
        <div v-else-if="currentMethod === 'visualization'">
          <h4>数据可视化</h4>
          <p>生成数据集的可视化图表，帮助理解数据分布和关系。</p>
        </div>
        <div v-else-if="currentMethod === 'ml_analysis'">
          <h4>机器学习分析</h4>
          <p>执行机器学习分析任务，如聚类、分类、回归等。</p>
        </div>
        <div v-else-if="currentMethod === 'clustering'">
          <h4>聚类分析</h4>
          <p>使用聚类算法对数据进行分组分析。</p>
        </div>
        <div v-else-if="currentMethod === 'classification'">
          <h4>分类分析</h4>
          <p>使用分类算法对数据进行分类预测。</p>
        </div>
        <div v-else-if="currentMethod === 'regression'">
          <h4>回归分析</h4>
          <p>使用回归算法分析变量之间的关系。</p>
        </div>
        <div v-else-if="currentMethod === 'text_analysis'">
          <h4>文本分析</h4>
          <p>对文本数据进行分析，提取关键信息和模式。</p>
        </div>
        <div v-else-if="currentMethod === 'sentiment_analysis'">
          <h4>情感分析</h4>
          <p>分析文本数据中的情感倾向。</p>
        </div>
        <div v-else-if="currentMethod === 'invalid_samples'">
          <h4>无效样本</h4>
          <p>删除重复行、重复列、唯一值列、缺失过多的行列。</p>
        </div>
        <div v-else-if="currentMethod === 'missing_value_interpolation'">
          <h4>插值法</h4>
          <p>对数据中的缺失值进行插值处理，支持多种插值方法。</p>
        </div>
        <div v-else-if="currentMethod === 'delete_columns'">
          <h4>删除列</h4>
          <p>删除指定的列。</p>
        </div>
        <div v-else-if="currentMethod === 'data_transformation'">
          <h4>数据转换</h4>
          <p>对数据进行转换操作，如标准化、归一化等。</p>
        </div>
        <div v-else-if="currentMethod === 'add_header'">
          <h4>添加/修改标题行</h4>
          <p>为没有标题行的文件添加自定义列名，或修改现有标题行。</p>
          <div class="header-mode-toggle">
            <label>
              <input 
                type="radio" 
                :checked="headerEditMode === 'add'" 
                value="add" 
                @change="$emit('update:headerEditMode', 'add')"
                name="headerEditMode"
              > 添加标题行
            </label>
            <label>
              <input 
                type="radio" 
                :checked="headerEditMode === 'modify'" 
                value="modify" 
                @change="$emit('update:headerEditMode', 'modify')"
                name="headerEditMode"
              > 修改标题行
            </label>
            <label>
              <input 
                type="radio" 
                :checked="headerEditMode === 'remove'" 
                value="remove" 
                @change="$emit('update:headerEditMode', 'remove')"
                name="headerEditMode"
              > 删除首行
            </label>
          </div>
        </div>
      </div>
      <div class="method-actions">
        <button 
          v-if="currentMethod === 'add_header'"
          @click="$emit('apply-header-names')"
          class="execute-button"
        >
          应用标题
        </button>
        <button
          v-else-if="currentMethod === 'invalid_samples'"
          @click="$emit('execute-invalid-samples')"
          class="execute-button"
        >
          执行操作
        </button>
        <button
          v-else-if="currentMethod === 'missing_value_interpolation'"
          @click="$emit('execute-missing-value-interpolation')"
          class="execute-button"
        >
          执行插值
        </button>
        <button
          v-else-if="currentMethod === 'delete_columns'"
          @click="$emit('execute-delete-columns')"
          class="execute-button"
        >
          执行操作
        </button>
        <button 
          v-else
          @click="$emit('execute-method')"
          class="execute-button"
        >
          执行分析
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MethodDescription",
  props: {
    currentMethod: {
      type: String,
      required: true
    },
    headerEditMode: {
      type: String,
      default: 'add'
    }
  },
  emits: [
    'update:headerEditMode',
    'apply-header-names',
    'execute-invalid-samples',
    'execute-missing-value-interpolation',
    'execute-delete-columns',
    'execute-method'
  ]
}
</script>

<style scoped>
.method-description-section {
  background: white;
  padding: 0;
  margin-bottom: 0;
  flex: 0 0 auto;
}

.method-description-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.method-content {
  flex: 1;
  background-color: white;
  border-radius: 4px;
  padding: 15px;
}

.method-actions {
  flex: 0 0 auto;
  text-align: center;
  align-self: flex-start;
  margin-top: 15px;
}

.execute-button {
  padding: 10px 20px;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  white-space: nowrap;
  margin-right: 5px;
}

.execute-button:hover {
  background-color: #85ce61;
}

.header-mode-toggle {
  margin-top: 10px;
  margin-bottom: 15px;
}

.header-mode-toggle label {
  margin-right: 15px;
  font-weight: normal;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.header-mode-toggle input[type="radio"] {
  margin-right: 5px;
}

@media (max-width: 768px) {
  .method-description-content {
    flex-direction: column;
    align-items: stretch;
  }
  
  .method-actions {
    align-self: stretch;
    margin-top: 10px;
  }
}
</style>