<template>
  <div class="correlation-result">
    <!-- 相关性矩阵表格 -->
    <div class="table-header">
      <h4>相关性矩阵</h4>
      <button class="copy-button" @click="copyMatrix" title="复制矩阵">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    
    <!-- 配色方案选择弹窗 -->
    <div v-if="showColorSchemeModal" class="modal-overlay" @click="showColorSchemeModal = false">
      <div class="color-scheme-modal" @click.stop>
        <div class="modal-header">
          <h3>选择配色方案</h3>
          <button class="close-button" @click="showColorSchemeModal = false">×</button>
        </div>
        <div class="color-schemes">
          <div 
            v-for="(scheme, key) in colorSchemes" 
            :key="key" 
            class="color-scheme-option" 
            :class="{ active: colorScheme === key }"
            @click="selectColorScheme(key)"
          >
            <div class="color-preview">
              <div 
                v-for="color in scheme.colors" 
                :key="color" 
                class="color-item" 
                :style="{ backgroundColor: color }"
              ></div>
            </div>
            <div class="scheme-name">{{ scheme.name }}</div>
          </div>
          
          <!-- 自定义配色选项 -->
          <div 
            class="color-scheme-option custom-option" 
            :class="{ active: colorScheme === 'custom' }"
            @click="openCustomColorModal"
          >
            <div class="color-preview">
              <div 
                v-for="color in customColors" 
                :key="color" 
                class="color-item" 
                :style="{ backgroundColor: color }"
              ></div>
            </div>
            <div class="scheme-name">自定义</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 自定义配色弹窗 -->
    <div v-if="showCustomColorModal" class="modal-overlay" @click="showCustomColorModal = false">
      <div class="custom-color-modal" @click.stop>
        <div class="modal-header">
          <h3>自定义配色方案</h3>
          <button class="close-button" @click="showCustomColorModal = false">×</button>
        </div>
        <div class="custom-color-content">
          <div class="color-preview-large">
            <div 
              v-for="(color, index) in customColors" 
              :key="index" 
              class="color-item-large" 
              :style="{ backgroundColor: color }"
            >
              <div class="color-value">{{ color }}</div>
            </div>
          </div>
          <div class="color-inputs">
            <div 
              v-for="(color, index) in customColors" 
              :key="index" 
              class="color-input-item"
            >
              <label>颜色 {{ index + 1 }}:</label>
              <input 
                type="color" 
                :value="color" 
                @input="updateCustomColor(index, $event.target.value)"
              />
              <input 
                type="text" 
                :value="color" 
                @input="updateCustomColor(index, $event.target.value)"
                class="color-text-input"
              />
            </div>
          </div>
          <div class="modal-actions">
            <button class="apply-button" @click="applyCustomColors">应用配色</button>
            <button class="cancel-button" @click="showCustomColorModal = false">取消</button>
          </div>
        </div>
      </div>
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
      chart: null,
      colorScheme: 'default',
      showColorSchemeModal: false,
      showCustomColorModal: false,
      customColors: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'],
      colorSchemes: {
        default: {
          name: '默认',
          colors: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        },
        blue: {
          name: '蓝色',
          colors: ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']
        },
        green: {
          name: '绿色',
          colors: ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b']
        },
        red: {
          name: '红色',
          colors: ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d']
        }
      }
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
    },
    colorScheme: {
      handler() {
        this.updateChartColorScheme();
      }
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
              title: '重置' 
            },
            myColorScheme: {
              show: true,
              title: '切换配色',
              icon: 'path://M12,2C13.1,2 14,2.9 14,4C14,5.1 13.1,6 12,6C10.9,6 10,5.1 10,4C10,2.9 10.9,2 12,2M21,9V7L15,1H5C3.89,1 3,1.89 3,3V21A2,2 0 0,0 5,23H19A2,2 0 0,0 21,21V9M19,9H14V4H19V9Z',
              onclick: () => {
                this.showColorSchemeModal = true;
              }
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
          bottom: '10%',
          inRange: {
            color: this.colorScheme === 'custom' ? this.customColors : this.colorSchemes[this.colorScheme].colors
          }
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
    
    selectColorScheme(schemeKey) {
      this.colorScheme = schemeKey;
      this.showColorSchemeModal = false;
      this.updateChartColorScheme();
    },
    
    openCustomColorModal() {
      this.showColorSchemeModal = false;
      this.showCustomColorModal = true;
    },
    
    updateCustomColor(index, colorValue) {
      // 验证颜色值是否有效
      const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
      if (hexRegex.test(colorValue) || colorValue.startsWith('#')) {
        this.customColors[index] = colorValue;
      } else if (!colorValue.startsWith('#') && colorValue.length <= 6) {
        // 自动补全 # 符号
        const fullColorValue = '#' + colorValue;
        if (hexRegex.test(fullColorValue)) {
          this.customColors[index] = fullColorValue;
        }
      }
    },
    
    applyCustomColors() {
      this.colorScheme = 'custom';
      this.showCustomColorModal = false;
      this.updateChartColorScheme();
    },
    
    updateChartColorScheme() {
      if (this.chart) {
        let colors;
        if (this.colorScheme === 'custom') {
          colors = this.customColors;
        } else {
          colors = this.colorSchemes[this.colorScheme].colors;
        }
        
        const option = {
          visualMap: {
            inRange: {
              color: colors
            }
          }
        };
        this.chart.setOption(option);
      }
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.color-scheme-modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 15px;
  width: 450px;
  max-width: 90%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: #333;
}

.color-schemes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}

.color-scheme-option {
  border: 2px solid #eee;
  border-radius: 6px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.color-scheme-option:hover {
  border-color: #409eff;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.color-scheme-option.active {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.color-preview {
  display: flex;
  height: 30px;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.color-item {
  flex: 1;
}

.scheme-name {
  text-align: center;
  font-size: 14px;
  color: #333;
}

.custom-color-modal {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 20px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.custom-color-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-height: calc(80vh - 100px);
  overflow-y: auto;
}

.color-preview-large {
  display: flex;
  height: 60px;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.color-item-large {
  flex: 1;
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 4px;
}

.color-value {
  background: rgba(255, 255, 255, 0.8);
  font-size: 10px;
  padding: 2px 4px;
  border-radius: 2px;
  color: #333;
}

.color-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
}

.color-input-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.color-input-item label {
  font-size: 14px;
  color: #333;
}

.color-input-item input[type="color"] {
  width: 100%;
  height: 40px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
}

.color-input-item input[type="text"] {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-family: monospace;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 10px;
}

.apply-button {
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.apply-button:hover {
  background-color: #337ecc;
}

.cancel-button {
  padding: 8px 16px;
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-button:hover {
  background-color: #ebebeb;
}
</style>