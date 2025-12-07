<template>
  <div class="correlation-result">
    <!-- 相关性矩阵表格 -->
    <div class="table-header">
      <h4>相关性矩阵</h4>
      <button class="copy-button" @click="copyMatrix" title="复制矩阵">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>

    <div class="matrix-container">
      <table class="matrix-table">
        <thead>
          <tr>
            <th></th>
            <th v-for="col in matrixColumns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in matrixRows" :key="rowIndex">
            <th>{{ row.label }}</th>
            <td
              v-for="(cell, cellIndex) in row.values"
              :key="cellIndex"
              :class="getCellClass(cell)"
            >
              {{ cell.toFixed(3) }}
              <span v-if="shouldShowSignificance(rowIndex, cellIndex)" class="matrix-significance">
                {{ getSignificanceSymbol(rowIndex, cellIndex) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 星号含义注释 -->
    <div class="significance-note">
      <p>* p < 0.05, ** p < 0.01</p>
    </div>

    <!-- 相关性热力图 -->
    <div class="chart-container">
      <div ref="correlationChart" class="correlation-chart"></div>
    </div>
    
    <!-- 相关性表格 -->
    <div class="table-header">
      <h4>相关性系数表</h4>
      <button class="copy-button" @click="copyTable" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    
    <div class="correlation-table-container">
      <table class="correlation-table">
        <thead>
          <tr>
            <th>变量1</th>
            <th>变量2</th>
            <th>相关系数</th>
            <th>p值</th>
            <th>显著性</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in formattedCorrelationData" :key="index">
            <td>{{ item.column_x }}</td>
            <td>{{ item.column_y }}</td>
            <td>{{ item.correlation.toFixed(4) }}</td>
            <td>{{ item.p_value.toFixed(4) }}</td>
            <td>
              <span v-if="item.p_value < 0.001" class="significance strong">***</span>
              <span v-else-if="item.p_value < 0.01" class="significance strong">**</span>
              <span v-else-if="item.p_value < 0.05" class="significance weak">*</span>
              <span v-else>-</span>
            </td>
          </tr>
          <tr v-if="!formattedCorrelationData || formattedCorrelationData.length === 0">
            <td colspan="5" class="no-data">无相关性数据</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "CorrelationAnalysisResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    };
  },
  computed: {
    formattedCorrelationData() {
      if (!this.datasetDetails || !this.datasetDetails.correlation_data) {
        return [];
      }
      return this.datasetDetails.correlation_data;
    },
    
    matrixColumns() {
      if (!this.datasetDetails || !this.datasetDetails.correlation_matrix) {
        return [];
      }
      return this.datasetDetails.correlation_matrix.columns;
    },
    
    matrixRows() {
      if (!this.datasetDetails || !this.datasetDetails.correlation_matrix) {
        return [];
      }
      
      const columns = this.datasetDetails.correlation_matrix.columns;
      const correlations = this.datasetDetails.correlation_matrix.correlations;
      const pValues = this.datasetDetails.correlation_matrix.p_values;
      
      return columns.map((label, rowIndex) => {
        return {
          label,
          values: correlations[rowIndex]
        };
      });
    },
    
    pValueMatrix() {
      if (!this.datasetDetails || !this.datasetDetails.correlation_matrix) {
        return [];
      }
      return this.datasetDetails.correlation_matrix.p_values;
    }
  },
  watch: {
    datasetDetails: {
      handler() {
        this.redrawChart();
      },
      deep: true
    }
  },
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    initChart() {
      if (!this.datasetDetails || !this.matrixColumns.length) {
        return;
      }
      
      // 初始化图表
      if (!this.chart) {
        this.chart = echarts.init(this.$refs.correlationChart);
      }
      
      // 准备热力图数据
      const columns = this.matrixColumns;
      const correlations = this.datasetDetails.correlation_matrix.correlations;
      
      const data = [];
      for (let i = 0; i < columns.length; i++) {
        for (let j = 0; j < columns.length; j++) {
          data.push([j, i, correlations[i][j]]);
        }
      }
      
      const option = {
        tooltip: {
          position: 'top',
          formatter: (params) => {
            const [xIndex, yIndex, value] = params.value;
            const pValue = this.pValueMatrix[yIndex][xIndex];
            return `${columns[yIndex]} - ${columns[xIndex]}<br/>相关系数: ${value.toFixed(4)}<br/>p值: ${pValue.toFixed(4)}`;
          }
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: { 
              show: true, 
              title: '保存为图片',
              pixelRatio: 2 
            },
            restore: { 
              show: true, 
              title: '刷新' 
            }
          }
        },
        grid: {
          height: '70%',
          top: '15%'
        },
        xAxis: {
          type: 'category',
          data: columns,
          splitArea: {
            show: true
          },
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'category',
          data: columns,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: -1,
          max: 1,
          calculable: true,
          orient: 'vertical',
          right: '0',
          top: '10%',
          bottom: '10%'
        },
        series: [{
          name: '相关性',
          type: 'heatmap',
          data: data,
          xAxisIndex: 0,
          yAxisIndex: 0,
          label: {
            show: true,
            formatter: (params) => {
              return params.value[2].toFixed(2);
            }
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      };
      
      this.chart.setOption(option);
    },
    
    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    
    redrawChart() {
      if (this.chart) {
        this.chart.dispose();
        this.chart = null;
      }
      this.$nextTick(() => {
        this.initChart();
      });
    },
    
    copyTable() {
      if (!this.formattedCorrelationData.length) {
        alert('没有数据可复制');
        return;
      }
      
      let csvContent = "变量1,变量2,相关系数,p值,显著性\n";
      this.formattedCorrelationData.forEach(item => {
        const significance = item.p_value < 0.001 ? '***' : (item.p_value < 0.01 ? '**' : (item.p_value < 0.05 ? '*' : '-'));
        csvContent += `${item.column_x},${item.column_y},${item.correlation.toFixed(4)},${item.p_value.toFixed(4)},${significance}\n`;
      });
      
      this.copyToClipboard(csvContent);
    },
    
    copyMatrix() {
      if (!this.matrixColumns.length || !this.matrixRows.length) {
        alert('没有数据可复制');
        return;
      }
      
      let csvContent = "," + this.matrixColumns.join(",") + "\n";
      this.matrixRows.forEach((row, index) => {
        let rowContent = row.label;
        row.values.forEach((value, cellIndex) => {
          const significance = this.getSignificanceSymbol(index, cellIndex);
          rowContent += `,${value.toFixed(3)}${significance}`;
        });
        csvContent += rowContent + "\n";
      });
      
      this.copyToClipboard(csvContent);
    },
    
    copyToClipboard(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    },
    
    getCellClass(value) {
      if (Math.abs(value) >= 0.7) return 'strong-correlation';
      if (Math.abs(value) >= 0.3) return 'moderate-correlation';
      return 'weak-correlation';
    },
    
    shouldShowSignificance(rowIndex, cellIndex) {
      // 不在对角线上且p值小于显著性水平
      return rowIndex !== cellIndex && this.pValueMatrix[rowIndex] && 
             this.pValueMatrix[rowIndex][cellIndex] < 0.05;
    },
    
    getSignificanceSymbol(rowIndex, cellIndex) {
      if (!this.pValueMatrix[rowIndex]) return '';
      
      const pValue = this.pValueMatrix[rowIndex][cellIndex];
      if (pValue < 0.001) return '***';
      if (pValue < 0.01) return '**';
      if (pValue < 0.05) return '*';
      return '';
    }
  }
}
</script>

<style scoped>
.correlation-result {
  padding: 20px;
}

.correlation-result h3 {
  margin-top: 0;
  color: #303133;
}

.correlation-result h4 {
  margin: 20px 0 10px 0;
}

.chart-container {
  margin-bottom: 30px;
}

.correlation-chart {
  width: 100%;
  height: 400px;
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
}

.copy-button:hover {
  background-color: #f5f5f5;
}

.copy-button img {
  width: 16px;
  height: 16px;
}

.correlation-table-container,
.matrix-container {
  overflow-x: auto;
  margin-bottom: 30px;
}

.correlation-table,
.matrix-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  border-top: 1px solid #333;
  border-bottom: 1px solid #333;
}

.correlation-table th,
.correlation-table td,
.matrix-table th,
.matrix-table td {
  padding: 8px;
  text-align: center;
  white-space: nowrap;
}

.correlation-table th,
.matrix-table th {
  font-weight: bold;
  border-bottom: 1px solid #333;
  background-color: transparent;
}

.correlation-table td,
.matrix-table td {
  border: none;
}

.correlation-table tbody tr:last-child td,
.matrix-table tbody tr:last-child td {
  border-bottom: none;
}

.no-data {
  text-align: center;
  color: #909399;
  font-style: italic;
}

.significance.strong {
  color: #e74c3c;
  font-weight: bold;
}

.significance.weak {
  color: #f39c12;
  font-weight: bold;
}

.matrix-significance {
  color: #e74c3c;
  font-weight: bold;
}

.strong-correlation {
  background-color: #fef0f0;
}

.moderate-correlation {
  background-color: #fdf6ec;
}

.weak-correlation {
  background-color: #f0f9eb;
}

.significance-note {
  margin-top: 5px;
  font-size: 14px;
  color: #666;
}
</style>