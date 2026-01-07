<template>
  <div class="t-test-result" v-if="datasetDetails.resultMethod === 't_test'">
    <!-- 正态性检验结果 -->
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">检验类型:</span>
        <span class="info-value">{{ getTestTypeName(testType) }}</span>
      </div>
      <div class="info-item">
        <span class="info-label">显著性水平 (α):</span>
        <span class="info-value">{{ datasetDetails.alpha || 0.05 }}</span>
      </div>
    </div>

    <div class="table-header">
      <h4>正态性检验</h4>
      <button class="copy-button" @click="copyTable('normality')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div v-if="datasetDetails.normality_test" class="stats-summary-container">
      <table class="stats-summary-table" ref="normalityTable">
        <thead>
          <tr>
            <th>列名</th>
            <th>检验方法</th>
            <th>统计量</th>
            <th>P值</th>
            <th>是否正态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in normalityTableData" :key="item.column">
            <td>{{ item.column }}</td>
            <td>{{ item.method }}</td>
            <td>{{ item.statistic }}</td>
            <td>{{ item.pValue }}</td>
            <td>
              <span :class="item.isNormal ? 'normal' : 'not-normal'">
                {{ item.isNormal ? '是' : '否' }}
              </span>
            </td>
          </tr>
          <tr v-if="!datasetDetails.normality_test || Object.keys(datasetDetails.normality_test).length === 0">
            <td colspan="5" class="no-data">无统计数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- T检验结果 -->
    <div class="table-header">
      <h4>T检验结果</h4>
      <button class="copy-button" @click="copyTable('ttest')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <div v-if="testType === 'one_sample'" class="stats-summary-container">
      <table class="stats-summary-table" ref="oneSampleTable">
        <thead>
          <tr>
            <th>列名</th>
            <th>样本均值</th>
            <th>总体均值</th>
            <th>T统计量</th>
            <th>P值</th>
            <th>显著性</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in oneSampleTableData" :key="item.column">
            <td>{{ item.column }}</td>
            <td>{{ item.sampleMean }}</td>
            <td>{{ item.popMean }}</td>
            <td>{{ item.statistic }}</td>
            <td>{{ item.pValue }}</td>
            <td>
              <span :class="item.significant ? 'significant' : 'not-significant'">
                {{ item.significant ? '显著' : '不显著' }}
              </span>
            </td>
          </tr>
          <tr v-if="!datasetDetails.t_test || Object.keys(datasetDetails.t_test).length === 0">
            <td colspan="6" class="no-data">无统计数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="testType === 'independent'">
      <div class="table-header">
        <h5>方差齐性检验</h5>
        <button class="copy-button" @click="copyTable('variance')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div v-if="datasetDetails.t_test && datasetDetails.t_test.variance_test" class="stats-summary-container">
        <table class="stats-summary-table" ref="varianceTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>Levene统计量</th>
              <th>Levene P值</th>
              <th>方差相等</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in varianceTableData" :key="item.column">
              <td>{{ item.column }}</td>
              <td>{{ item.leveneStat }}</td>
              <td>{{ item.leveneP }}</td>
              <td>
                <span :class="item.equalVariance ? 'equal-var' : 'unequal-var'">
                  {{ item.equalVariance ? '是' : '否' }}
                </span>
              </td>
            </tr>
            <tr v-if="!datasetDetails.t_test.variance_test || Object.keys(datasetDetails.t_test.variance_test).length === 0">
              <td colspan="4" class="no-data">无统计数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-header">
        <h5>独立样本T检验</h5>
        <button class="copy-button" @click="copyTable('independent')" title="复制表格">
          <img src="@/assets/images/copy.svg" alt="复制" />
        </button>
      </div>
      <div class="stats-summary-container">
        <table class="stats-summary-table" ref="independentTable">
          <thead>
            <tr>
              <th>列名</th>
              <th>组1名称</th>
              <th>组1均值</th>
              <th>组2名称</th>
              <th>组2均值</th>
              <th>T统计量</th>
              <th>P值</th>
              <th>显著性</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in independentTableData" :key="item.column">
              <td>{{ item.column }}</td>
              <td>{{ item.group1Name }}</td>
              <td>{{ item.group1Mean }}</td>
              <td>{{ item.group2Name }}</td>
              <td>{{ item.group2Mean }}</td>
              <td>{{ item.statistic }}</td>
              <td>{{ item.pValue }}</td>
              <td>
                <span :class="item.significant ? 'significant' : 'not-significant'">
                  {{ item.significant ? '显著' : '不显著' }}
                </span>
              </td>
            </tr>
            <tr v-if="!datasetDetails.t_test || independentTableData.length === 0">
              <td colspan="8" class="no-data">无统计数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else-if="testType === 'paired'" class="stats-summary-container">
      <table class="stats-summary-table" ref="pairedTable">
        <thead>
          <tr>
            <th>列1</th>
            <th>列2</th>
            <th>均值差</th>
            <th>T统计量</th>
            <th>P值</th>
            <th>显著性</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pairedTableData" :key="item.column1 + '-' + item.column2">
            <td>{{ item.column1 }}</td>
            <td>{{ item.column2 }}</td>
            <td>{{ item.meanDiff }}</td>
            <td>{{ item.statistic }}</td>
            <td>{{ item.pValue }}</td>
            <td>
              <span :class="item.significant ? 'significant' : 'not-significant'">
                {{ item.significant ? '显著' : '不显著' }}
              </span>
            </td>
          </tr>
          <tr v-if="!datasetDetails.t_test || pairedTableData.length === 0">
            <td colspan="6" class="no-data">无统计数据</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "TTestResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  computed: {
    testType() {
      return this.datasetDetails.test_type || 'one_sample';
    },
    
    normalityTableData() {
      if (!this.datasetDetails.normality_test) return [];
      
      return Object.keys(this.datasetDetails.normality_test).map(key => {
        const item = this.datasetDetails.normality_test[key];
        return {
          column: key,
          method: item.method === 'shapiro' ? 'Shapiro-Wilk' : 'D\'Agostino',
          statistic: item.statistic ? item.statistic.toFixed(4) : '-',
          pValue: item.p_value ? item.p_value.toFixed(4) : '-',
          isNormal: item.is_normal
        };
      });
    },
    
    oneSampleTableData() {
      if (!this.datasetDetails.t_test || this.testType !== 'one_sample') return [];
      
      return Object.keys(this.datasetDetails.t_test).map(key => {
        const item = this.datasetDetails.t_test[key];
        if (item.test_type !== 'one_sample') return null;
        
        return {
          column: key,
          sampleMean: item.sample_mean ? item.sample_mean.toFixed(4) : '-',
          popMean: item.popmean,
          statistic: item.statistic ? item.statistic.toFixed(4) : '-',
          pValue: item.p_value ? item.p_value.toFixed(4) : '-',
          significant: item.significant
        };
      }).filter(item => item !== null);
    },
    
    independentTableData() {
      if (!this.datasetDetails.t_test || this.testType !== 'independent') return [];
      
      return Object.keys(this.datasetDetails.t_test).map(key => {
        const item = this.datasetDetails.t_test[key];
        if (item.test_type !== 'independent' || !item.group1) return null;
        
        return {
          column: key,
          group1Name: item.group1.name,
          group1Mean: item.group1.mean ? item.group1.mean.toFixed(4) : '-',
          group2Name: item.group2.name,
          group2Mean: item.group2.mean ? item.group2.mean.toFixed(4) : '-',
          statistic: item.statistic ? item.statistic.toFixed(4) : '-',
          pValue: item.p_value ? item.p_value.toFixed(4) : '-',
          significant: item.significant
        };
      }).filter(item => item !== null);
    },
    
    pairedTableData() {
      if (!this.datasetDetails.t_test || this.testType !== 'paired') return [];
      
      const pairedTest = this.datasetDetails.t_test.paired_test;
      if (!pairedTest) return [];
      
      return [{
        column1: pairedTest.column1,
        column2: pairedTest.column2,
        meanDiff: pairedTest.mean_difference ? pairedTest.mean_difference.toFixed(4) : '-',
        statistic: pairedTest.statistic ? pairedTest.statistic.toFixed(4) : '-',
        pValue: pairedTest.p_value ? pairedTest.p_value.toFixed(4) : '-',
        significant: pairedTest.significant
      }];
    },
    
    varianceTableData() {
      if (!this.datasetDetails.t_test || !this.datasetDetails.t_test.variance_test) return [];
      
      return Object.keys(this.datasetDetails.t_test.variance_test).map(key => {
        const item = this.datasetDetails.t_test.variance_test[key];
        if (!item.levene) return null;
        
        return {
          column: key,
          leveneStat: item.levene.statistic ? item.levene.statistic.toFixed(4) : '-',
          leveneP: item.levene.p_value ? item.levene.p_value.toFixed(4) : '-',
          equalVariance: item.levene.equal_variance
        };
      }).filter(item => item !== null);
    }
  },
  methods: {
    getTestTypeName(type) {
      const typeMap = {
        'one_sample': '单样本T检验',
        'independent': '独立样本T检验',
        'paired': '配对样本T检验'
      };
      return typeMap[type] || '未知检验类型';
    },
    
    // 复制表格数据到剪贴板
    copyTable(tableType) {
      let table;
      switch (tableType) {
        case 'normality':
          table = this.$refs.normalityTable;
          break;
        case 'ttest':
          if (this.testType === 'one_sample') {
            table = this.$refs.oneSampleTable;
          } else if (this.testType === 'independent') {
            // 独立样本T检验使用独立样本表格
            table = this.$refs.independentTable;
          } else if (this.testType === 'paired') {
            table = this.$refs.pairedTable;
          }
          break;
        case 'variance':
          table = this.$refs.varianceTable;
          break;
        case 'independent':
          table = this.$refs.independentTable;
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

.t-test-result {
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

.normal {
  color: #67c23a;
  font-weight: bold;
}

.not-normal {
  color: #f56c6c;
  font-weight: bold;
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

h5 {
  margin: 15px 0 10px 0;
  color: #666;
}
</style>