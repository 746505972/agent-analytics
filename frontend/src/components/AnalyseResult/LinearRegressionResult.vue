<template>
  <div class="linear-regression-result" v-if="datasetDetails.resultMethod === 'linear_regression'">
    <h3>线性回归分析结果</h3>
    
    <!-- 模型信息 -->
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">回归方法:</span>
        <span class="info-value">{{ datasetDetails.method }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">因变量 (Y):</span>
        <span class="info-value">{{ datasetDetails.y_column }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">样本数量:</span>
        <span class="info-value">{{ datasetDetails.sample_size }}</span>
      </div>
      <div class="info-item" v-if="datasetDetails.intercept !== null">
        <span class="info-label">截距:</span>
        <span class="info-value">{{ formatNumber(datasetDetails.intercept) }}</span>
      </div>
    </div>

    <!-- 自变量列表 -->
    <div class="table-header">
      <h4>自变量 (X)</h4>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table">
        <thead>
          <tr>
            <th>变量名称</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(x, index) in datasetDetails.x_columns" :key="index">
            <td>{{ x }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 回归系数 -->
    <div class="table-header">
      <h4>回归系数</h4>
      <button class="copy-button" @click="copyTable('coefficients')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="coefficientsTable">
        <thead>
          <tr>
            <th>变量</th>
            <th>系数</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(coef, varName) in datasetDetails.coefficients" :key="varName">
            <td>{{ varName }}</td>
            <td>{{ formatNumber(coef) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 模型评估指标 -->
    <div class="table-header">
      <h4>模型评估指标</h4>
      <button class="copy-button" @click="copyTable('evaluation')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="evaluationTable">
        <thead>
          <tr>
            <th>指标</th>
            <th>值</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>R² 得分</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.r2_score) }}</td>
          </tr>
          <tr>
            <td>均方误差 (MSE)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.mse) }}</td>
          </tr>
          <tr>
            <td>均方根误差 (RMSE)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.rmse) }}</td>
          </tr>
          <tr>
            <td>平均绝对误差 (MAE)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.mae) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 正则化参数 -->
    <div class="regularization-params" v-if="datasetDetails.regularization_params">
      <div class="table-header">
        <h4>正则化参数</h4>
        <button class="copy-button" @click="copyTable('regularization')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="regularizationTable">
          <thead>
            <tr>
              <th>参数</th>
              <th>值</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Alpha (正则化强度)</td>
              <td>{{ formatNumber(datasetDetails.alpha) }}</td>
            </tr>
            <tr v-if="datasetDetails.method === 'elastic_net'">
              <td>L1比例</td>
              <td>{{ formatNumber(datasetDetails.l1_ratio) }}</td>
            </tr>
            <tr>
              <td>最大迭代次数</td>
              <td>{{ datasetDetails.regularization_params.max_iter }}</td>
            </tr>
            <tr>
              <td>收敛容差</td>
              <td>{{ formatNumber(datasetDetails.regularization_params.tol) }}</td>
            </tr>
            <tr>
              <td>拟合截距</td>
              <td>{{ datasetDetails.regularization_params.fit_intercept ? '是' : '否' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 线性回归公式 -->
    <div class="table-header">
      <h4>线性回归公式</h4>
      <button class="copy-button" @click="copyFormula()" title="复制公式">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="formula-container">
      <div class="formula-display">
        <div class="formula-math">y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n</div>
      </div>
      <div class="formula-breakdown">
        <div class="formula-breakdown-item">
          <span class="formula-part">y =</span>
          <span class="formula-expression">{{ formatFormulaExpression() }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LinearRegressionResult',
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatNumber(value) {
      if (value === null || value === undefined) {
        return 'N/A';
      }
      if (typeof value === 'number') {
        return value.toFixed(6);
      }
      return value;
    },
    
    // 复制表格数据到剪贴板
    copyTable(tableType) {
      let table;
      switch (tableType) {
        case 'coefficients':
          table = this.$refs.coefficientsTable;
          break;
        case 'evaluation':
          table = this.$refs.evaluationTable;
          break;
        case 'regularization':
          table = this.$refs.regularizationTable;
          break;
        default:
          return;
      }

      if (!table) {
        console.error('无法找到表格元素');
        return;
      }

      // 获取表格数据
      let csvContent = '';
      const rows = table.querySelectorAll('tr');
      
      for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cells = rows[i].querySelectorAll('th, td');
        
        for (let j = 0; j < cells.length; j++) {
          // 处理特殊字符和逗号
          let cellText = cells[j].innerText.replace(/"/g, '""');
          if (cellText.includes(',') || cellText.includes('\n')) {
            cellText = `"${cellText}"`;
          }
          row.push(cellText);
        }
        
        csvContent += row.join(',') + '\n';
      }

      // 尝试使用 Clipboard API
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(csvContent).then(() => {
          this.showCopyNotification('表格数据已复制到剪贴板');
          console.log('表格数据已复制到剪贴板');
        }).catch(err => {
          console.error('复制失败:', err);
          this.fallbackCopyTextToClipboard(csvContent);
        });
      } else {
        // 回退方案
        this.fallbackCopyTextToClipboard(csvContent);
      }
    },

    // 回退的复制方法
    fallbackCopyTextToClipboard(text) {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      
      // 避免滚动到底部
      textArea.style.top = '0';
      textArea.style.left = '0';
      textArea.style.position = 'fixed';
      textArea.style.opacity = '0';
      
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        const successful = document.execCommand('copy');
        if (successful) {
          this.showCopyNotification('表格数据已复制到剪贴板');
          console.log('表格数据已复制到剪贴板');
        } else {
          console.error('复制命令失败');
        }
      } catch (err) {
        console.error('回退复制失败:', err);
      }

      document.body.removeChild(textArea);
    },
    
    // 显示复制通知
    showCopyNotification(message, isError = false) {
      // 创建通知元素
      const notification = document.createElement('div');
      notification.textContent = message;
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background-color: ${isError ? '#f56c6c' : '#67c23a'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        z-index: 2000;
        font-size: 14px;
      `;
      
      // 添加到页面
      document.body.appendChild(notification);
      
      // 3秒后移除
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 3000);
    },
    
    // 格式化公式表达式
    formatFormulaExpression() {
      // 构建公式表达式
      let parts = [];
      
      // 添加截距项
      if (this.datasetDetails.intercept !== null && this.datasetDetails.intercept !== undefined) {
        parts.push(this.formatNumber(this.datasetDetails.intercept));
      } else {
        parts.push('0');
      }
      
      // 添加变量系数项
      for (const [varName, value] of Object.entries(this.datasetDetails.coefficients)) {
        const formattedValue = this.formatNumber(value);
        // 根据系数正负决定符号
        if (value >= 0 && parts.length > 1) {  // 如果不是第一项且系数为正
          parts.push('+', `${formattedValue} * ${varName}`);
        } else {
          parts.push(`${formattedValue < 0 ? '' : '+'} ${formattedValue} * ${varName}`);
        }
      }
      
      return parts.join(' ');
    },
    
    // 复制公式到剪贴板
    copyFormula() {
      let formulaText = `线性回归公式:\ny = ${this.formatFormulaExpression()}`;
      
      this.copyToClipboard(formulaText);
    },
    
    // 统一的复制到剪贴板方法
    copyToClipboard(csvContent) {
      // 尝试使用 Clipboard API
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(csvContent).then(() => {
          this.showCopyNotification('公式已复制到剪贴板');
          console.log('公式已复制到剪贴板');
        }).catch(err => {
          console.error('复制失败:', err);
          this.fallbackCopyTextToClipboard(csvContent);
        });
      } else {
        // 回退方案
        this.fallbackCopyTextToClipboard(csvContent);
      }
    }
  }
};
</script>

<style scoped>
.table-header {
  display: flex;
  align-items: center;
}

.copy-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.3s;
  margin-left: 10px;
}

.copy-button:hover {
  background-color: #f5f5f5;
}

.copy-button img {
  width: 16px;
  height: 16px;
}

.linear-regression-result {
  padding: 20px;
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

.stats-summary-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.stats-summary-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  border-top: 2px solid #000;
  border-bottom: 2px solid #000;
}

.stats-summary-table th {
  border-bottom: 1px solid #000;
  padding: 8px;
  text-align: center;
  white-space: nowrap;
  background-color: transparent;
  font-weight: bold;
}

.stats-summary-table td {
  padding: 8px;
  text-align: center;
  white-space: nowrap;
  border: none;
}

.no-data {
  text-align: center;
  color: #909399;
  font-style: italic;
}

h4 {
  margin: 20px 0 10px 0;
  color: #333;
  padding-bottom: 5px;
}

h5 {
  margin: 15px 0 10px 0;
  color: #666;
}

.formula-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.formula-display {
  margin-bottom: 15px;
}

.formula-math {
  font-size: 16px;
  text-align: center;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  font-family: 'Times New Roman', serif;
  font-style: italic;
}

.formula-breakdown {
  margin-top: 10px;
}

.formula-breakdown-item {
  margin: 10px 0;
  padding: 8px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
}

.formula-part {
  font-weight: bold;
  margin-right: 10px;
  min-width: 50px;
}

.formula-expression {
  font-family: 'Courier New', monospace;
  flex: 1;
}
</style>