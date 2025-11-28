<template>
  <div class="result-content">
    <!-- 基本信息分析结果 -->
    <div v-if="currentMethod === 'basic_info' && datasetDetails" class="analysis-section">
      <div class="basic-info-details">
        <h3>数据集基本信息</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">文件名:</span>
            <span class="info-value">{{ datasetDetails.filename }}</span>
          </div>
          <div class="info-item">
            <div>
              <span class="info-label">行数:</span>
              <span class="info-value">{{ datasetDetails.rows.toLocaleString() }}</span>
            </div>
            <div>
              <span class="info-label">列数:</span>
              <span class="info-value">{{ datasetDetails.columns.toLocaleString() }}</span>
            </div>
          </div>
          <div class="info-item">
            <div>
              <span class="info-label">完整性:</span>
              <span class="info-value">{{ (datasetDetails.completeness * 100).toFixed(2) }}%</span>
            </div>
            <div>
              <span class="info-label">总单元格数:</span>
              <span class="info-value">{{ datasetDetails.total_cells.toLocaleString() }}</span>
            </div>
            <div>
              <span class="info-label">缺失值总数:</span>
              <span class="info-value">{{ datasetDetails.total_missing.toLocaleString() }}</span>
            </div>
          </div>
        </div>
        
        <h4>列信息:</h4>
        <div class="column-table-container">
          <table class="column-table">
            <thead>
              <tr>
                <th>列名</th>
                <th>数据类型</th>
                <th>缺失值数量</th>
                <th>列完整性</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(dtype, columnName) in datasetDetails.dtypes" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ dtype }}</td>
                <td>{{ datasetDetails.missing_values[columnName].toLocaleString() || 0 }}</td>
                <td>{{ (datasetDetails.completeness_values[columnName] * 100).toFixed(2) + '%' || 'unknown' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <h4>数值型列统计信息:</h4>
        <div class="stats-table-container">
          <table class="stats-table">
            <thead>
              <tr>
                <th>列名</th>
                <th>最小值</th>
                <th>最大值</th>
                <th>平均值</th>
                <th>标准差</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(stats, columnName) in datasetDetails.numeric_stats" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ stats.min !== null ? stats.min.toLocaleString() : 'N/A' }}</td>
                <td>{{ stats.max !== null ? stats.max.toLocaleString() : 'N/A' }}</td>
                <td>{{ stats.mean !== null ? Number(stats.mean.toFixed(2)).toLocaleString() : 'N/A' }}</td>
                <td>{{ stats.std !== null ? Number(stats.std.toFixed(2)).toLocaleString() : 'N/A' }}</td>
              </tr>
              <tr v-if="Object.keys(datasetDetails.numeric_stats).length === 0">
                <td colspan="5" class="no-data">无数值型列</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <h4>分类型列统计信息:</h4>
        <div class="stats-table-container">
          <table class="stats-table">
            <thead>
              <tr>
                <th>列名</th>
                <th>唯一值数量</th>
                <th>常见值</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(stats, columnName) in datasetDetails.categorical_stats" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ stats.unique_count }}</td>
                <td>
                  <div v-for="(count, value) in stats.top_values" :key="value" class="top-value-item">
                    <span class="highlight-param">{{ value }}</span> 出现 <span class="highlight-param">{{ count }}</span> 次
                  </div>
                </td>
              </tr>
              <tr v-if="Object.keys(datasetDetails.categorical_stats).length === 0">
                <td colspan="3" class="no-data">无分类型列</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <h4>前5行数据预览:</h4>
        <div class="data-preview">
          <table>
            <thead>
              <tr>
                <th v-for="col in datasetDetails.column_names" :key="col">{{ col }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in datasetDetails.head" :key="index">
                <td v-for="col in datasetDetails.column_names" :key="col">{{ row[col] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <!-- 统计摘要分析结果 -->
    <div v-else-if="currentMethod === 'statistical_summary'" class="analysis-section">
      <h3>统计摘要</h3>
      <p>此功能正在开发中...</p>
    </div>
    
    <!-- 数据可视化分析结果 -->
    <div v-else-if="currentMethod === 'visualization'" class="analysis-section">
      <h3>数据可视化</h3>
      <p>此功能正在开发中...</p>
    </div>
    
    <!-- 机器学习分析结果 -->
    <div v-else-if="currentMethod === 'ml_analysis'" class="analysis-section">
      <h3>机器学习分析</h3>
      <p>此功能正在开发中...</p>
    </div>
    
    <!-- 加载状态 -->
    <div v-else-if="loadingDetails" class="analysis-section">
      <div class="loading-spinner">加载分析结果中...</div>
    </div>
    
    <!-- 错误状态 -->
    <div v-else class="analysis-section">
      <p>无法加载分析结果</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ResultContent",
  props: {
    currentMethod: {
      type: String,
      required: true
    },
    datasetDetails: {
      type: Object,
      default: null
    },
    loadingDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.result-content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.analysis-section {
  min-height: 500px;
}

.loading-spinner {
  text-align: center;
  padding: 50px;
  color: #409eff;
  font-size: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  overflow-wrap: break-word;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.info-label {
  font-size: 14px;
  color: #606266;
}

.info-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.data-preview {
  overflow-x: auto;
}

.data-preview table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.data-preview th,
.data-preview td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  white-space: nowrap;
}

.data-preview th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.stats-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.stats-table th,
.stats-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.stats-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.no-data {
  text-align: center;
  color: #909399;
  font-style: italic;
}

.top-value-item {
  margin-bottom: 3px;
}

.column-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.column-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.column-table th,
.column-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.column-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.highlight-param {
  font-family: 'Courier New', monospace;
}
</style>