<template>
  <div class="logistic-regression-result" v-if="datasetDetails.resultMethod === 'logistic_regression'">
    <h3>逻辑回归分析结果</h3>
    
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
      <div class="info-item">
        <span class="info-label">类别数量:</span>
        <span class="info-value">{{ datasetDetails.n_classes }}</span>
      </div>
      <div class="info-item" v-if="datasetDetails.intercept !== null && datasetDetails.intercept !== undefined">
        <span class="info-label">截距:</span>
        <span class="info-value">{{ formatNumber(datasetDetails.intercept) }}</span>
      </div>
    </div>

    <!-- 自变量列表 -->
    <div class="table-header">
      <h4>自变量 (X)</h4>
      <button class="copy-button" @click="copyTable('variables')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="variablesTable">
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

    <!-- 类别标签 -->
    <div class="table-header">
      <h4>类别标签</h4>
      <button class="copy-button" @click="copyTable('labels')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="labelsTable">
        <thead>
          <tr>
            <th>标签</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(label, index) in datasetDetails.class_labels" :key="index">
            <td>{{ label }}</td>
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
      <div 
        v-for="(coef, className) in datasetDetails.coefficients"
        :key="className"
        class="coefficient-group"
      >
        <h5 v-if="datasetDetails.n_classes > 2">{{ className }} 系数</h5>
        <table class="stats-summary-table" :ref="`coefficientsTable-${className}`">
          <thead>
            <tr>
              <th>变量</th>
              <th>系数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(value, varName) in coef" :key="varName">
              <td>{{ varName }}</td>
              <td>{{ formatNumber(value) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
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
            <td>准确率 (Accuracy)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.accuracy) }}</td>
          </tr>
          <tr v-if="datasetDetails.evaluation_metrics.precision !== null">
            <td>精确率 (Precision)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.precision) }}</td>
          </tr>
          <tr v-if="datasetDetails.evaluation_metrics.recall !== null">
            <td>召回率 (Recall)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.recall) }}</td>
          </tr>
          <tr v-if="datasetDetails.evaluation_metrics.f1_score !== null">
            <td>F1分数</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.f1_score) }}</td>
          </tr>
          <tr v-if="datasetDetails.evaluation_metrics.precision_micro !== null">
            <td>精确率 (Micro)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.precision_micro) }}</td>
          </tr>
          <tr v-if="datasetDetails.evaluation_metrics.recall_micro !== null">
            <td>召回率 (Micro)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.recall_micro) }}</td>
          </tr>
          <tr v-if="datasetDetails.evaluation_metrics.f1_micro !== null">
            <td>F1分数 (Micro)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.f1_micro) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 模型参数 -->
    <div class="table-header">
      <h4>模型参数</h4>
      <button class="copy-button" @click="copyTable('params')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="paramsTable">
        <thead>
          <tr>
            <th>参数</th>
            <th>值</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>正则化强度 (C)</td>
            <td>{{ datasetDetails.model_params.C }}</td>
          </tr>
          <tr>
            <td>优化算法</td>
            <td>{{ datasetDetails.model_params.solver }}</td>
          </tr>
          <tr>
            <td>最大迭代次数</td>
            <td>{{ datasetDetails.model_params.max_iter }}</td>
          </tr>
          <tr>
            <td>收敛容差</td>
            <td>{{ datasetDetails.model_params.tol }}</td>
          </tr>
          <tr>
            <td>拟合截距</td>
            <td>{{ datasetDetails.model_params.fit_intercept ? '是' : '否' }}</td>
          </tr>
          <tr>
            <td>类别权重</td>
            <td>{{ datasetDetails.model_params.class_weight || '无' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 混淆矩阵 -->
    <div class="table-header">
      <h4>混淆矩阵</h4>
      <button class="copy-button" @click="copyTable('confusion')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="confusionTable">
        <thead>
          <tr>
            <th></th>
            <th v-for="(label, index) in datasetDetails.class_labels" :key="'header'+index">{{ label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in datasetDetails.confusion_matrix" :key="'row'+i">
            <th>{{ datasetDetails.class_labels[i] }}</th>
            <td v-for="(value, j) in row" :key="'cell'+j">{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 逻辑回归公式 -->
    <div class="table-header">
      <h4>逻辑回归公式</h4>
      <button class="copy-button" @click="copyFormula()" title="复制公式">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="formula-container">
      <div class="formula-display">
        <div class="formula-math">P(y=1) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n)}}</div>
      </div>
      <div class="formula-breakdown" v-if="datasetDetails.coefficients">
        <div v-if="datasetDetails.n_classes === 2">
          <!-- 二分类情况 -->
          <div class="formula-breakdown-item">
            <span class="formula-part">z =</span>
            <span class="formula-expression">{{ formatFormulaExpression() }}</span>
          </div>
          <div class="formula-breakdown-item">
            <span class="formula-part">P(y=1) =</span>
            <span class="formula-expression">1 / (1 + e^(-z))</span>
          </div>
        </div>
        <div v-else>
          <!-- 多分类情况 -->
          <div v-for="(coef, className) in datasetDetails.coefficients" :key="className" class="multiclass-formula">
            <h5>{{ className }} 类别公式:</h5>
            <div class="formula-breakdown-item">
              <span class="formula-part">z_{{ className }} =</span>
              <span class="formula-expression">{{ formatFormulaExpression(coef, datasetDetails.intercept, className) }}</span>
            </div>
            <div class="formula-breakdown-item">
              <span class="formula-part">P(y={{ className }}) =</span>
              <span class="formula-expression">e^(z_{{ className }}) / (Σ e^(z_i))</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LogisticRegressionResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatNumber(value) {
      if (value === null || value === undefined) return 'N/A';
      if (typeof value === 'number') {
        // 如果是小数，保留适当的小数位数
        if (Math.abs(value) < 0.0001 && value !== 0) {
          return value.toExponential(4);
        } else if (Math.abs(value) < 1 && Math.abs(value) >= 0.0001) {
          return value.toFixed(6);
        } else if (Math.abs(value) >= 1000) {
          return value.toLocaleString(undefined, { maximumFractionDigits: 4 });
        } else {
          return Number(value.toFixed(4));
        }
      }
      return value;
    },
    copyTable(tableType) {
      let table;
      
      switch (tableType) {
        case 'variables':
          table = this.$refs.variablesTable;
          break;
        case 'labels':
          table = this.$refs.labelsTable;
          break;
        case 'coefficients':
          // 回归系数可能有多个表格，需要特殊处理
          if (this.datasetDetails && this.datasetDetails.coefficients) {
            let csvContent = '';
            
            for (const [className, coef] of Object.entries(this.datasetDetails.coefficients)) {
              // 添加类别标题（如果多类别）
              if (this.datasetDetails.n_classes > 2) {
                csvContent += `${className} 系数,\n`;
              }
              
              // 添加表头
              csvContent += '变量,系数\n';
              
              // 添加数据行
              for (const [varName, value] of Object.entries(coef)) {
                let varNameText = varName.replace(/"/g, '""');
                if (varNameText.includes(',') || varNameText.includes('\n')) {
                  varNameText = `"${varNameText}"`;
                }
                
                let valueText = this.formatNumber(value).toString().replace(/"/g, '""');
                if (valueText.includes(',') || valueText.includes('\n')) {
                  valueText = `"${valueText}"`;
                }
                
                csvContent += `${varNameText},${valueText}\n`;
              }
              
              // 添加空行分隔不同类别的系数表
              csvContent += '\n';
            }
            
            this.copyToClipboard(csvContent);
            return;
          }
          break;
        case 'evaluation':
          table = this.$refs.evaluationTable;
          break;
        case 'params':
          table = this.$refs.paramsTable;
          break;
        case 'confusion':
          table = this.$refs.confusionTable;
          break;
        default:
          console.error('未知的表格类型:', tableType);
          return;
      }

      if (!table) {
        console.error('无法找到表格元素', tableType);
        return;
      }

      // 获取表格数据
      let csvContent = '';
      const rows = Array.isArray(table) ? table[0].querySelectorAll('tr') : table.querySelectorAll('tr');

      for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cells = rows[i].querySelectorAll('th, td');

        for (let j = 0; j < cells.length; j++) {
          // 处理特殊字符和逗号
          let cellText = cells[j].innerText.replace(/"/g, '""');
          if (cellText.includes(',') || cellText.includes('\n') || cellText.includes('"')) {
            cellText = `"${cellText}"`;
          }
          row.push(cellText);
        }

        csvContent += row.join(',') + '\n';
      }

      this.copyToClipboard(csvContent);
    },
    
    // 格式化公式表达式
    formatFormulaExpression(coef = null, intercept = null, className = null) {
      // 如果没有提供特定的系数和截距，使用默认值
      if (!coef) {
        coef = this.datasetDetails.coefficients && Object.keys(this.datasetDetails.coefficients).length > 0
          ? Object.values(this.datasetDetails.coefficients)[0]
          : {};
      }
      if (intercept === null || intercept === undefined) {
        intercept = this.datasetDetails.intercept;
      }
      
      // 构建公式表达式
      let parts = [];
      
      // 添加截距项
      if (intercept !== null && intercept !== undefined) {
        parts.push(this.formatNumber(intercept));
      } else {
        parts.push('0');
      }
      
      // 添加变量系数项
      for (const [varName, value] of Object.entries(coef)) {
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
      let formulaText = '';
      
      if (this.datasetDetails.n_classes === 2) {
        // 二分类情况
        formulaText = `逻辑回归公式:\nP(y=1) = 1 / (1 + e^(-z))\n其中 z = ${this.formatFormulaExpression()}`;
      } else {
        // 多分类情况
        formulaText = `多项逻辑回归公式:\n`;
        for (const [className, coef] of Object.entries(this.datasetDetails.coefficients)) {
          formulaText += `对于类别 ${className}:\n`;
          formulaText += `z_${className} = ${this.formatFormulaExpression(coef, this.datasetDetails.intercept, className)}\n`;
          formulaText += `P(y=${className}) = e^(z_${className}) / (Σ e^(z_i))\n\n`;
        }
      }
      
      this.copyToClipboard(formulaText);
    },
    
    // 统一的复制到剪贴板方法
    copyToClipboard(csvContent) {
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

.logistic-regression-result {
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

.coefficient-group {
  margin-bottom: 20px;
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
  min-width: 120px;
}

.formula-expression {
  font-family: 'Courier New', monospace;
  flex: 1;
}

.multiclass-formula {
  margin-bottom: 15px;
}

.multiclass-formula h5 {
  margin: 10px 0 5px 0;
  color: #666;
  border-bottom: 1px dashed #d8d8d8;
  padding-bottom: 5px;
}
</style>