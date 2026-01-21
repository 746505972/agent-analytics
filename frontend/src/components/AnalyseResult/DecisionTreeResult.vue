<template>
  <div class="decision-tree-result" v-if="datasetDetails.resultMethod === 'decision_tree' || datasetDetails.method === 'decision_tree_classification' || datasetDetails.method === 'decision_tree_regression'">
    <h3>决策树分析结果</h3>
    
    <!-- 模型信息 -->
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">任务类型:</span>
        <span class="info-value">{{ isClassification ? '分类' : '回归' }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">算法方法:</span>
        <span class="info-value">{{ datasetDetails.method }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">分割标准:</span>
        <span class="info-value">{{ datasetDetails.criterion }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">因变量 (Y):</span>
        <span class="info-value">{{ datasetDetails.y_column }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">样本数量:</span>
        <span class="info-value">{{ datasetDetails.sample_size }}</span>
      </div>
      <div class="info-item" v-if="datasetDetails.train_size !== undefined">
        <span class="info-label">训练集大小:</span>
        <span class="info-value">{{ datasetDetails.train_size }}</span>
      </div>
      <div class="info-item" v-if="datasetDetails.test_size !== undefined">
        <span class="info-label">测试集大小:</span>
        <span class="info-value">{{ datasetDetails.test_size }}</span>
      </div>
      <div class="info-item" v-if="datasetDetails.n_classes !== undefined">
        <span class="info-label">类别数量:</span>
        <span class="info-value">{{ datasetDetails.n_classes }}</span>
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

    <!-- 类别标签 (仅分类任务) -->
    <div class="table-header" v-if="isClassification && datasetDetails.class_labels">
      <h4>类别标签</h4>
      <button class="copy-button" @click="copyTable('labels')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container" v-if="isClassification && datasetDetails.class_labels">
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

    <!-- 特征重要性 -->
    <div class="table-header">
      <h4>特征重要性</h4>
      <button class="copy-button" @click="copyTable('importance')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="importanceTable">
        <thead>
          <tr>
            <th>特征</th>
            <th>重要性</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(importance, feature) in datasetDetails.feature_importance" :key="feature">
            <td>{{ feature }}</td>
            <td>{{ formatNumber(importance) }}</td>
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
          <!-- 分类任务指标 -->
          <tr v-if="isClassification && datasetDetails.evaluation_metrics.accuracy !== null && datasetDetails.evaluation_metrics.accuracy !== undefined">
            <td>准确率 (Accuracy)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.accuracy) }}</td>
          </tr>
          <tr v-if="isClassification && datasetDetails.evaluation_metrics.precision !== null && datasetDetails.evaluation_metrics.precision !== undefined">
            <td>精确率 (Precision)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.precision) }}</td>
          </tr>
          <tr v-if="isClassification && datasetDetails.evaluation_metrics.recall !== null && datasetDetails.evaluation_metrics.recall !== undefined">
            <td>召回率 (Recall)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.recall) }}</td>
          </tr>
          <tr v-if="isClassification && datasetDetails.evaluation_metrics.f1_score !== null && datasetDetails.evaluation_metrics.f1_score !== undefined">
            <td>F1分数</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.f1_score) }}</td>
          </tr>
          
          <!-- 回归任务指标 -->
          <tr v-if="!isClassification && datasetDetails.evaluation_metrics.mse !== null && datasetDetails.evaluation_metrics.mse !== undefined">
            <td>均方误差 (MSE)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.mse) }}</td>
          </tr>
          <tr v-if="!isClassification && datasetDetails.evaluation_metrics.rmse !== null && datasetDetails.evaluation_metrics.rmse !== undefined">
            <td>均方根误差 (RMSE)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.rmse) }}</td>
          </tr>
          <tr v-if="!isClassification && datasetDetails.evaluation_metrics.mae !== null && datasetDetails.evaluation_metrics.mae !== undefined">
            <td>平均绝对误差 (MAE)</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.mae) }}</td>
          </tr>
          <tr v-if="!isClassification && datasetDetails.evaluation_metrics.r2_score !== null && datasetDetails.evaluation_metrics.r2_score !== undefined">
            <td>R² 得分</td>
            <td>{{ formatNumber(datasetDetails.evaluation_metrics.r2_score) }}</td>
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
            <td>分割标准</td>
            <td>{{ datasetDetails.model_params.criterion }}</td>
          </tr>
          <tr v-if="datasetDetails.model_params.max_depth !== null && datasetDetails.model_params.max_depth !== undefined">
            <td>最大深度</td>
            <td>{{ datasetDetails.model_params.max_depth }}</td>
          </tr>
          <tr>
            <td>最小分割样本数</td>
            <td>{{ datasetDetails.model_params.min_samples_split }}</td>
          </tr>
          <tr>
            <td>叶节点最小样本数</td>
            <td>{{ datasetDetails.model_params.min_samples_leaf }}</td>
          </tr>
          <tr v-if="datasetDetails.model_params.max_features !== null && datasetDetails.model_params.max_features !== undefined">
            <td>特征数量策略</td>
            <td>{{ datasetDetails.model_params.max_features }}</td>
          </tr>
          <tr>
            <td>随机种子</td>
            <td>{{ datasetDetails.model_params.random_state }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 混淆矩阵 (仅分类任务) -->
    <div class="table-header" v-if="isClassification && datasetDetails.confusion_matrix">
      <h4>混淆矩阵</h4>
      <button class="copy-button" @click="copyTable('confusion')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container" v-if="isClassification && datasetDetails.confusion_matrix">
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
  </div>
</template>

<script>
export default {
  name: "DecisionTreeResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  computed: {
    isClassification() {
      return this.datasetDetails.method === 'decision_tree_classification' || 
             (this.datasetDetails.n_classes !== undefined && this.datasetDetails.n_classes > 0);
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
        case 'importance':
          table = this.$refs.importanceTable;
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

.decision-tree-result {
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
</style>