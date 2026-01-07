<template>
  <div class="chi-square-test-result" v-if="datasetDetails.resultMethod === 'chi_square_test'">
    <!-- 卡方检验信息 -->
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

    <!-- 拟合优度检验结果 -->
    <div v-if="hasGoodnessOfFitResults" class="section">
      <div class="table-header">
        <h4>拟合优度检验</h4>
        <button class="copy-button" @click="copyTable('goodnessOfFit')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="goodnessOfFitTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>卡方统计量</th>
              <th>P值</th>
              <th>显著性</th>
              <th>类别数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, columnName) in goodnessOfFitResults" :key="columnName">
              <td>{{ columnName }}</td>
              <td>{{ formatValue(item.statistic) }}</td>
              <td>{{ formatValue(item.p_value) }}</td>
              <td>
                <span :class="item.significant ? 'significant' : 'not-significant'">
                  {{ item.significant ? '显著' : '不显著' }}
                </span>
              </td>
              <td>{{ item.categories?.length || '-' }}</td>
            </tr>
            <tr v-if="Object.keys(goodnessOfFitResults).length === 0">
              <td colspan="5" class="no-data">无统计数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 独立性检验结果 -->
    <div v-if="hasIndependenceResults" class="section">
      <div class="table-header">
        <h4>独立性检验</h4>
        <button class="copy-button" @click="copyTable('independence')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="independenceTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>卡方统计量</th>
              <th>P值</th>
              <th>自由度</th>
              <th>显著性</th>
              <th>警告</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, columnName) in independenceResults" :key="columnName">
              <td>{{ columnName }}</td>
              <td>{{ formatValue(item.statistic) }}</td>
              <td>{{ formatValue(item.p_value) }}</td>
              <td>{{ item.degrees_of_freedom }}</td>
              <td>
                <span :class="item.significant ? 'significant' : 'not-significant'">
                  {{ item.significant ? '显著' : '不显著' }}
                </span>
              </td>
              <td>
                <span v-if="item.warning" class="warning">{{ item.warning }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr v-if="Object.keys(independenceResults).length === 0">
              <td colspan="6" class="no-data">无统计数据</td>
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
  name: "ChiSquareTestResult",
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
    
    goodnessOfFitResults() {
      const results = {};
      Object.keys(this.datasetDetails.chi_square_test).forEach(key => {
        if (this.datasetDetails.chi_square_test[key].test_type === 'goodness_of_fit') {
          results[key] = this.datasetDetails.chi_square_test[key];
        }
      });
      return results;
    },
    
    independenceResults() {
      const results = {};
      Object.keys(this.datasetDetails.chi_square_test).forEach(key => {
        if (this.datasetDetails.chi_square_test[key].test_type === 'independence') {
          results[key] = this.datasetDetails.chi_square_test[key];
        }
      });
      return results;
    },
    
    hasGoodnessOfFitResults() {
      return Object.keys(this.goodnessOfFitResults).length > 0;
    },
    
    hasIndependenceResults() {
      return Object.keys(this.independenceResults).length > 0;
    },
    
    errorMessages() {
      const errors = {};
      Object.keys(this.datasetDetails.chi_square_test).forEach(key => {
        if (this.datasetDetails.chi_square_test[key].error) {
          errors[key] = this.datasetDetails.chi_square_test[key].error;
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
        case 'goodnessOfFit':
          table = this.$refs.goodnessOfFitTable;
          break;
        case 'independence':
          table = this.$refs.independenceTable;
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

.chi-square-test-result {
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

.warning {
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