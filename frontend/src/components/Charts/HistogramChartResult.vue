<template>
  <div class="controls">
    <div class="control-group">
      <label>选择字段:</label>
      <select v-model="selectedColumn" @change="onConfigChange">
        <option v-for="col in numericColumns" :key="col" :value="col">{{ col }}</option>
      </select>
    </div>
    <div class="control-group">
      <label>分箱数:</label>
      <input 
        type="range" 
        min="5" 
        max="50" 
        v-model="chartStyles.bin_count"
        @change="onConfigChange"
      />
      <span>{{ chartStyles.bin_count }}</span>
    </div>
    <!-- 图表配置按钮 -->
    <div class="control-group">
      <button class="config-button" @click="showConfigPopup = true">
        图表配置
      </button>
    </div>
  </div>

  <BackendChartResult
    :chart-path="chartPath"
    :loading="loading"
  />

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
              <label>
                <input
                  type="checkbox"
                  v-model="chartStyles.showLabel"
                  @change="applyStyleChanges"
                />
                显示数据标签
              </label>
            </div>
            <div class="style-option">
              <label>
                <input
                  type="checkbox"
                  v-model="chartStyles.showLegend"
                  @change="applyStyleChanges"
                />
                显示图例
              </label>
            </div>
            <div class="style-option">
              <label>
                <input
                  type="checkbox"
                  v-model="chartStyles.showToolbox"
                  @change="applyStyleChanges"
                />
                显示工具箱
              </label>
            </div>
          </div>
        </div>
        
        <div class="config-section">
          <h4>坐标轴设置</h4>
          <div class="axis-options">
            <div class="axis-option">
              <label>X轴标签旋转角度:</label>
              <input
                type="range"
                v-model="chartStyles.xAxisLabelRotate"
                @change="applyStyleChanges"
                min="0"
                max="90"
                step="5"
              />
              <span>{{ chartStyles.xAxisLabelRotate }}°</span>
            </div>
            <div class="axis-option">
              <label>Y轴最小值:</label>
              <input
                type="number"
                v-model="chartStyles.yAxisMin"
                @change="applyStyleChanges"
                placeholder="自动"
              />
            </div>
            <div class="axis-option">
              <label>Y轴最大值:</label>
              <input
                type="number"
                v-model="chartStyles.yAxisMax"
                @change="applyStyleChanges"
                placeholder="自动"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BackendChartResult from "@/components/Charts/BackendChartResult.vue";

export default {
  name: "HistogramChartResult",
  components: {BackendChartResult},
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedColumn: '',
      chartPath: null,
      loading: false,
      showConfigPopup: false,
      currentColorScheme: 0,
      chartTitle: '直方图',
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
        showLabel: false,
        showLegend: true,
        xAxisLabelRotate: 0,
        yAxisMin: null,
        yAxisMax: null,
        showToolbox: true,
        bin_count: 20  // 添加分箱数配置
      }
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
        if (newVal && newVal.column_info) {
          this.generateBackendChart();
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    onConfigChange() {
      if (this.selectedColumn) {
        this.generateBackendChart();
      }
    },
    
    getChartConfig() {
      // 返回当前图表配置
      return {
        data_id: this.datasetDetails.data_id || 'default',
        x_axis_column: this.selectedColumn,
        y_axis_columns: [], // 直方图不需要Y轴字段
        chart_title: this.chartTitle,
        chart_styles: this.chartStyles,
        color_scheme: this.currentColorScheme,
        custom_colors: this.customColors,
        chart_type: 'histogram',
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
      this.colorSchemes[0][0] = this.customColors.histogram;
      this.currentColorScheme = 0; // 切换到自定义配色方案
      this.onConfigChange();
    },
    
    applyStyleChanges() {
      this.onConfigChange();
    },

    onTitleChange() {
      this.onConfigChange();
    },
    // 后端图表生成方法
    async generateBackendChart() {
      try {
        this.loading = true;
        this.chartPath = null;
        
        const response = await fetch('/charts/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...this.getChartConfig(),
            chart_type: 'histogram'
          }),
          credentials: 'include'
        });

        const result = await response.json();
        if (result.success) {
          this.chartPath = result.chart_path;
        } else {
          console.error('生成图表失败:', result.error);
        }
      } catch (error) {
        console.error('请求生成图表时出错:', error);
      } finally {
        this.loading = false;
      }
    }
  },
  
  mounted() {
    this.selectedColumn = this.numericColumns[0];
    // 初始化后端图表生成
    this.generateBackendChart();
  }
};
</script>

<style scoped>
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
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  width: 600px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.popup-header {
  padding: 16px 20px;
  background-color: #f5f7fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #606266;
  border-bottom: 1px solid #dcdfe6;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
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
  padding: 20px;
  overflow-y: auto;
}

.config-section {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #e4e7ed;
}

.config-section:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.config-section h4 {
  margin: 5px 0 5px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.config-section h4::before {
  content: "";
  display: inline-block;
  width: 4px;
  height: 16px;
  background-color: #409eff;
  margin-right: 10px;
  border-radius: 2px;
}

.color-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 12px;
  margin-top: 10px;
}

.color-scheme-option {
  cursor: pointer;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  padding: 12px 8px;
  text-align: center;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.color-scheme-option:hover,
.color-scheme-option.active {
  border-color: #409eff;
  box-shadow: 0 4px 8px rgba(64, 158, 255, 0.2);
  transform: translateY(-2px);
}

.color-preview {
  display: flex;
  height: 24px;
  margin-bottom: 8px;
  border-radius: 3px;
  overflow: hidden;
  width: 100%;
}

.color-item {
  flex: 1;
}

.custom-color-picker {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
}

.custom-color-picker label {
  font-size: 14px;
  color: #606266;
  min-width: 80px;
}

.style-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  margin-top: 10px;
}

.style-option label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.style-option label:hover {
  background-color: #f5f7fa;
}

.axis-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 10px;
}

.axis-option {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.axis-option label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 2px;
}

.axis-option input[type="range"] {
  width: 100%;
}

.axis-option input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
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