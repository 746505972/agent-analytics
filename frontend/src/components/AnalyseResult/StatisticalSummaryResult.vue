<template>
  <div class="statistical-summary-details">
    <div class="table-header">
      <h3>统计摘要</h3>
      <button class="copy-button" @click="copyTable('upper')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <!-- 上部分表格：样本量 最小值 最大值 平均值 标准差 中位数 -->
    <div class="stats-summary-container">
      <table class="stats-summary-table upper-table">
        <thead>
          <tr>
            <th>列名</th>
            <th>样本量</th>
            <th>最小值</th>
            <th>最大值</th>
            <th>平均值</th>
            <th>标准差</th>
            <th>中位数</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in datasetDetails.summary" :key="item.column">
            <td>{{ item.column }}</td>
            <td>{{ item.count }}</td>
            <td>{{ item.min !== null ? item.min : 'N/A' }}</td>
            <td>{{ item.max !== null ? item.max : 'N/A' }}</td>
            <td>{{ item.mean !== null ? item.mean : 'N/A' }}</td>
            <td>{{ item.std_dev !== null ? item.std_dev : 'N/A' }}</td>
            <td>{{ item.median !== null ? item.median : 'N/A' }}</td>
          </tr>
          <tr v-if="!datasetDetails.summary || datasetDetails.summary.length === 0">
            <td colspan="7" class="no-data">无统计数据</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 图表类型选择工具栏 -->
    <div class="chart-toolbar">
      <span class="toolbar-label">图表类型:</span>
      <button 
        v-for="chartType in chartTypes" 
        :key="chartType.value"
        :class="{ active: currentChartType === chartType.value }"
        @click="switchChartType(chartType.value)"
        class="chart-type-button"
      >
        {{ chartType.label }}
      </button>
      <!-- 图表配置按钮 -->
      <button 
        class="chart-type-button"
        @click="showConfigPopup = true"
      >
        图表配置
      </button>
    </div>
    
    <!-- 图表配置浮窗 -->
    <div v-if="showConfigPopup" class="config-popup-overlay" @click.self="showConfigPopup = false">
      <div class="config-popup">
        <div class="popup-header">
          <span>图表配置</span>
          <button class="close-btn" @click="showConfigPopup = false">×</button>
        </div>
        <div class="popup-content">
          <div class="config-section">
            <h4>配色方案</h4>
            <div class="color-options">
              <div
                v-for="(colorScheme, index) in colorSchemes"
                :key="index"
                :class="['color-scheme-option', { active: currentColorScheme === index }]"
                @click="selectColorScheme(index)"
              >
                <div class="color-preview">
                  <div
                    v-for="(color, idx) in colorScheme"
                    :key="idx"
                    class="color-item"
                    :style="{ backgroundColor: color }"
                  ></div>
                </div>
                <span>{{ getColorSchemeName(index) }}</span>
              </div>
            </div>
          </div>

          <div class="config-section">
            <h4>自定义颜色</h4>
            <div class="custom-color-picker">
              <label>主色调:</label>
              <input
                type="color"
                v-model="customColors.primary"
                @change="applyCustomColors"
              />
            </div>
          </div>

          <div class="config-section">
            <h4>样式设置</h4>
            <div class="style-options">
              <div class="style-option">
                <label>
                  <input
                    type="checkbox"
                    v-model="chartStyles.showGrid"
                    @change="applyStyleChanges"
                  />
                  显示网格线
                </label>
              </div>
              <div class="style-option">
                <label>
                  <input
                    type="checkbox"
                    v-model="chartStyles.smoothLine"
                    @change="applyStyleChanges"
                  />
                  平滑曲线
                </label>
              </div>
              <div class="style-option">
                <label>
                  <input
                    type="checkbox"
                    v-model="chartStyles.showArea"
                    @change="applyStyleChanges"
                  />
                  显示填充区域
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 中间部分：ECharts图表 -->
    <div ref="statisticalChart" class="statistical-chart"></div>
    
    <!-- 下部分表格标题和按钮 -->
    <div class="table-header">
      <h3>更多统计信息</h3>
      <button class="copy-button" @click="copyTable('lower')" title="复制表格">
        <img src="@/assets/images/copy.svg" alt="复制" />
      </button>
    </div>
    <!-- 下部分表格：剩余统计数据 -->
    <div class="stats-summary-container">
      <table class="stats-summary-table lower-table">
        <thead>
          <tr>
            <th>列名</th>
            <th>方差</th>
            <th>第一四分位数</th>
            <th>第三四分位数</th>
            <th>峰度</th>
            <th>偏度</th>
            <th>极差</th>
            <th>四分位距</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in datasetDetails.summary" :key="item.column">
            <td>{{ item.column }}</td>
            <td>{{ item.variance !== null ? item.variance : 'N/A' }}</td>
            <td>{{ item.q1 !== null ? item.q1 : 'N/A' }}</td>
            <td>{{ item.q3 !== null ? item.q3 : 'N/A' }}</td>
            <td>{{ item.kurtosis !== null ? item.kurtosis : 'N/A' }}</td>
            <td>{{ item.skewness !== null ? item.skewness : 'N/A' }}</td>
            <td>{{ item.range !== null ? item.range : 'N/A' }}</td>
            <td>{{ item.iqr !== null ? item.iqr : 'N/A' }}</td>
          </tr>
          <tr v-if="!datasetDetails.summary || datasetDetails.summary.length === 0">
            <td colspan="8" class="no-data">无统计数据</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "StatisticalSummaryResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null,
      currentChartType: 'line', // 默认图表类型为折线图
      chartTypes: [
        { label: '折线图', value: 'line' },
        { label: '柱状图', value: 'bar' },
        { label: '条形图', value: 'barHorizontal' },
        { label: '雷达图', value: 'radar' }
      ],
      showConfigPopup: false, // 是否显示配置浮窗
      currentColorScheme: 0, // 当前使用的配色方案索引
      colorSchemes: [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
      ],
      customColors: {
        primary: '#5470c6'
      },
      chartStyles: {
        showGrid: true,
        smoothLine: false,
        showArea: false
      }
    };
  },
  watch: {
    datasetDetails: {
      handler() {
        this.$nextTick(() => {
          this.initStatisticalChart();
        });
      },
      deep: true,
      immediate: true
    },
    currentChartType: {
      handler() {
        this.$nextTick(() => {
          this.initStatisticalChart();
        });
      }
    }
  },
  methods: {
    // 复制表格数据到剪贴板
    copyTable(tableType) {
      let table;
      if (tableType === 'upper') {
        table = document.querySelector('.upper-table');
      } else {
        table = document.querySelector('.lower-table');
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
          this.$message && this.$message.success('表格数据已复制到剪贴板');
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
    
    // 显示复制通知（复用 ChatAssistant.vue 的样式）
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

    switchChartType(chartType) {
      this.currentChartType = chartType;
    },
    
    toggleConfigPanel() {
      this.isConfigPanelOpen = !this.isConfigPanelOpen;
    },
    
    selectColorScheme(index) {
      this.currentColorScheme = index;
    },
    
    getColorSchemeName(index) {
      const names = ['默认', '深色', '明亮', '柔和'];
      return names[index] || `方案${index + 1}`;
    },
    
    applyCustomColors() {
      // 使用自定义颜色更新配色方案
      this.colorSchemes[0][0] = this.customColors.primary;
      this.currentColorScheme = 0; // 切换到自定义配色方案
    },
    
    applyStyleChanges() {
      this.$nextTick(() => {
        this.initStatisticalChart();
      });
    },
    
    initStatisticalChart() {
      // 销毁之前的图表实例
      if (this.chart) {
        this.chart.dispose();
      }
      
      // 初始化图表
      this.chart = echarts.init(this.$refs.statisticalChart);
      
      // 为图表容器添加 passive 事件监听器以避免性能警告
      const chartContainer = this.$refs.statisticalChart;
      if (chartContainer) {
        // 移除已有的 wheel 事件监听器（如果存在）
        chartContainer.removeEventListener('wheel', this.handleWheel, { passive: false });
        // 添加 passive wheel 事件监听器
        chartContainer.addEventListener('wheel', this.handleWheel, { passive: true });
      }
      
      // 根据选中的图表类型生成不同的配置
      let option;
      switch (this.currentChartType) {
        case 'line':
          option = this.getLineChartOption();
          break;
        case 'bar':
          option = this.getBarChartOption();
          break;
        case 'barHorizontal':
          option = this.getHorizontalBarChartOption();
          break;
        case 'radar':
          option = this.getRadarChartOption();
          break;
        default:
          option = this.getLineChartOption();
      }
      
      // 应用配色方案
      option.color = this.colorSchemes[this.currentColorScheme];
      
      // 渲染图表
      this.chart.setOption(option);
      
      // 监听窗口大小变化，自适应调整图表大小
      window.addEventListener('resize', this.handleResize);
    },
    
    getLineChartOption() {
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: false
            },
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            restore: {},
            saveAsImage: {}
          }
        },
        legend: {
          data: ['平均值']
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.datasetDetails.summary.map(item => item.column),
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '平均值'
        },
        series: [
          {
            name: '平均值',
            type: 'line',
            data: this.datasetDetails.summary.map(item => item.mean),
            smooth: this.chartStyles.smoothLine,
            emphasis: {
              focus: 'series'
            }
          }
        ]
      };
      
      // 如果需要显示填充区域
      if (this.chartStyles.showArea) {
        option.series[0].areaStyle = {};
      }
      
      // 如果不显示网格线
      if (!this.chartStyles.showGrid) {
        option.xAxis.splitLine = { show: false };
        option.yAxis.splitLine = { show: false };
      }
      
      return option;
    },
    
    getBarChartOption() {
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: false
            },
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            restore: {},
            saveAsImage: {}
          }
        },
        legend: {
          data: ['平均值']
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: this.datasetDetails.summary.map(item => item.column),
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '平均值'
        },
        series: [
          {
            name: '平均值',
            type: 'bar',
            data: this.datasetDetails.summary.map(item => item.mean),
            emphasis: {
              focus: 'series'
            }
          }
        ]
      };
      
      // 如果不显示网格线
      if (!this.chartStyles.showGrid) {
        option.xAxis.splitLine = { show: false };
        option.yAxis.splitLine = { show: false };
      }
      
      return option;
    },
    
    getHorizontalBarChartOption() {
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: false
            },
            dataView: { readOnly: false },
            magicType: { type: ['line', 'bar'] },
            restore: {},
            saveAsImage: {}
          }
        },
        legend: {
          data: ['平均值']
        },
        grid: {
          left: '15%',
          right: '10%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '平均值'
        },
        yAxis: {
          type: 'category',
          data: this.datasetDetails.summary.map(item => item.column)
        },
        series: [
          {
            name: '平均值',
            type: 'bar',
            data: this.datasetDetails.summary.map(item => item.mean),
            emphasis: {
              focus: 'series'
            }
          }
        ]
      };
      
      // 如果不显示网格线
      if (!this.chartStyles.showGrid) {
        option.xAxis.splitLine = { show: false };
        option.yAxis.splitLine = { show: false };
      }
      
      return option;
    },
    
    getRadarChartOption() {
      // 雷达图需要特殊的配置
      const columns = this.datasetDetails.summary.map(item => item.column);
      const meanValues = this.datasetDetails.summary.map(item => item.mean);
      
      return {
        tooltip: {},
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        legend: {
          data: ['平均值']
        },
        radar: {
          indicator: columns.map((column, index) => {
            // 确保 meanValues 不为空且包含有效数值
            if (!meanValues || meanValues.length === 0) {
              return {
                name: column,
                max: 100
              };
            }
            
            // 过滤掉无效值（null, undefined, NaN）
            const validMeanValues = meanValues.filter(val => 
              val !== null && val !== undefined && !isNaN(val));
              
            if (validMeanValues.length === 0) {
              return {
                name: column,
                max: 100
              };
            }
            
            // 计算最大值并增加一些边距，同时确保数值合理以避免刻度不可读
            const maxValue = Math.max(...validMeanValues) * 1.2;
            
            // 如果最大值为0，设置一个默认最大值
            if (maxValue === 0) {
              return {
                name: column,
                max: 100
              };
            }
            
            // 对于非常大的数值，使用适当的缩放以提高可读性
            let formattedMax = maxValue;
            if (maxValue > 1000000000) { // 大于10亿
              formattedMax = Math.ceil(maxValue / 100000000) * 100000000;
            } else if (maxValue > 1000000) { // 大于1百万
              formattedMax = Math.ceil(maxValue / 100000) * 100000;
            } else if (maxValue > 1000) { // 大于1千
              formattedMax = Math.ceil(maxValue / 100) * 100;
            } else {
              // 对较小的数值保留适当的小数位数
              formattedMax = parseFloat(maxValue.toFixed(2));
            }
            
            return {
              name: column,
              max: formattedMax
            };
          }),
          // 添加轴线和分割线配置以改善可读性
          axisLine: {
            lineStyle: {
              color: '#999'
            }
          },
          splitLine: {
            lineStyle: {
              color: '#ddd'
            }
          },
          splitArea: {
            show: false
          }
        },
        series: [{
          name: '平均值',
          type: 'radar',
          data: [
            {
              value: meanValues,
              name: '平均值'
            }
          ],
          // 添加雷达图线条和区域样式
          lineStyle: {
            width: 2
          },
          symbol: 'circle',
          symbolSize: 4,
          itemStyle: {
            borderRadius: 2
          }
        }]
      };
    },
    
    handleResize() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    
    // 处理滚轮事件，用于避免 passive 事件监听器警告
    handleWheel(event) {
      // 这里不需要特殊处理，只需要确保事件监听器是 passive 的
      // ECharts 会处理实际的滚轮交互
    }
  },
  
  beforeUnmount() {
    // 组件销毁前清理图表实例和事件监听器
    if (this.chart) {
      this.chart.dispose();
    }
    window.removeEventListener('resize', this.handleResize);
    
    // 移除 passive 事件监听器
    const chartContainer = this.$refs.statisticalChart;
    if (chartContainer) {
      chartContainer.removeEventListener('wheel', this.handleWheel, { passive: true });
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
}

.copy-button:hover {
  background-color: #f5f5f5;
}

.copy-button img {
  width: 16px;
  height: 16px;
}

.statistical-chart {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
}

.stats-summary-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.stats-summary-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.stats-summary-table th,
.stats-summary-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  white-space: nowrap;
}

.stats-summary-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.no-data {
  text-align: center;
  color: #909399;
  font-style: italic;
}

.chart-toolbar {
  margin: 15px 0;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.toolbar-label {
  font-weight: bold;
  color: #606266;
}

.chart-type-button {
  padding: 8px 16px;
  background-color: #f4f4f5;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
  height: 32px; /* 与其它按钮保持一致的高度 */
  box-sizing: border-box;
}

.chart-type-button:hover {
  background-color: #e9e9eb;
}

.chart-type-button.active {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

/* 图表配置浮窗样式 */
.config-popup-overlay {
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

.config-popup {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 500px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.popup-header {
  padding: 12px 15px;
  background-color: #f5f7fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #606266;
  border-bottom: 1px solid #dcdfe6;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.close-btn:hover {
  color: #606266;
}

.popup-content {
  padding: 15px;
  overflow-y: auto;
}

.config-section {
  margin-bottom: 20px;
}

.config-section:last-child {
  margin-bottom: 0;
}

.config-section h4 {
  margin: 0 0 10px 0;
  color: #606266;
  font-size: 14px;
}

.color-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.color-scheme-option {
  cursor: pointer;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 8px;
  width: 100px;
  text-align: center;
  transition: all 0.3s;
}

.color-scheme-option:hover,
.color-scheme-option.active {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.color-preview {
  display: flex;
  height: 20px;
  margin-bottom: 5px;
  border-radius: 2px;
  overflow: hidden;
}

.color-item {
  flex: 1;
}

.custom-color-picker {
  display: flex;
  align-items: center;
  gap: 10px;
}

.custom-color-picker label {
  font-size: 14px;
  color: #606266;
}

.style-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.style-option label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
}

@media (max-width: 768px) {
  .chart-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chart-type-button {
    width: 100%;
    text-align: center;
  }
  
  .color-options {
    justify-content: center;
  }
  
  .color-scheme-option {
    width: 80px;
  }
}
</style>