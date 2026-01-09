<template>
  <div class="normality-test-result" v-if="datasetDetails.resultMethod === 'normality_test'">
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">检验方法:</span>
        <span class="info-value">{{ getTestMethodName(datasetDetails.method) || '-' }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">显著性水平 (α):</span>
        <span class="info-value">{{ datasetDetails.alpha || '-' }}</span>
      </div>
    </div>

    <!-- 分组结果显示 -->
    <div v-if="isGroupedResult" class="grouped-results">
      <div v-for="(groupResult, groupName) in groupedResults" :key="groupName" class="group-result">
        <h4>组: {{ groupName }}</h4>
        <div class="table-header">
          <h5>正态性检验结果</h5>
          <button class="copy-button" @click="copyTable('group-' + groupName)" title="复制表格">
            <img src="@/assets/images/copy.svg" alt="复制" />
          </button>
        </div>
        <div class="stats-summary-container">
          <table class="stats-summary-table" :ref="'groupTable-' + groupName">
            <thead>
              <tr>
                <th>列名</th>
                <th>统计量</th>
                <th>P值</th>
                <th>是否正态</th>
                <th>样本数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, columnName) in groupResult.normality_results" :key="columnName">
                <td>{{ columnName }}</td>
                <td>{{ formatValue(item.statistic) }}</td>
                <td>{{ formatValue(item.p_value) }}</td>
                <td>
                  <span :class="item.is_normal ? 'normal' : 'not-normal'">
                    {{ item.is_normal ? '是' : '否' }}
                  </span>
                </td>
                <td>{{ item.sample_size }}</td>
              </tr>
              <tr v-if="!groupResult.normality_results || Object.keys(groupResult.normality_results).length === 0">
                <td colspan="6" class="no-data">无统计数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 普通结果显示 -->
    <div v-else>
      <div class="table-header">
        <h4>正态性检验结果</h4>
        <button class="copy-button" @click="copyTable('normality')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="normalityTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>统计量</th>
              <th>P值</th>
              <th>是否正态</th>
              <th>样本数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, columnName) in normalityResults" :key="columnName">
              <td>{{ columnName }}</td>
              <td>{{ formatValue(item.statistic) }}</td>
              <td>{{ formatValue(item.p_value) }}</td>
              <td>
                <span :class="item.is_normal ? 'normal' : 'not-normal'">
                  {{ item.is_normal ? '是' : '否' }}
                </span>
              </td>
              <td>{{ item.sample_size }}</td>
            </tr>
            <tr v-if="!normalityResults || Object.keys(normalityResults).length === 0">
              <td colspan="6" class="no-data">无统计数据</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 常量列提示 -->
      <div v-if="constantColumns && constantColumns.length > 0" class="constant-columns-info">
        <h4>注意</h4>
        <p>以下列为常量列（所有值相同）：</p>
        <ul>
          <li v-for="column in constantColumns" :key="column">{{ column }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NormalityTestResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    },
  },
  computed: {
    isGroupedResult() {
      return this.datasetDetails.grouped_results !== undefined;
    },
    
    groupedResults() {
      return this.datasetDetails.grouped_results || {};
    },
    
    normalityResults() {
      return this.datasetDetails.normality_results || {};
    },
    
    constantColumns() {
      return this.datasetDetails.constant_columns || [];
    }
  },
  methods: {
    getTestMethodName(method) {
      return method === 'shapiro' ? 'Shapiro-Wilk' : 'D\'Agostino';
    },
    
    formatValue(value) {
      if (value === null || value === undefined) return '-';
      return parseFloat(value).toFixed(4);
    },
    
    // 复制表格数据到剪贴板
    copyTable(tableType) {
      let table;
      
      if (tableType.startsWith('group-')) {
        // 分组表格
        const groupName = tableType.substring(6);
        table = this.$refs[`groupTable-${groupName}`];
      } else {
        // 普通表格
        table = this.$refs.normalityTable;
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

.normality-test-result {
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

.grouped-results {
  margin-top: 20px;
}

.group-result {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.group-result h4 {
  margin-top: 0;
  color: #333;
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

.normal {
  color: #67c23a;
  font-weight: bold;
}

.not-normal {
  color: #f56c6c;
  font-weight: bold;
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

.constant-columns-info {
  background-color: #fffbe6;
  border-left: 4px solid #ffe58f;
  padding: 10px;
  margin-top: 20px;
}

.constant-columns-info h4 {
  margin-top: 0;
  color: #d48806;
}

.constant-columns-info ul {
  margin: 10px 0;
  padding-left: 20px;
}

.constant-columns-info li {
  margin-bottom: 5px;
}
</style>