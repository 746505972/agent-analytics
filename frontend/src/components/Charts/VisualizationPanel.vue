<template>
  <div class="chart-selector">
    <label>图表类型:</label>
    <select v-model="selectedChartType" @change="renderChart">
      <option value="line">折线图</option>
      <option value="bar">柱状图</option>
      <option value="scatter">散点图</option>
      <option value="histogram">直方图</option>
      <option value="pie">饼图</option>
      <option value="boxplot">箱线图</option>
    </select>
  </div>

  <component
    :is="currentChartComponent"
    :dataset-details="datasetDetails"
  />

</template>

<script>
import LineChartResult from './LineChartResult.vue';
import BarChartResult from './BarChartResult.vue';
import ScatterPlotResult from './ScatterPlotResult.vue';
import HistogramChartResult from './HistogramChartResult.vue';
import PieChartResult from './PieChartResult.vue';
import BoxPlotResult from './BoxPlotResult.vue';

export default {
  name: "VisualizationPanel",
  components: {
    LineChartResult,
    BarChartResult,
    ScatterPlotResult,
    HistogramChartResult,
    PieChartResult,
    BoxPlotResult
  },
  props: {
    datasetDetails: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedChartType: 'line'
    };
  },
  computed: {
    currentChartComponent() {
      // 根据选择的图表类型动态返回对应的组件
      switch (this.selectedChartType) {
        case 'line':
          return 'LineChartResult';
        case 'bar':
          return 'BarChartResult';
        case 'scatter':
          return 'ScatterPlotResult';
        case 'histogram':
          return 'HistogramChartResult';
        case 'pie':
          return 'PieChartResult';
        case 'boxplot':
          return 'BoxPlotResult';
        default:
          return 'LineChartResult'; // 默认使用折线图
      }
    }
  },
  methods: {
    renderChart() {
      // 触发图表重新渲染
      this.$forceUpdate();
    },
  }
};
</script>

<style scoped>

.chart-selector {
  display: flex;
  margin-bottom: 20px;
}

.chart-selector label {
  margin-right: 10px;
  font-weight: bold;
}

.chart-selector select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

</style>