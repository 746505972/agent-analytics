<template>
  <div class="clustering-result" v-if="datasetDetails.resultMethod === 'clustering_analysis'">
    <!-- 分析摘要 -->
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">聚类方法:</span>
        <span class="info-value">{{ clusteringData.method }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">特征列数:</span>
        <span class="info-value">{{ clusteringData.columns.length }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">簇数量:</span>
        <span class="info-value">{{ clusteringData.n_clusters }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">样本数量:</span>
        <span class="info-value">{{ clusteringData.sample_size }}</span>
      </div>
    </div>

    <!-- 评估指标 -->
    <div class="table-header">
      <h4>评估指标</h4>
      <button class="copy-button" @click="copyTable('metrics')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div v-if="clusteringData.evaluation_metrics &&
      (clusteringData.evaluation_metrics.silhouette_score ||
       clusteringData.evaluation_metrics.calinski_harabasz_score)" class="stats-summary-container">
      <table class="stats-summary-table" ref="metricsTable">
        <thead>
          <tr>
            <th>指标名称</th>
            <th>值</th>
            <th>描述</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="clusteringData.evaluation_metrics.silhouette_score !== null">
            <td>轮廓系数</td>
            <td>{{ clusteringData.evaluation_metrics.silhouette_score.toFixed(4) }}</td>
            <td>衡量聚类的紧密度和分离度，值越接近1越好</td>
          </tr>
          <tr v-if="clusteringData.evaluation_metrics.calinski_harabasz_score !== null">
            <td>Calinski-Harabasz指数</td>
            <td>{{ clusteringData.evaluation_metrics.calinski_harabasz_score.toFixed(2) }}</td>
            <td>簇间离散度与簇内离散度的比值，值越大越好</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 簇统计信息 -->
    <div class="table-header">
      <h4>簇统计信息</h4>
      <button class="copy-button" @click="copyTable('clusterStats')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="stats-summary-container">
      <table class="stats-summary-table" ref="clusterStatsTable">
        <thead>
          <tr>
            <th>簇ID</th>
            <th>样本数量</th>
            <th>占比(%)</th>
            <th>中心点坐标</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(stats, clusterId) in clusteringData.cluster_stats"
            :key="clusterId"
          >
            <td>簇 {{ clusterId }}</td>
            <td>{{ stats.size }}</td>
            <td>{{ (stats.proportion * 100).toFixed(2) }}%</td>
            <td>
              <div
                v-for="(value, feature) in stats.centroid"
                :key="feature"
                class="feature-value"
              >
                <span class="feature-name">{{ feature }}:</span>
                <span class="feature-val">{{ value !== null ? value.toFixed(4) : 'N/A' }}</span>
              </div>
            </td>
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
            <td>簇数量</td>
            <td>{{ clusteringData.model_params.n_clusters }}</td>
          </tr>
          <tr>
            <td>标准化</td>
            <td>{{ clusteringData.model_params.standardize ? '是' : '否' }}</td>
          </tr>
          <tr>
            <td>最大迭代次数</td>
            <td>{{ clusteringData.model_params.max_iter }}</td>
          </tr>
          <!-- 算法特定参数 -->
          <tr v-if="clusteringData.method === 'kmeans'">
            <td>初始化方法</td>
            <td>{{ clusteringData.model_params.init }}</td>
          </tr>
          <tr v-if="clusteringData.method === 'dbscan'">
            <td>邻域半径(eps)</td>
            <td>{{ clusteringData.model_params.eps }}</td>
          </tr>
          <tr v-if="clusteringData.method === 'dbscan'">
            <td>最小样本数</td>
            <td>{{ clusteringData.model_params.min_samples }}</td>
          </tr>
          <tr v-if="clusteringData.method === 'hierarchical'">
            <td>链接方法</td>
            <td>{{ clusteringData.model_params.linkage }}</td>
          </tr>
          <tr v-if="clusteringData.method === 'gmm'">
            <td>协方差类型</td>
            <td>{{ clusteringData.model_params.covariance_type }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 聚类标签 -->
    <div class="table-header">
      <h4>聚类标签</h4>
      <button class="copy-button" @click="copyTable('labels')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div class="labels-info">
      <p>前20个样本的聚类标签:</p>
      <div class="labels-preview">
        <span
          v-for="(label, index) in clusteringData.cluster_labels.slice(0, 20)"
          :key="index"
          :class="['label-item', `cluster-${label}`]"
        >
          {{ label }}
        </span>
        <span v-if="clusteringData.cluster_labels.length > 20" class="more-labels">...还有{{ clusteringData.cluster_labels.length - 20 }}个</span>
      </div>
    </div>

    <!-- 下载聚类结果 -->
    <div class="table-header">
      <h4>下载结果</h4>
    </div>
    <div class="download-section">
      <p>下载包含原始数据和聚类标签的CSV文件：</p>
      <button class="download-button" @click="downloadClusteringResult" :disabled="!clusteringData.result_file_path">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20">
          <path fill="none" d="M0 0h24v24H0z"></path>
          <path fill="currentColor" d="M1 14.5a6.496 6.496 0 0 1 3.064-5.519 8.001 8.001 0 0 1 15.872 0 6.5 6.5 0 0 1-2.936 12L7 21c-3.356-.274-6-3.078-6-6.5zm15.848 4.487a4.5 4.5 0 0 0 2.03-8.309l-.807-.503-.12-.942a6.001 6.001 0 0 0-11.903 0l-.12.942-.805.503a4.5 4.5 0 0 0 2.029 8.309l.173.013h9.35l.173-.013zM13 12h3l-4 5-4-5h3V8h2v4z"></path>
        </svg>
        下载聚类结果CSV
      </button>
      <div v-if="!clusteringData.result_file_path" class="no-result-file">
        <p>暂无结果文件可供下载</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClusteringResult',
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  computed: {
    clusteringData() {
      return this.datasetDetails;

    }
  },
  methods: {
    // 下载聚类结果CSV文件
    downloadClusteringResult() {
      if (!this.clusteringData.result_file_path) {
        this.showCopyNotification('暂无结果文件可供下载', true);
        return;
      }

      // 创建下载链接
      const link = document.createElement('a');
      link.href = this.clusteringData.result_file_path;
      link.download = `clustering_result.csv`;
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
        case 'clusterStats':
          table = this.$refs.clusterStatsTable;
          break;
        case 'params':
          table = this.$refs.paramsTable;
          break;
        case 'labels':
          // 聚类标签不适用表格复制，可以添加其他复制逻辑
          this.copyLabels();
          return;
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
    
    // 复制聚类标签
    copyLabels() {
      const labels = this.clusteringData.cluster_labels.join(', ');
      const textToCopy = `聚类标签: [${labels}]`;
      
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(() => {
          this.showCopyNotification('聚类标签已复制到剪贴板');
        }).catch(err => {
          console.error('复制失败:', err);
          this.fallbackCopyTextToClipboard(textToCopy);
        });
      } else {
        this.fallbackCopyTextToClipboard(textToCopy);
      }
    }
  },
};
</script>

<style scoped>
.clustering-result {
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

.feature-value {
  display: flex;
  justify-content: space-between;
  padding: 3px 0;
  font-size: 13px;
}

.feature-name {
  color: #909399;
}

.feature-val {
  color: #303133;
  font-weight: 500;
}

.labels-info p {
  margin-top: 0;
  color: #606266;
}

.labels-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.label-item {
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

/* 为不同簇分配不同颜色 */
.label-item.cluster-0 { background-color: #c23531; }
.label-item.cluster-1 { background-color: #2f4554; }
.label-item.cluster-2 { background-color: #61a0a8; }
.label-item.cluster-3 { background-color: #d48265; }
.label-item.cluster-4 { background-color: #91c7ae; }
.label-item.cluster-5 { background-color: #749f83; }
.label-item.cluster-6 { background-color: #ca8622; }
.label-item.cluster-7 { background-color: #bda29a; }
.label-item.cluster-8 { background-color: #6e7074; }
.label-item.cluster-9 { background-color: #546570; }

.more-labels {
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