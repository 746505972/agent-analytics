<template>
  <div class="param-config-section">
    <div class="correlation-config">
      <h3>相关性分析配置</h3>
      
      <div class="form-group">
        <label>分析方法:</label>
        <select 
          :value="correlationMethod" 
          @input="$emit('update:correlationMethod', $event.target.value)"
          class="method-select"
        >
          <option value="pearson">Pearson相关系数</option>
          <option value="spearman">Spearman相关系数</option>
          <option value="kendall">Kendall相关系数</option>
        </select>
      </div>
      
      <!-- 方法介绍 -->
      <div class="method-description" v-if="correlationMethod === 'pearson'">
        <p>Pearson相关系数：衡量两个连续变量之间的线性相关程度。</p>
        <p class="formula">公式：ρ = cov(X,Y) / (σ_X * σ_Y)</p>
        <p class="formula-desc">其中cov(X,Y)是X和Y的协方差，σ_X和σ_Y分别是X和Y的标准差</p>
      </div>
      
      <div class="method-description" v-else-if="correlationMethod === 'spearman'">
        <p>Spearman相关系数：衡量两个变量之间的单调关系，基于变量的秩次而非原始值。</p>
        <p class="formula">公式：ρ = 1 - (6 * Σd²) / (n * (n² - 1))</p>
        <p class="formula-desc">其中d是两个变量的秩次差，n是样本数量</p>
      </div>
      
      <div class="method-description" v-else-if="correlationMethod === 'kendall'">
        <p>Kendall相关系数：衡量两个变量之间的秩序相关性，基于一致对和不一致对的数量。</p>
        <p class="formula">公式：τ = (P - Q) / √((P + Q + T) * (P + Q + U))</p>
        <p class="formula-desc">其中P是一致对数量，Q是不一致对数量，T和U是关联对数量</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CorrelationAnalysisConfig",
  props: {
    correlationMethod: {
      type: String,
      default: 'pearson'
    }
  },
  emits: [
    'update:correlationMethod'
  ]
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

.correlation-config {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #606266;
}

.method-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
  background-color: #fff;
  cursor: pointer;
}

.method-select:hover {
  border-color: #c0c4cc;
}

.method-select:focus {
  outline: none;
  border-color: #409eff;
}

.method-description {
  background-color: #f8f9fa;
  border-left: 4px solid #409eff;
  padding: 12px 16px;
  margin: 15px 0;
  border-radius: 0 4px 4px 0;
}

.method-description p {
  margin: 8px 0;
  line-height: 1.6;
  color: #606266;
  font-size: 14px;
}

.formula {
  font-style: italic;
  color: #409eff;
  font-weight: 500;
}

.formula-desc {
  font-size: 13px;
  color: #909399;
}
</style>