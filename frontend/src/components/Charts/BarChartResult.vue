<template>
  <div class="controls">
    <div class="control-group">
      <label>X轴字段:</label>
      <select v-model="xAxisColumn" @change="onConfigChange">
        <option v-for="col in availableColumns" :key="col" :value="col">{{ col }}</option>
      </select>
    </div>
    <div class="control-group">
      <label>Y轴字段:</label>
      <select v-model="yAxisColumn" @change="onConfigChange">
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
    <div v-if="!chartPath && !useBackendRendering" class="no-chart">
      <p>请配置图表参数以生成图表</p>
    </div>
    <iframe 
      v-else-if="chartPath" 
      :src="chartPath" 
      width="100%" 
      height="100%" 
      frameborder="0" 
      @load="onChartLoaded"
    ></iframe>
    <div v-else-if="useBackendRendering && loading" class="loading">
      <p>正在生成图表...</p>
    </div>
    <div v-else ref="chart" class="chart"></div>
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
          <h4>图表标题</h4>
          <div class="title-input">
            <input
              type="text"
              v-model="chartTitle"
              @input="onTitleChange"
              placeholder="请输入图表标题"
            />
          </div>
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
            <label>柱体颜色:</label>
            <input
              type="color"
              v-model="customColors.bar"
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
                  v-model="chartStyles.horizontal"
                  @change="applyStyleChanges"
                />
                横向柱状图
              </label>
            </div>
          </div>
        </div>
        
        <div class="config-section">
          <h4>渲染模式</h4>
          <div class="render-mode-options">
            <div class="style-option">
              <label>
                <input
                  type="radio"
                  v-model="renderMode"
                  value="frontend"
                  @change="switchRenderMode"
                />
                前端渲染
              </label>
            </div>
            <div class="style-option">
              <label>
                <input
                  type="radio"
                  v-model="renderMode"
                  value="backend"
                  @change="switchRenderMode"
                />
                后端渲染
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
  name: "BarChartResult",
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
      chartPath: null,
      useBackendRendering: false,
      loading: false,
      showConfigPopup: false,
      currentColorScheme: 0,
      chartTitle: '柱状图',
      colorSchemes: [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
      ],
      customColors: {
        bar: '#5470c6'
      },
      chartStyles: {
        showGrid: true,
        horizontal: false
      },
      renderMode: 'frontend', // 'frontend' 或 'backend'
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
      this.onConfigChange();
    },
    yAxisColumn() {
      this.onConfigChange();
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
          if (this.renderMode === 'frontend') {
            this.drawChart();
          } else {
            this.generateBackendChart();
          }
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
    
    onConfigChange() {
      // 当配置改变时，发送事件到父组件
      this.$emit('chart-config-updated', this.getChartConfig());
      
      // 根据渲染模式决定如何处理
      if (this.renderMode === 'frontend') {
        this.drawChart();
      } else {
        this.generateBackendChart();
      }
    },
    
    getChartConfig() {
      // 返回当前图表配置
      return {
        data_id: this.datasetDetails.data_id || 'default',
        x_axis_column: this.xAxisColumn,
        y_axis_column: this.yAxisColumn,
        chart_title: this.chartTitle,
        chart_styles: this.chartStyles,
        color_scheme: this.currentColorScheme,
        custom_colors: this.customColors,
        chart_type: 'bar',
        render_mode: this.renderMode
      };
    },
    
    selectColorScheme(index) {
      this.currentColorScheme = index;
      this.onConfigChange();
    },
    
    getColorSchemeName(index) {
      const names = ['默认', '深色', '明亮', '柔和'];
      return names[index] || `方案${index + 1}`;
    },
    
    applyCustomColors() {
      // 使用自定义颜色更新配色方案
      this.colorSchemes[0][0] = this.customColors.bar;
      this.currentColorScheme = 0; // 切换到自定义配色方案
      this.onConfigChange();
    },
    
    applyStyleChanges() {
      this.onConfigChange();
    },

    onTitleChange() {
      this.onConfigChange();
    },
    
    onChartLoaded() {
      // 图表加载完成后的回调
      console.log('图表加载完成');
    },
    
    // 后端图表生成方法
    async generateBackendChart() {
      if (this.renderMode !== 'backend') {
        return;
      }
      
      try {
        this.loading = true;
        this.useBackendRendering = true;
        this.chartPath = null;
        
        const response = await fetch('/charts/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...this.getChartConfig(),
            chart_type: 'bar'
          }),
          credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
          this.chartPath = result.chart_path;
          // 如果前端图表实例存在，销毁它
          if (this.chart) {
            this.chart.dispose();
            this.chart = null;
          }
        } else {
          console.error('生成图表失败:', result.error);
          this.useBackendRendering = false;
          this.loading = false;
          // 重新初始化前端图表
          this.initChart();
        }
      } catch (error) {
        console.error('请求生成图表时出错:', error);
        this.useBackendRendering = false;
        this.loading = false;
        // 重新初始化前端图表
        this.initChart();
      } finally {
        this.loading = false;
      }
    },
    
    // 前端图表绘制方法
    drawChart() {
      if (this.renderMode !== 'frontend') {
        return;
      }
      
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
            text: this.chartTitle,
            left: 'center',
            textStyle: {
              color: '#666',
              fontSize: 16
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
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
            type: this.chartStyles.horizontal ? yAxisType : xAxisType,
            name: this.chartStyles.horizontal ? this.yAxisColumn : this.xAxisColumn,
            data: (!this.chartStyles.horizontal && xAxisType === 'category') ? xAxisData : undefined,
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
            boundaryGap: true,
            min: 'dataMin',
            max: 'dataMax'
          },
          yAxis: {
            type: this.chartStyles.horizontal ? xAxisType : yAxisType,
            name: this.chartStyles.horizontal ? this.xAxisColumn : this.yAxisColumn,
            data: (this.chartStyles.horizontal && xAxisType === 'category') ? xAxisData : undefined,
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
            type: 'bar',
            data: this.chartStyles.horizontal ? seriesData.map(item => [item[1], item[0]]) : seriesData,
            itemStyle: {
              color: this.colorSchemes[this.currentColorScheme][0] || this.customColors.bar
            },
            barWidth: '60%',
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
          ]
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
    
    switchRenderMode() {
      if (this.renderMode === 'backend') {
        this.generateBackendChart();
      } else {
        this.drawChart();
      }
      this.onConfigChange();
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

.chart-container {
  width: 100%;
  height: 500px;
  margin-bottom: 20px;
}

.no-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  color: #909399;
  font-size: 14px;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  color: #666;
  font-size: 16px;
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

.render-mode-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.title-input input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.title-input input:focus {
  outline: none;
  border-color: #409eff;
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