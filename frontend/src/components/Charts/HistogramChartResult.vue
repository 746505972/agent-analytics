<template>
  <div class="controls">
    <div class="control-group">
      <label>选择字段:</label>
      <select v-model="selectedColumn" @change="drawChart">
        <option v-for="col in numericColumns" :key="col" :value="col">{{ col }}</option>
      </select>
    </div>
    <div class="control-group">
      <label>分箱数:</label>
      <input 
        type="range" 
        min="5" 
        max="50" 
        v-model="binCount" 
        @change="drawChart"
      />
      <span>{{ binCount }}</span>
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
            <label>柱体颜色:</label>
            <input
              type="color"
              v-model="customColors.histogram"
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
<!--              <label>-->
<!--                <input-->
<!--                  type="checkbox"-->
<!--                  v-model="chartStyles.showDensity"-->
<!--                  @change="applyStyleChanges"-->
<!--                />-->
<!--                显示密度曲线-->
<!--              </label>-->
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
  name: "HistogramChartResult",
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null,
      selectedColumn: '',
      binCount: 20,
    binCountWatcher: 0,
      showConfigPopup: false,
      currentColorScheme: 0,
      colorSchemes: [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
      ],
      customColors: {
        histogram: '#5470c6'
      },
      chartStyles: {
        showGrid: true,
        showDensity: false
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
    selectedColumn() {
      this.drawChart();
    },
    binCount: {
      handler() {
        this.drawChart();
      }
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
        if (!this.selectedColumn && this.numericColumns.length > 0) {
          this.selectedColumn = this.numericColumns[0];
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
    
    calculateHistogramData() {
      if (!this.selectedColumn || !this.datasetDetails || !this.datasetDetails.data) {
        return { bins: [], counts: [] };
      }
      
      // 提取选定列的数据
      const rawData = this.datasetDetails.data
        .map(row => row[this.selectedColumn]);
      
      // 过滤掉无效值并转换为数字
      const data = rawData
        .filter(val => val !== null && val !== undefined && val !== '' && !isNaN(parseFloat(val)))
        .map(val => parseFloat(val));
      
      if (data.length === 0) {
        return { bins: [], counts: [] };
      }
      
      // 计算最小值和最大值
      const min = Math.min(...data);
      const max = Math.max(...data);
      
      // 如果所有值都相同
      if (min === max) {
        return {
          bins: [min, min],
          counts: [data.length]
        };
      }
      
      // 确保分箱数不超过数据点数
      const actualBinCount = Math.min(this.binCount, data.length);
      
      // 计算分箱
      const binWidth = (max - min) / actualBinCount;
      const bins = [];
      const counts = new Array(actualBinCount).fill(0);
      
      // 创建分箱边界
      for (let i = 0; i <= actualBinCount; i++) {
        bins.push(min + i * binWidth);
      }
      
      // 统计每个分箱中的数据数量
      data.forEach(value => {
        // 特殊处理最大值，确保它被分配到最后一个分箱
        let binIndex;
        if (value === max) {
          binIndex = actualBinCount - 1;
        } else {
          binIndex = Math.min(Math.floor((value - min) / binWidth), actualBinCount - 1);
        }
        counts[binIndex]++;
      });
      
      return { bins, counts };
    },
    
    drawChart() {
      // 检查必要条件是否满足
      if (!this.chart || !this.selectedColumn || 
          !this.datasetDetails || !this.datasetDetails.data || this.datasetDetails.data.length === 0) {
        return;
      }
      
      try {
        const histData = this.calculateHistogramData();
        
        if (histData.bins.length === 0) {
          return;
        }
        
        // 准备直方图系列数据
        const seriesData = histData.bins.slice(0, -1).map((binStart, index) => {
          return {
            name: binStart.toFixed(2) + ' - ' + histData.bins[index + 1].toFixed(2),
            value: histData.counts[index] || 0
          };
        });
        
        // 准备密度曲线数据（如果启用）
        let densitySeries = [];
        if (this.chartStyles.showDensity) {
          // 计算密度数据 - 简化的核密度估计
          const totalCount = histData.counts.reduce((sum, count) => sum + count, 0);
          const binWidth = histData.bins.length > 1 ? (histData.bins[1] - histData.bins[0]) : 1;
          
          const densityData = histData.bins.slice(0, -1).map((binStart, index) => {
            // 计算概率密度 = 频率 / (总数量 * 分箱宽度)
            const density = totalCount > 0 && binWidth > 0 ? 
              histData.counts[index] / (totalCount * binWidth) : 0;
            // 使用分箱中点作为X坐标
            const xCoord = binStart + binWidth / 2;
            return [xCoord, density];
          });
          
          densitySeries = [{
            name: '密度曲线',
            type: 'line',
            smooth: true,
            data: densityData,
            yAxisIndex: 1,
            itemStyle: {
              color: this.colorSchemes[this.currentColorScheme][1] || '#ff7f0e'
            },
            lineStyle: {
              width: 2
            },
            emphasis: {
              focus: 'series'
            }
          }];
        }
        
        const option = {
          title: {
            text: '直方图',
            left: 'center',
            textStyle: {
              color: '#666',
              fontSize: 16
            }
          },
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'shadow'
            },
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            textStyle: {
              color: '#fff'
            },
            formatter: (params) => {
              // 如果是直方图系列
              if (params.seriesName === '频率') {
                if (!params.data || params.data.value === undefined) {
                  return `${params.name}<br/>计数: 0`;
                }
                return `${params.name}<br/>计数: ${params.data.value}`;
              } 
              // 如果是密度曲线系列
              else if (params.seriesName === '密度曲线') {
                if (!params.data || params.data[1] === undefined) {
                  return `${params.name}<br/>密度: 0`;
                }
                return `${params.axisValue !== undefined ? params.axisValue.toFixed(2) : params.name}<br/>密度: ${params.data[1].toExponential(2)}`;
              }
              return params.name;
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
            type: 'category',
            data: histData.bins.slice(0, -1).map((bin, index) => 
              bin.toFixed(2) + ' - ' + histData.bins[index + 1].toFixed(2)),
            axisLabel: {
              color: '#666',
              rotate: 45
            },
            axisLine: {
              lineStyle: {
                color: '#ccc'
              }
            },
            name: this.selectedColumn,
            nameLocation: 'middle',
            nameGap: 30
          },
          yAxis: [
            {
              type: 'value',
              name: '频率',
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
              }
            },
            {
              type: 'value',
              name: '密度',
              position: 'right',
              axisLabel: {
                color: '#666',
                formatter: (value) => {
                  // 格式化密度值，保留合适的位数
                  return value.toExponential(2);
                }
              },
              axisLine: {
                lineStyle: {
                  color: '#ccc'
                }
              },
              splitLine: {
                show: false
              }
            }
          ],
          series: [
            {
              name: '频率',
              type: 'bar',
              data: seriesData,
              itemStyle: {
                color: this.colorSchemes[this.currentColorScheme][0] || this.customColors.histogram
              },
              barWidth: '90%',
              emphasis: {
                focus: 'series'
              }
            },
            ...densitySeries
          ]
        };
        
        // 如果不显示网格线
        if (!this.chartStyles.showGrid) {
          option.xAxis.splitLine = { show: false };
          option.yAxis[0].splitLine = { show: false };
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
      this.colorSchemes[0][0] = this.customColors.histogram;
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
  align-items: center;
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

.control-group input[type="range"] {
  width: 100px;
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