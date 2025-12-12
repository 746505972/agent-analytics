<template>
  <div class="line-chart-result">
    <h3>折线图</h3>
    <div class="controls">
      <div class="control-group">
        <label>X轴字段:</label>
        <select v-model="xAxisColumn" @change="drawChart">
          <option v-for="col in availableColumns" :key="col" :value="col">{{ col }}</option>
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
              <label>线条颜色:</label>
              <input
                type="color"
                v-model="customColors.line"
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
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "LineChartResult",
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
        line: '#5470c6'
      },
      chartStyles: {
        showGrid: true,
        smoothLine: true,
        showArea: false
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
    },
    availableColumns() {
      // 获取所有可用列（包括数值型、分类型、日期时间型等）
      if (this.datasetDetails && this.datasetDetails.column_info) {
        return Object.keys(this.datasetDetails.column_info).filter(col => 
          ['numeric', 'categorical', 'datetime', 'ordinal'].includes(
            this.datasetDetails.column_info[col].dtype
          )
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
          // X轴可以选择任何支持的类型
          if (this.availableColumns.length >= 1) {
            this.xAxisColumn = this.availableColumns[0];
          }
          
          // Y轴优先选择数值型列
          if (this.numericColumns.length >= 1) {
            this.yAxisColumn = this.numericColumns[0];
          } else if (this.availableColumns.length >= 2) {
            this.yAxisColumn = this.availableColumns[1];
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
        
        // 根据X轴数据类型确定X轴类型
        const xColumnType = this.datasetDetails.column_info[this.xAxisColumn]?.dtype || 'category';
        const xAxisType = ['numeric', 'datetime'].includes(xColumnType) ? 'value' : 'category';
        
        // Y轴通常应该是数值型的
        const yColumnType = this.datasetDetails.column_info[this.yAxisColumn]?.dtype || 'value';
        const yAxisType = yColumnType === 'datetime' ? 'time' : 
                         yColumnType === 'numeric' ? 'value' : 'category';
        
        // 准备系列数据
        let seriesData;
        if (xAxisType === 'category') {
          seriesData = yAxisData;
        } else {
          // 对于数值型或时间型X轴，需要组合XY数据
          seriesData = data.map((row, index) => [row[this.xAxisColumn], row[this.yAxisColumn]]);
        }
        
        const option = {
          title: {
            text: '折线图',
            left: 'center',
            textStyle: {
              color: '#666',
              fontSize: 16
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              crossStyle: {
                color: '#999'
              }
            },
            snap: true,
            label: {
              show: true,
              backgroundColor: '#666'
            },
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            textStyle: {
              color: '#fff'
            },
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
            type: xAxisType,
            name: this.xAxisColumn,
            data: xAxisType === 'category' ? xAxisData : undefined,
            axisLabel: {
              color: '#666',
              rotate: 0,
              interval: 'auto'
            },
            axisLine: {
              lineStyle: {
                color: '#ccc'
              }
            },
            boundaryGap: false,
            min: 'dataMin',
            max: 'dataMax'
          },
          yAxis: {
            type: yAxisType,
            name: this.yAxisColumn,
            axisLabel: {
              color: '#666',
              formatter: yAxisType === 'value' ? '{value}' : undefined
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
            }
          },
          series: [{
            name: this.yAxisColumn,
            type: 'line',
            data: seriesData,
            smooth: this.chartStyles.smoothLine,
            areaStyle: this.chartStyles.showArea ? {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                  offset: 0,
                  color: this.colorSchemes[this.currentColorScheme][0] || this.customColors.line
                }, {
                  offset: 1,
                  color: 'rgba(255, 255, 255, 0.1)'
                }]
              }
            } : undefined,
            itemStyle: {
              color: this.colorSchemes[this.currentColorScheme][0] || this.customColors.line
            },
            lineStyle: {
              color: this.colorSchemes[this.currentColorScheme][0] || this.customColors.line,
              width: 2
            },
            symbolSize: 4,
            emphasis: {
              focus: 'series'
            }
          }],
          dataZoom: [
            {
              type: 'inside',
              xAxisIndex: [0],
              yAxisIndex: false,
              zoomOnMouseWheel: true,
              moveOnMouseMove: true
            },
            {
              type: 'slider',
              xAxisIndex: [0],
              yAxisIndex: false,
              start: 0,
              end: 100
            }
          ],
          axisPointer: {
            link: { xAxisIndex: 'all' },
            triggerTooltip: true
          }
        };
        
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
      this.colorSchemes[0][0] = this.customColors.line;
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
.line-chart-result {
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