<template>
  <div class="f-test-result" v-if="datasetDetails.resultMethod === 'f_test'">
    <!-- F检验信息 -->
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">显著性水平 (α):</span>
        <span class="info-value">{{ datasetDetails.alpha || 0.05 }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">处理列:</span>
        <span class="info-value columns-value">{{ formattedColumns }}</span>
      </div>
      <div v-if="datasetDetails.group_by" class="info-item">
        <span class="info-label">分组列:</span>
        <span class="info-value">{{ datasetDetails.group_by }}</span>
      </div>
    </div>

    <!-- 方差齐性检验结果 -->
    <div v-if="datasetDetails.f_test.variance_homogeneity" class="section">
      <div class="table-header">
        <h4>方差齐性检验 (Levene检验)</h4>
        <button class="copy-button" @click="copyTable('variance')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="varianceTable">
          <thead>
            <tr>
              <th>统计量</th>
              <th>P值</th>
              <th>显著性</th>
              <th>方差齐性</th>
              <th>列数</th>
              <th>样本量</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ formatValue(varianceHomogeneityTest.statistic) }}</td>
              <td>{{ formatValue(varianceHomogeneityTest.p_value) }}</td>
              <td>
                <span :class="varianceHomogeneityTest.significant ? 'significant' : 'not-significant'">
                  {{ varianceHomogeneityTest.significant ? '显著' : '不显著' }}
                </span>
              </td>
              <td>
                <span :class="varianceHomogeneityTest.equal_variance ? 'equal-var' : 'unequal-var'">
                  {{ varianceHomogeneityTest.equal_variance ? '是' : '否' }}
                </span>
              </td>
              <td>{{ varianceHomogeneityTest.columns?.length || '-' }}</td>
              <td>{{ varianceHomogeneityTest.sample_sizes?.join(', ') || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 方差分析结果 -->
    <div class="section">
      <div class="table-header">
        <h4>方差分析 (ANOVA)</h4>
        <button class="copy-button" @click="copyTable('anova')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="anovaTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>F统计量</th>
              <th>P值</th>
              <th>显著性</th>
              <th>组数</th>
              <th>组名</th>
              <th>样本量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, columnName) in anovaResults" :key="columnName">
              <td>{{ columnName }}</td>
              <td>{{ formatValue(item.statistic) }}</td>
              <td>{{ formatValue(item.p_value) }}</td>
              <td>
                <span :class="item.significant ? 'significant' : 'not-significant'">
                  {{ item.significant ? '显著' : '不显著' }}
                </span>
              </td>
              <td>{{ item.groups }}</td>
              <td>{{ item.group_names?.join(', ') || '-' }}</td>
              <td>{{ item.sample_sizes?.join(', ') || '-' }}</td>
            </tr>
            <tr v-if="Object.keys(anovaResults).length === 0">
              <td colspan="7" class="no-data">无统计数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 各组统计信息 -->
    <div v-if="hasGroupStats" class="section">
      <div class="table-header">
        <h4>各组统计信息</h4>
        <button class="copy-button" @click="copyTable('groupStats')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="groupStatsTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>组名</th>
              <th>平均值</th>
              <th>标准差</th>
              <th>样本量</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(item, columnName) in anovaResultsWithGroupStats" :key="columnName">
              <tr v-for="(groupStat, index) in item.group_stats" :key="`${columnName}-${index}`">
                <td v-if="index === 0" :rowspan="item.group_stats.length">{{ columnName }}</td>
                <td>{{ groupStat.name }}</td>
                <td>{{ formatValue(groupStat.mean) }}</td>
                <td>{{ formatValue(groupStat.std) }}</td>
                <td>{{ groupStat.size }}</td>
              </tr>
            </template>
            <tr v-if="!hasGroupStats">
              <td colspan="5" class="no-data">无统计数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 错误信息 -->
    <div v-if="Object.keys(errorMessages).length > 0" class="section">
      <h4>错误信息</h4>
      <div class="error-message" v-for="(error, key) in errorMessages" :key="key">
        <p><strong>{{ key }}:</strong> {{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FTestResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  computed: {
    formattedColumns() {
      const columns = this.datasetDetails.columns;
      if (!columns) return '-';
      
      // 如果是数组，将其转换为字符串并限制长度
      if (Array.isArray(columns)) {
        return columns.join(', ');
      }
      
      // 如果是字符串且包含逗号，分割并限制长度
      if (typeof columns === 'string' && columns.includes(',')) {
        const columnArray = columns.split(',').map(col => col.trim());
        return columnArray.join(', ');
      }
      
      // 其他情况直接返回
      return columns;
    },
    
    varianceHomogeneityTest() {
      return this.datasetDetails.f_test.variance_homogeneity || null;
    },
    
    anovaResults() {
      const results = {};
      Object.keys(this.datasetDetails.f_test).forEach(key => {
        if (this.datasetDetails.f_test[key].test_type === 'anova') {
          results[key] = this.datasetDetails.f_test[key];
        }
      });
      return results;
    },

    anovaResultsWithGroupStats() {
      const results = {};
      Object.keys(this.datasetDetails.f_test).forEach(key => {
        const item = this.datasetDetails.f_test[key];
        if (item.test_type === 'anova' && item.group_stats) {
          results[key] = item;
        }
      });
      return results;
    },

    hasGroupStats() {
      return Object.keys(this.anovaResultsWithGroupStats).length > 0;
    },
    
    errorMessages() {
      const errors = {};
      Object.keys(this.datasetDetails.f_test).forEach(key => {
        if (this.datasetDetails.f_test[key].error) {
          errors[key] = this.datasetDetails.f_test[key].error;
        }
      });
      return errors;
    }
  },
  methods: {
    formatValue(value) {
      if (value === null || value === undefined) return '-';
      return parseFloat(value).toFixed(4);
    },
    
    // 复制表格数据到剪贴板
    copyTable(tableType) {
      let table;
      
      switch(tableType) {
        case 'variance':
          table = this.$refs.varianceTable;
          break;
        case 'anova':
          table = this.$refs.anovaTable;
          break;
        case 'groupStats':
          table = this.$refs.groupStatsTable;
          break;
        default:
          return;
      }
      
      if (!table) {
        console.error('无法找到表格元素');
        return;
      }

      // 如果是数组（元素引用可能是数组），取第一个元素
      if (Array.isArray(table)) {
        table = table[0];
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
    }
  }
};
</script>

<style scoped>
.section {
  margin-bottom: 30px;
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

.f-test-result {
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

.columns-value {
  word-break: break-all;
  white-space: normal;
  font-size: 16px;
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

.significant {
  color: #f56c6c;
  font-weight: bold;
}

.not-significant {
  color: #67c23a;
  font-weight: bold;
}

.equal-var {
  color: #67c23a;
  font-weight: bold;
}

.unequal-var {
  color: #e6a23c;
  font-weight: bold;
}

h4 {
  margin: 20px 0 10px 0;
  color: #333;
  padding-bottom: 5px;
}

.error-message {
  padding: 15px;
  background-color: #fef0f0;
  border: 1px solid #fde2e2;
  border-radius: 4px;
  color: #f56c6c;
  margin-bottom: 20px;
}
</style>