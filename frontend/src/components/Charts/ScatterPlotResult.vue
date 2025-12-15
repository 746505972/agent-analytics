<template>
  <div class="controls">
    <div class="control-group">
      <label>X轴字段:</label>
      <select v-model="xAxisColumn" @change="drawChart">
        <option v-for="col in numericColumns" :key="col" :value="col">{{ col }}</option>
      </select>
    </div>
    <div class="control-group">
      <label>Y轴字段:</label>
      <select v-model="yAxisColumn" @change="drawChart">
        <option v-for="col in numericColumns" :key="col" :value="col">{{ col }}</option>
      </select>
    </div>
    <!-- 图表配置按钮 -->
    <div class="control-group">
      <button class="config-button" @click="showConfigPopup = true">
        图表配置
      </button>
    </div>
  </div>
  <div class="chart-container">
    <div ref="chart" class="chart"></div>
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
                  v-for="(color, idx) in colorScheme.slice(0, 3)"
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
            <label>散点颜色:</label>
            <input
              type="color"
              v-model="customColors.scatter"
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
                  v-model="chartStyles.showRegressionLine"
                  @change="applyStyleChanges"
                />
                显示回归线
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "ScatterPlotResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null,
      xAxisColumn: '',
      yAxisColumn: '',
      loading: false,
      showConfigPopup: false,
      currentColorScheme: 0,
      colorSchemes: [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
      ],
      customColors: {
        scatter: '#5470c6'
      },
      chartStyles: {
        showGrid: true,
        showRegressionLine: false
      },
      resizeObserver: null
    };
  },
  computed: {
    numericColumns() {
      // 从数据集中提取数值型列
      if (this.datasetDetails && this.datasetDetails.column_info) {
        return Object.keys(this.datasetDetails.column_info).filter(col => 
          this.datasetDetails.column_info[col].dtype === 'numeric'
        );
      }
      return [];
    }
  },
  watch: {
    datasetDetails: {
      handler(newVal) {
        if (newVal && newVal.data && newVal.data.length > 0) {
          this.initChart();
        }
      },
      deep: true,
      immediate: true
    },
    xAxisColumn() {
      this.drawChart();
    },
    yAxisColumn() {
      this.drawChart();
    }
  },
  methods: {
    initChart() {
      // 确保DOM已经更新
      this.$nextTick(() => {
        if (!this.$refs.chart) {
          console.warn('Chart container not found');
          return;
        }

        // 如果已有图表实例，先销毁
        if (this.chart) {
          this.chart.dispose();
          this.chart = null;
        }

        // 初始化ECharts实例
        this.chart = echarts.init(this.$refs.chart);
        
        // 添加resize监听
        this.setupResizeObserver();

        // 设置默认字段
        if (!this.xAxisColumn && !this.yAxisColumn) {
          // 散点图需要两个数值型字段
          if (this.numericColumns.length >= 2) {
            this.xAxisColumn = this.numericColumns[0];
            this.yAxisColumn = this.numericColumns[1];
          } else if (this.numericColumns.length >= 1) {
            this.xAxisColumn = this.numericColumns[0];
            this.yAxisColumn = this.numericColumns[0];
          }
        }

        this.$nextTick(() => {
          this.drawChart();
        });
      });
    },
    
    setupResizeObserver() {
      // 清除之前的监听器
      if (this.resizeObserver) {
        this.resizeObserver.disconnect();
      }
      
      // 创建新的ResizeObserver
      this.resizeObserver = new ResizeObserver(() => {
        if (this.chart) {
          this.chart.resize();
        }
      });
      
      // 监听图表容器变化
      if (this.$refs.chart) {
        this.resizeObserver.observe(this.$refs.chart);
      }
    },
    
    calculateLinearRegression(seriesData) {
      if (!seriesData || seriesData.length < 2) {
        return null;
      }
      
      // 计算回归线的系数
      let n = seriesData.length;
      let sumX = 0;
      let sumY = 0;
      let sumXY = 0;
      let sumXX = 0;
      
      for (let i = 0; i < n; i++) {
        let x = seriesData[i][0];
        let y = seriesData[i][1];
        sumX += x;
        sumY += y;
        sumXY += x * y;
        sumXX += x * x;
      }
      
      // 计算斜率和截距
      let slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
      let intercept = (sumY - slope * sumX) / n;
      
      // 返回回归函数
      return function(x) {
        return slope * x + intercept;
      };
    },
    
    drawChart() {
      // 检查必要条件是否满足
      if (!this.chart || !this.xAxisColumn || !this.yAxisColumn || 
          !this.datasetDetails || !this.datasetDetails.data || this.datasetDetails.data.length === 0) {
        return;
      }
      
      try {
        // 直接从传入的数据中提取数据
        const data = this.datasetDetails.data;
        
        // 提取X轴和Y轴数据
        const xAxisData = data.map(row => row[this.xAxisColumn]);
        const yAxisData = data.map(row => row[this.yAxisColumn]);
        
        // 准备系列数据
        const seriesData = data.map((row, index) => [row[this.xAxisColumn], row[this.yAxisColumn]]);
        
        const option = {
          title: {
            text: '散点图',
            left: 'center',
            textStyle: {
              color: '#666',
              fontSize: 16
            }
          },
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'cross'
            },
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            textStyle: {
              color: '#fff'
            },
            formatter: (params) => {
              return `${this.xAxisColumn}: ${params.data[0]}<br/>${this.yAxisColumn}: ${params.data[1]}`;
            }
          },
          toolbox: {
            show: true,
            feature: {
              dataView: { readOnly: false },
              restore: {},
              saveAsImage: {}
            }
          },
          grid: {
            top: '20%',
            bottom: '15%',
            left: '10%',
            right: '10%',
            containLabel: true
          },
          xAxis: {
            type: 'value',
            name: this.xAxisColumn,
            axisLabel: {
              color: '#666'
            },
            axisLine: {
              lineStyle: {
                color: '#ccc'
              }
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            },
            min: 'dataMin',
            max: 'dataMax'
          },
          yAxis: {
            type: 'value',
            name: this.yAxisColumn,
            axisLabel: {
              color: '#666'
            },
            axisLine: {
              lineStyle: {
                color: '#ccc'
              }
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            },
            min: 'dataMin',
            max: 'dataMax'
          },
          series: [{
            name: '散点',
            type: 'scatter',
            data: seriesData,
            itemStyle: {
              color: this.colorSchemes[this.currentColorScheme][0] || this.customColors.scatter
            },
            symbolSize: 8,
            emphasis: {
              focus: 'series'
            }
          }],
          dataZoom: [
            {
              type: 'inside',
              xAxisIndex: [0],
              yAxisIndex: [0],
              zoomOnMouseWheel: true,
              moveOnMouseMove: true
            },
            {
              type: 'slider',
              xAxisIndex: [0],
              yAxisIndex: [0],
              start: 0,
              end: 100
            }
          ]
        };
        
        // 如果需要显示回归线
        if (this.chartStyles.showRegressionLine) {
          // 计算回归线
          const regressionFunc = this.calculateLinearRegression(seriesData);
          
          if (regressionFunc) {
            // 生成回归线数据点
            const minX = Math.min(...xAxisData);
            const maxX = Math.max(...xAxisData);
            const regressionPoints = [
              [minX, regressionFunc(minX)],
              [maxX, regressionFunc(maxX)]
            ];
            
            option.series.push({
              name: '回归线',
              type: 'line',
              data: regressionPoints,
              smooth: false,
              symbol: 'none',
              lineStyle: {
                color: this.colorSchemes[this.currentColorScheme][1] || '#ff7f0e',
                width: 2,
                type: 'solid'
              },
              emphasis: {
                focus: 'series'
              }
            });
          }
        }
        
        // 如果不显示网格线
        if (!this.chartStyles.showGrid) {
          option.xAxis.splitLine = { show: false };
          option.yAxis.splitLine = { show: false };
        }

        // 先清空图表再重新设置选项，确保坐标系正确初始化
        this.chart.clear();
        this.chart.setOption(option, true);

      } catch (error) {
        console.error('绘制图表失败:', error);
      }
    },
    
    selectColorScheme(index) {
      this.currentColorScheme = index;
      this.$nextTick(() => {
        this.drawChart();
      });
    },
    
    getColorSchemeName(index) {
      const names = ['默认', '深色', '明亮', '柔和'];
      return names[index] || `方案${index + 1}`;
    },
    
    applyCustomColors() {
      // 使用自定义颜色更新配色方案
      this.colorSchemes[0][0] = this.customColors.scatter;
      this.currentColorScheme = 0; // 切换到自定义配色方案
      this.drawChart();
    },
    
    applyStyleChanges() {
      this.drawChart();
    }
  },
  
  mounted() {
    this.initChart();
  },
  
  beforeUnmount() {
    // 组件销毁前清理资源
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = null;
    }
    
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
  }
};
</script>

<style scoped>
.scatter-plot-result {
  padding: 20px;
}

.chart-container {
  width: 100%;
  height: 500px;
  margin-bottom: 20px;
}

.chart {
  width: 100%;
  height: 100%;
}

.controls {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-group label {
  font-weight: bold;
}

.control-group select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

.config-button {
  padding: 6px 12px;
  background-color: #f4f4f5;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
}

.config-button:hover {
  background-color: #e9e9eb;
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
  .controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .control-group {
    width: 100%;
  }
  
  .color-options {
    justify-content: center;
  }
  
  .color-scheme-option {
    width: 80px;
  }
}
</style>