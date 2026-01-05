<template>
  <div class="sentiment-analysis-result" v-if="datasetDetails.resultMethod === 'sentiment_analysis'">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>正在进行情感分析...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>情感分析时出错: {{ error }}</p>
    </div>
    <div v-else-if="sentimentData" class="result-content">
      <!-- 图表容器 -->
      <div class="charts-wrapper">
        <!-- 情感分布饼图 -->
        <div class="chart-container">
          <div class="chart-header">
            <h3>情感分布</h3>
            <!-- 图表配置按钮 -->
            <div class="chart-controls">
              <button class="config-button" @click="showPieConfigPopup = true">
                图表配置
              </button>
            </div>
          </div>
          <div ref="pieChart" class="chart"></div>
        </div>

        <!-- 情感强度箱线图 -->
        <div class="chart-container">
          <div class="chart-header">
            <h3>情感强度分布</h3>
            <!-- 图表配置按钮 -->
            <div class="chart-controls">
              <button class="config-button" @click="showBoxplotConfigPopup = true">
                图表配置
              </button>
            </div>
          </div>
          <div ref="boxplotChart" class="chart"></div>
        </div>
      </div>
      
      <!-- 统计信息 -->
      <div class="info-container">
        <h3>分析信息</h3>
        <div class="info-card">
          <div class="info-item">
            <span class="info-label">分析列:</span>
            <span class="info-value">{{ sentimentData.column }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">总评论数:</span>
            <span class="info-value">{{ sentimentData.statistics?.total_count || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">平均情感得分:</span>
            <span class="info-value">{{ sentimentData.statistics?.average_score?.toFixed(3) || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">得分标准差:</span>
            <span class="info-value">{{ sentimentData.statistics?.std_score?.toFixed(3) || 'N/A' }}</span>
          </div>
        </div>
        
        <!-- 情感比例详情 -->
        <div class="ratio-details">
          <h4>情感比例</h4>
          <div class="ratio-item positive">
            <span class="ratio-label">正面:</span>
            <span class="ratio-value">{{ sentimentData.sentiment_ratios?.positive ? (sentimentData.sentiment_ratios.positive * 100).toFixed(1) : 'N/A' }}%</span>
            <div class="ratio-bar">
              <div 
                class="ratio-fill positive" 
                :style="{ width: (sentimentData.sentiment_ratios?.positive ? (sentimentData.sentiment_ratios.positive * 100) : 0) + '%' }"
              ></div>
            </div>
          </div>
          <div class="ratio-item neutral">
            <span class="ratio-label">中性:</span>
            <span class="ratio-value">{{ sentimentData.sentiment_ratios?.neutral ? (sentimentData.sentiment_ratios.neutral * 100).toFixed(1) : 'N/A' }}%</span>
            <div class="ratio-bar">
              <div 
                class="ratio-fill neutral" 
                :style="{ width: (sentimentData.sentiment_ratios?.neutral ? (sentimentData.sentiment_ratios.neutral * 100) : 0) + '%' }"
              ></div>
            </div>
          </div>
          <div class="ratio-item negative">
            <span class="ratio-label">负面:</span>
            <span class="ratio-value">{{ sentimentData.sentiment_ratios?.negative ? (sentimentData.sentiment_ratios.negative * 100).toFixed(1) : 'N/A' }}%</span>
            <div class="ratio-bar">
              <div 
                class="ratio-fill negative" 
                :style="{ width: (sentimentData.sentiment_ratios?.negative ? (sentimentData.sentiment_ratios.negative * 100) : 0) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 饼图配置浮窗 -->
    <div v-if="showPieConfigPopup" class="config-popup-overlay" @click.self="showPieConfigPopup = false">
      <div class="config-popup">
        <div class="popup-header">
          <span>饼图配置</span>
          <button class="close-btn" @click="showPieConfigPopup = false">×</button>
        </div>
        <div class="popup-content">
          <div class="config-section">
            <h4>图表标题</h4>
            <div class="title-input">
              <input
                type="text"
                v-model="pieChartTitle"
                @input="updateCharts"
                placeholder="请输入图表标题"
              />
            </div>
            <h4>配色方案</h4>
            <div class="color-options">
              <div
                v-for="(colorScheme, index) in colorSchemes"
                :key="index"
                :class="['color-scheme-option', { active: pieColorScheme === index }]"
                @click="selectPieColorScheme(index)"
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
        </div>
      </div>
    </div>

    <!-- 箱线图配置浮窗 -->
    <div v-if="showBoxplotConfigPopup" class="config-popup-overlay" @click.self="showBoxplotConfigPopup = false">
      <div class="config-popup">
        <div class="popup-header">
          <span>箱线图配置</span>
          <button class="close-btn" @click="showBoxplotConfigPopup = false">×</button>
        </div>
        <div class="popup-content">
          <div class="config-section">
            <h4>图表标题</h4>
            <div class="title-input">
              <input
                type="text"
                v-model="boxplotChartTitle"
                @input="updateCharts"
                placeholder="请输入图表标题"
              />
            </div>
            <h4>配色方案</h4>
            <div class="color-options">
              <div
                v-for="(colorScheme, index) in colorSchemes"
                :key="index"
                :class="['color-scheme-option', { active: boxplotColorScheme === index }]"
                @click="selectBoxplotColorScheme(index)"
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
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "SentimentAnalysisResult",
  props: {
    datasetDetails: {
      type: Object,
      default: () => null
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      pieChart: null,
      boxplotChart: null,
      showPieConfigPopup: false,
      showBoxplotConfigPopup: false,
      pieChartTitle: '情感分布',
      boxplotChartTitle: '情感强度分布',
      pieColorScheme: 0,
      boxplotColorScheme: 0,
      colorSchemes: [
        ['#4CAF50', '#FFC107', '#F44336'],
        ['#66BB6A', '#FFD54F', '#EF9A9A'],
        ['#2E7D32', '#F9A825', '#C62828'],
        ['#00C853', '#FFAB00', '#FF5252'],
        ['#5470c6', '#91cc75', '#fac858'],
        ['#c23531', '#2f4554', '#61a0a8'],
        ['#ee6666', '#73c0de', '#3ba272'],
        ['#dd6b66', '#759aa0', '#e69d87'],
      ],
      resizeObserver: null
    };
  },
  mounted() {
    this.initCharts();
    this.setupResizeObserver();
  },
  beforeUnmount() {
    if (this.pieChart) {
      this.pieChart.dispose();
    }
    if (this.boxplotChart) {
      this.boxplotChart.dispose();
    }
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }
  },
  methods: {
    initCharts() {
      if (this.$refs.pieChart) {
        this.pieChart = echarts.init(this.$refs.pieChart);
      }
      if (this.$refs.boxplotChart) {
        this.boxplotChart = echarts.init(this.$refs.boxplotChart);
      }
      this.updateCharts();
    },
    setupResizeObserver() {
      // 创建ResizeObserver来监听容器大小变化
      this.resizeObserver = new ResizeObserver(() => {
        if (this.pieChart) {
          this.pieChart.resize();
        }
        if (this.boxplotChart) {
          this.boxplotChart.resize();
        }
      });
      
      // 监听图表容器变化
      if (this.$refs.pieChart) {
        this.resizeObserver.observe(this.$refs.pieChart);
      }
      if (this.$refs.boxplotChart) {
        this.resizeObserver.observe(this.$refs.boxplotChart);
      }
    },
    percentile(arr, p) {
      if (arr.length === 0) return 0;
      if (p <= 0) return arr[0];
      if (p >= 100) return arr[arr.length - 1];

      const index = (p / 100) * (arr.length - 1);
      const lower = Math.floor(index);
      const upper = lower + 1;
      const weight = index % 1;

      if (upper >= arr.length) return arr[lower];
      return arr[lower] * (1 - weight) + arr[upper] * weight;
    },
    updateCharts() {
      if (this.pieChart && this.pieChartData) {
        const pieOption = {
          title: {
            text: this.pieChartTitle,
            left: 'center',
            textStyle: {
              color: '#666',
              fontSize: 16
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          toolbox: {
            show: true,
            feature: {
              restore: {
                title: '刷新'
              },
              saveAsImage: {
                title: '下载图片'
              }
            }
          },
          series: [
            {
              name: '情感分布',
              type: 'pie',
              radius: '50%',
              data: this.pieChartData,
              color: this.colorSchemes[this.pieColorScheme],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
              label: {
                show: true,
                formatter: '{b}: {d}%'
              }
            }
          ]
        };
        this.pieChart.setOption(pieOption, true);
      }
      
      if (this.boxplotChart && this.boxplotData) {
        const boxplotOption = {
          title: {
            text: this.boxplotChartTitle,
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
            }
          },
          toolbox: {
            show: true,
            feature: {
              restore: {
                title: '刷新'
              },
              saveAsImage: {
                title: '下载图片'
              }
            }
          },
          xAxis: {
            type: 'category',
            data: ['正面', '中性', '负面']
          },
          yAxis: {
            type: 'value',
            name: '情感得分'
          },
          series: [
            {
              name: '情感强度',
              type: 'boxplot',
              data: this.boxplotData,
              color: this.colorSchemes[this.boxplotColorScheme],
              tooltip: {
                formatter: function (param) {
                  return [
                    '情感类型: ' + param.name,
                    '最大值: ' + param.data[5],
                    '上四分位数: ' + param.data[4], 
                    '中位数: ' + param.data[3],
                    '下四分位数: ' + param.data[2],
                    '最小值: ' + param.data[1]
                  ].join('<br/>');
                }
              }
            }
          ]
        };
        this.boxplotChart.setOption(boxplotOption, true);
      }
    },
    selectPieColorScheme(index) {
      this.pieColorScheme = index;
      this.updateCharts();
    },
    selectBoxplotColorScheme(index) {
      this.boxplotColorScheme = index;
      this.updateCharts();
    },
    getColorSchemeName(index) {
      const names = ['经典','经典柔和','经典商务','现代','默认', '深色', '明亮', '柔和'];
      return names[index] || `方案${index + 1}`;
    }
  },
  computed: {
    sentimentData() {
      return this.datasetDetails || null;
    },
    
    pieChartData() {
      if (!this.sentimentData?.echarts_data?.pie_chart) return [];
      return this.sentimentData.echarts_data.pie_chart;
    },
    
    boxplotData() {
      if (!this.sentimentData?.echarts_data?.boxplot_data) return [];
      
      const boxplotData = this.sentimentData.echarts_data.boxplot_data;
      const processData = (data) => {
        if (data.length === 0) return [0, 0, 0, 0, 0];
        data.sort((a, b) => a - b);
        const min = Math.min(...data);
        const max = Math.max(...data);
        const q1 = this.percentile(data, 25);
        const q3 = this.percentile(data, 75);
        const median = this.percentile(data, 50);
        return [min, q1, median, q3, max];
      };
      
      return [
        processData(boxplotData.positive),
        processData(boxplotData.neutral),
        processData(boxplotData.negative)
      ];
    }
  },
  watch: {
    data: {
      handler() {
        this.$nextTick(() => {
          this.updateCharts();
        });
      },
      deep: true
    }
  },
};
</script>

<style scoped>
.sentiment-analysis-result {
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.sentiment-analysis-result h3 {
  margin-top: 0;
  color: #303133;
  font-weight: 600;
}

.sentiment-analysis-result h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
  font-size: 18px;
}

.loading, .error {
  text-align: center;
}

.loading p, .error p {
  font-size: 16px;
  color: #606266;
  margin-top: 20px;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #409eff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-content {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.charts-wrapper {
  display: table-column;
  width: 100%;
  overflow: hidden;
}

.chart-container {
  flex: 1;
  min-width: 300px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  overflow: hidden;
  margin: 10px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.chart-header h3 {
  margin: 0;
}

.config-button {
  padding: 6px 12px;
  background-color: #f4f4f5;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
  font-size: 14px;
}

.config-button:hover {
  background-color: #e9e9eb;
}

.chart {
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.info-container {
  flex: 1;
  min-width: 300px;
}

.info-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 500;
  color: #606266;
}

.info-value {
  font-weight: 600;
  color: #303133;
}

.ratio-details {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.ratio-item {
  margin-bottom: 15px;
}

.ratio-item:last-child {
  margin-bottom: 0;
}

.ratio-label {
  display: inline-block;
  width: 60px;
  font-weight: 500;
  color: #606266;
}

.ratio-value {
  display: inline-block;
  width: 60px;
  font-weight: 600;
  text-align: right;
}

.ratio-bar {
  display: inline-block;
  width: calc(100% - 140px);
  height: 10px;
  background: #ebeef5;
  border-radius: 5px;
  overflow: hidden;
  vertical-align: middle;
  margin-left: 10px;
}

.ratio-fill {
  height: 100%;
}

.ratio-fill.positive {
  background: #67c23a;
}

.ratio-fill.neutral {
  background: #909399;
}

.ratio-fill.negative {
  background: #f56c6c;
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
  .result-content {
    flex-direction: column;
  }
  
  .chart-container,
  .info-container {
    min-width: 100%;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .color-options {
    justify-content: center;
  }
  
  .color-scheme-option {
    width: 80px;
  }
}
</style>