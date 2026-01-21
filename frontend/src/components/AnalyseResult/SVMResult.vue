<template>
  <div class="svm-result" v-if="datasetDetails && (datasetDetails.method === 'svm_classification' || datasetDetails.method === 'svm_regression')">
    <!-- 分析摘要 -->
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">任务类型:</span>
        <span class="info-value">{{ datasetDetails.task_type }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">特征列数:</span>
        <span class="info-value">{{ datasetDetails.x_columns.length }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">目标列:</span>
        <span class="info-value">{{ datasetDetails.y_column }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">样本数量:</span>
        <span class="info-value">{{ datasetDetails.sample_size }}</span>
      </div>
      <div class="info-item" v-if="datasetDetails.method === 'svm_classification'">
        <span class="info-label">类别数量:</span>
        <span class="info-value">{{ datasetDetails.n_classes }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">支持向量数量:</span>
        <span class="info-value">{{ datasetDetails.support_vectors_count }}</span>
      </div>
    </div>

    <!-- 评估指标 -->
    <div class="table-header">
      <h4>评估指标</h4>
      <button class="copy-button" @click="copyTable('metrics')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="metricsTable">
        <thead>
          <tr>
            <th>指标名称</th>
            <th>值</th>
          </tr>
        </thead>
        <tbody>
          <!-- 分类评估指标 -->
          <tr v-if="datasetDetails.method === 'svm_classification'">
            <td>准确率 (Accuracy)</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.accuracy) }}</td>
          </tr>
          <tr v-if="datasetDetails.method === 'svm_classification'">
            <td>精确率 (Precision)</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.precision) }}</td>
          </tr>
          <tr v-if="datasetDetails.method === 'svm_classification'">
            <td>召回率 (Recall)</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.recall) }}</td>
          </tr>
          <tr v-if="datasetDetails.method === 'svm_classification'">
            <td>F1分数</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.f1_score) }}</td>
          </tr>
          <!-- 回归评估指标 -->
          <tr v-if="datasetDetails.method === 'svm_regression'">
            <td>均方误差 (MSE)</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.mse) }}</td>
          </tr>
          <tr v-if="datasetDetails.method === 'svm_regression'">
            <td>均方根误差 (RMSE)</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.rmse) }}</td>
          </tr>
          <tr v-if="datasetDetails.method === 'svm_regression'">
            <td>R² 分数</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.r2_score) }}</td>
          </tr>
          <tr v-if="datasetDetails.method === 'svm_regression'">
            <td>平均绝对误差 (MAE)</td>
            <td>{{ formatMetric(datasetDetails.evaluation_metrics.mae) }}</td>
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
            <th>参数名称</th>
            <th>值</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>核函数</td>
            <td>{{ datasetDetails.model_params.kernel }}</td>
          </tr>
          <tr>
            <td>C (正则化参数)</td>
            <td>{{ datasetDetails.model_params.C }}</td>
          </tr>
          <tr>
            <td>Gamma</td>
            <td>{{ datasetDetails.model_params.gamma }}</td>
          </tr>
          <tr v-if="datasetDetails.model_params.degree !== undefined">
            <td>多项式度数</td>
            <td>{{ datasetDetails.model_params.degree }}</td>
          </tr>
          <tr v-if="datasetDetails.model_params.coef0 !== undefined">
            <td>Coefficient 0</td>
            <td>{{ datasetDetails.model_params.coef0 }}</td>
          </tr>
          <tr>
            <td>容忍度</td>
            <td>{{ datasetDetails.model_params.tol }}</td>
          </tr>
          <tr>
            <td>最大迭代次数</td>
            <td>{{ datasetDetails.model_params.max_iter }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分类特有信息 -->
    <div v-if="datasetDetails.method === 'svm_classification'">
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
              <th>类别索引</th>
              <th>类别标签</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(label, index) in datasetDetails.class_labels" :key="index">
              <td>{{ index }}</td>
              <td>{{ label }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 支持向量统计 -->
      <div class="table-header">
        <h4>各类别支持向量数</h4>
        <button class="copy-button" @click="copyTable('svPerClass')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="svPerClassTable">
          <thead>
            <tr>
              <th>类别</th>
              <th>支持向量数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(count, index) in datasetDetails.n_support_vectors_per_class" :key="index">
              <td>类别 {{ index }}</td>
              <td>{{ count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 预测结果预览 -->
    <div class="table-header">
      <h4>预测结果预览</h4>
    </div>
    <div class="predictions-info">
      <p v-if="datasetDetails.method === 'svm_classification'">前20个样本的预测标签:</p>
      <p v-else>前20个样本的预测值:</p>
      <div class="predictions-preview">
        <span
          v-for="(pred, index) in (datasetDetails.method === 'svm_classification' ? datasetDetails.predicted_labels : datasetDetails.predicted_values).slice(0, 20)"
          :key="index"
          :class="['prediction-item', datasetDetails.method === 'svm_classification' ? `class-${pred}` : 'regression-prediction']"
        >
          {{ pred }}
        </span>
        <span v-if="(datasetDetails.method === 'svm_classification' ? datasetDetails.predicted_labels : datasetDetails.predicted_values).length > 20" class="more-predictions">
          ...还有{{
            (datasetDetails.method === 'svm_classification' ? datasetDetails.predicted_labels : datasetDetails.predicted_values).length - 20
          }}个
        </span>
      </div>
    </div>

    <!-- 下载SVM结果 -->
    <div class="table-header">
      <h4>下载结果</h4>
    </div>
    <div class="download-section">
      <p>下载包含原始数据和SVM预测结果的CSV文件：</p>
      <button class="download-button" @click="downloadSVMResult" :disabled="!datasetDetails.result_file_path">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20">
          <path fill="none" d="M0 0h24v24H0z"></path>
          <path fill="currentColor" d="M1 14.5a6.496 6.496 0 0 1 3.064-5.519 8.001 8.001 0 0 1 15.872 0 6.5 6.5 0 0 1-2.936 12L7 21c-3.356-.274-6-3.078-6-6.5zm15.848 4.487a4.5 4.5 0 0 0 2.03-8.309l-.807-.503-.12-.942a6.001 6.001 0 0 0-11.903 0l-.12.942-.805.503a4.5 4.5 0 0 0 2.029 8.309l.173.013h9.35l.173-.013zM13 12h3l-4 5-4-5h3V8h2v4z"></path>
        </svg>
        下载SVM结果CSV
      </button>
      <div v-if="!datasetDetails.result_file_path" class="no-result-file">
        <p>暂无结果文件可供下载</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SVMResult',
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  methods: {
    // 下载SVM结果CSV文件
    downloadSVMResult() {
      if (!this.datasetDetails.result_file_path) {
        this.showCopyNotification('暂无结果文件可供下载', true);
        return;
      }

      // 创建下载链接
      const link = document.createElement('a');
      link.href = this.datasetDetails.result_file_path;
      link.download = `${this.datasetDetails.method}_result.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    // 复制表格数据到剪贴板
    copyTable(tableType) {
      let table;
      switch (tableType) {
        case 'metrics':
          table = this.$refs.metricsTable;
          break;
        case 'params':
          table = this.$refs.paramsTable;
          break;
        case 'labels':
          table = this.$refs.labelsTable;
          break;
        case 'svPerClass':
          table = this.$refs.svPerClassTable;
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
    
    formatMetric(value) {
      if (value === null || value === undefined) {
        return 'N/A';
      }
      // 如果是数字，格式化为保留4位小数
      if (typeof value === 'number') {
        return value.toFixed(4);
      }
      return value;
    }
  },
};
</script>

<style scoped>
.svm-result {
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

.predictions-info p {
  margin-top: 0;
  color: #606266;
}

.predictions-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.prediction-item {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  min-width: 24px;
  text-align: center;
  background-color: #409eff;
  color: white;
}

/* 为不同类别分配不同颜色 */
.prediction-item.class-0 { background-color: #c23531; }
.prediction-item.class-1 { background-color: #2f4554; }
.prediction-item.class-2 { background-color: #61a0a8; }
.prediction-item.class-3 { background-color: #d48265; }
.prediction-item.class-4 { background-color: #91c7ae; }
.prediction-item.class-5 { background-color: #749f83; }
.prediction-item.class-6 { background-color: #ca8622; }
.prediction-item.class-7 { background-color: #bda29a; }
.prediction-item.class-8 { background-color: #6e7074; }
.prediction-item.class-9 { background-color: #546570; }

.prediction-item.regression-prediction {
  background-color: #546570;
}

.more-predictions {
  color: #909399;
  font-style: italic;
}

.download-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.download-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.download-button:hover {
  background-color: #337ecc;
}

.download-button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}

.download-button img {
  width: 16px;
  height: 16px;
}

.no-result-file {
  color: #909399;
  font-style: italic;
  margin-top: 10px;
}

h4 {
  margin: 20px 0 10px 0;
  color: #333;
  padding-bottom: 5px;
}
</style>