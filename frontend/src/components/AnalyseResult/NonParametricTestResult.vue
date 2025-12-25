<template>
  <div class="non-parametric-result">
    <div v-if="datasetDetails.non_parametric_test">
      <!-- Mann-Whitney U检验结果 -->
      <div v-if="datasetDetails.test_type === 'mannwhitney'" class="mannwhitney-section">
        <div class="table-header">
          <h4>Mann-Whitney U检验结果</h4>
          <button class="copy-button" @click="copyTable('mannwhitney')" title="复制表格">
            <img src="@/assets/images/copy.svg" alt="复制" />
          </button>
        </div>
        <div class="stats-summary-container">
          <table class="stats-summary-table" ref="mannwhitneyTable">
            <thead>
              <tr>
                <th>列名</th>
                <th>统计量</th>
                <th>P值</th>
                <th>显著性</th>
                <th>组1中位数</th>
                <th>组2中位数</th>
                <th>组1大小</th>
                <th>组2大小</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, columnName) in nonParametricResults" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ formatValue(item.statistic) }}</td>
                <td>{{ formatValue(item.p_value) }}</td>
                <td>
                  <span :class="item.significant ? 'significant' : 'not-significant'">
                    {{ item.significant ? '显著' : '不显著' }}
                  </span>
                </td>
                <td>{{ formatValue(item.group1.median) }}</td>
                <td>{{ formatValue(item.group2.median) }}</td>
                <td>{{ item.group1.size }}</td>
                <td>{{ item.group2.size }}</td>
              </tr>
              <tr v-if="!nonParametricResults || Object.keys(nonParametricResults).length === 0">
                <td colspan="8" class="no-data">无统计数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Wilcoxon符号秩检验结果 -->
      <div v-else-if="datasetDetails.test_type === 'wilcoxon'" class="wilcoxon-section">
        <div class="table-header">
          <h4>Wilcoxon符号秩检验结果</h4>
          <button class="copy-button" @click="copyTable('wilcoxon')" title="复制表格">
            <img src="@/assets/images/copy.svg" alt="复制" />
          </button>
        </div>
        <div class="stats-summary-container">
          <table class="stats-summary-table" ref="wilcoxonTable">
            <thead>
              <tr>
                <th>列1</th>
                <th>列2</th>
                <th>统计量</th>
                <th>P值</th>
                <th>显著性</th>
                <th>中位差</th>
                <th>均值差</th>
                <th>样本数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="pairedResult">
                <td>{{ pairedResult.column1 }}</td>
                <td>{{ pairedResult.column2 }}</td>
                <td>{{ formatValue(pairedResult.statistic) }}</td>
                <td>{{ formatValue(pairedResult.p_value) }}</td>
                <td>
                  <span :class="pairedResult.significant ? 'significant' : 'not-significant'">
                    {{ pairedResult.significant ? '显著' : '不显著' }}
                  </span>
                </td>
                <td>{{ formatValue(pairedResult.median_difference) }}</td>
                <td>{{ formatValue(pairedResult.mean_difference) }}</td>
                <td>{{ pairedResult.sample_size }}</td>
              </tr>
              <tr v-else>
                <td colspan="8" class="no-data">无统计数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Kruskal-Wallis检验结果 -->
      <div v-else-if="datasetDetails.test_type === 'kruskal'" class="kruskal-section">
        <div class="table-header">
          <h4>Kruskal-Wallis检验结果</h4>
          <button class="copy-button" @click="copyTable('kruskal')" title="复制表格">
            <img src="@/assets/images/copy.svg" alt="复制" />
          </button>
        </div>
        <div class="stats-summary-container">
          <table class="stats-summary-table" ref="kruskalTable">
            <thead>
              <tr>
                <th>列名</th>
                <th>统计量</th>
                <th>P值</th>
                <th>显著性</th>
                <th>组数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, columnName) in nonParametricResults" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ formatValue(item.statistic) }}</td>
                <td>{{ formatValue(item.p_value) }}</td>
                <td>
                  <span :class="item.significant ? 'significant' : 'not-significant'">
                    {{ item.significant ? '显著' : '不显著' }}
                  </span>
                </td>
                <td>{{ item.groups || '-' }}</td>
              </tr>
              <tr v-if="!nonParametricResults || Object.keys(nonParametricResults).length === 0">
                <td colspan="5" class="no-data">无统计数据</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Kruskal-Wallis分组统计信息 -->
        <div v-if="kruskalGroupStats && Object.keys(kruskalGroupStats).length > 0" class="group-stats-section">
          <h4>分组统计信息</h4>
          <div v-for="(groupStats, columnName) in kruskalGroupStats" :key="columnName" class="group-stats-container">
            <h5>{{ columnName }}</h5>
            <table class="stats-summary-table">
              <thead>
                <tr>
                  <th>组名</th>
                  <th>中位数</th>
                  <th>大小</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="group in groupStats" :key="group.name">
                  <td>{{ group.name }}</td>
                  <td>{{ formatValue(group.median) }}</td>
                  <td>{{ group.size }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Kolmogorov-Smirnov检验结果 -->
      <div v-else-if="datasetDetails.test_type === 'kolmogorov_smirnov'" class="ks-section">
        <div class="table-header">
          <h4>Kolmogorov-Smirnov检验结果</h4>
          <button class="copy-button" @click="copyTable('ks')" title="复制表格">
            <img src="@/assets/images/copy.svg" alt="复制" />
          </button>
        </div>
        <div class="stats-summary-container">
          <table class="stats-summary-table" ref="ksTable">
            <thead>
              <tr>
                <th>列名</th>
                <th>统计量</th>
                <th>P值</th>
                <th>显著性</th>
                <th>理论分布</th>
                <th>样本数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, columnName) in nonParametricResults" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ formatValue(item.statistic) }}</td>
                <td>{{ formatValue(item.p_value) }}</td>
                <td>
                  <span :class="item.significant ? 'significant' : 'not-significant'">
                    {{ item.significant ? '显著' : '不显著' }}
                  </span>
                </td>
                <td>{{ item.distribution || '-' }}</td>
                <td>{{ item.sample_size || '-' }}</td>
              </tr>
              <tr v-if="!nonParametricResults || Object.keys(nonParametricResults).length === 0">
                <td colspan="6" class="no-data">无统计数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 通用错误信息 -->
      <div v-if="hasErrors" class="error-section">
        <h4>错误信息</h4>
        <div v-for="(item, columnName) in nonParametricResults" :key="columnName" v-if="item.error" class="error-item">
          <p><strong>{{ columnName }}:</strong> {{ item.error }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>暂无非参数检验结果</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "NonParametricTestResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  computed: {
    nonParametricResults() {
      if (!this.datasetDetails.non_parametric_test) {
        return {};
      }
      // 过滤掉错误结果，只返回有效的检验结果
      const results = {};
      for (const [key, value] of Object.entries(this.datasetDetails.non_parametric_test)) {
        if (!value.error) {
          results[key] = value;
        }
      }
      return results;
    },
    
    pairedResult() {
      if (!this.datasetDetails.non_parametric_test) {
        return null;
      }
      // 检查是否是配对检验结果
      const pairedTest = this.datasetDetails.non_parametric_test.paired_test;
      if (pairedTest && !pairedTest.error) {
        return pairedTest;
      }
      return null;
    },
    
    kruskalGroupStats() {
      if (!this.datasetDetails.non_parametric_test || this.datasetDetails.test_type !== 'kruskal') {
        return {};
      }
      
      const groupStats = {};
      for (const [key, value] of Object.entries(this.datasetDetails.non_parametric_test)) {
        if (value.group_stats) {
          groupStats[key] = value.group_stats;
        }
      }
      return groupStats;
    },
    
    hasErrors() {
      if (!this.datasetDetails.non_parametric_test) {
        return false;
      }
      return Object.values(this.datasetDetails.non_parametric_test).some(item => item.error);
    }
  },
  methods: {
    formatValue(value) {
      if (value === null || value === undefined) {
        return '-';
      }
      if (typeof value === 'number') {
        if (Math.abs(value) >= 0.001 || Math.abs(value) === 0) {
          return value.toFixed(4);
        } else {
          return value.toExponential(4);
        }
      }
      return String(value);
    },
    
    copyTable(tableName) {
      let tableRef;
      switch(tableName) {
        case 'mannwhitney':
          tableRef = this.$refs.mannwhitneyTable;
          break;
        case 'wilcoxon':
          tableRef = this.$refs.wilcoxonTable;
          break;
        case 'kruskal':
          tableRef = this.$refs.kruskalTable;
          break;
        case 'ks':
          tableRef = this.$refs.ksTable;
          break;
        default:
          return;
      }
      
      if (!tableRef) return;
      
      const rows = Array.from(tableRef.querySelectorAll('tr'));
      const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => `"${cell.innerText.replace(/"/g, '""')}"`).join(',');
      }).join('\n');
      
      navigator.clipboard.writeText(csvContent)
        .then(() => {
          this.showCopyNotification('表格数据已复制到剪贴板');
          console.log(`${tableName} 表格已复制到剪贴板`);
        })
        .catch(err => {
          console.error('复制失败:', err);
        });
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
.non-parametric-result {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.table-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.copy-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.copy-button:hover {
  background-color: #f0f0f0;
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
  margin-bottom: 20px;
}

.stats-summary-table th,
.stats-summary-table td {
  border: 1px solid #e0e0e0;
  padding: 8px 12px;
  text-align: left;
}

.stats-summary-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #333;
}

.stats-summary-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.significant {
  color: #e74c3c;
  font-weight: bold;
}

.not-significant {
  color: #27ae60;
}

.no-data {
  text-align: center;
  color: #999;
  font-style: italic;
}

.error-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #fef6f6;
  border: 1px solid #fde2e2;
  border-radius: 4px;
}

.error-item {
  margin: 5px 0;
  color: #c0392b;
}

.group-stats-container {
  margin-bottom: 20px;
}

.group-stats-container h5 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}
</style>