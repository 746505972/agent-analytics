<template>
  <div class="chart-container">
    <div v-if="chartPath" class="chart-content">
      <iframe 
        :src="fullChartUrl" 
        width="100%"
        height="100%" 
        frameborder="0" 
        @load="onChartLoaded"
      ></iframe>
    </div>
    <div v-else-if="loading" class="loading">
      <Waiting />
    </div>
    <div v-else class="no-chart">
      <p>暂无图表数据</p>
    </div>
  </div>
</template>

<script>
import Waiting from "@/components/Waiting.vue";
import { backendBaseUrl } from '@/api/apiConfig';

export default {
  name: "BackendChartResult",
  components: {Waiting},
  props: {
    chartPath: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      loading: false,
      backendBaseUrl: backendBaseUrl
    };
  },
  computed: {
    fullChartUrl() {
      if (!this.chartPath) {
        return '';
      }
      
      // 如果chartPath已经是完整URL，则直接返回
      if (this.chartPath.startsWith('http')) {
        return this.chartPath;
      }
      
      // 如果chartPath是相对路径，添加后端基础URL
      // 使用apiConfig中的后端基础URL
      return `${this.backendBaseUrl}/${this.chartPath}`;
    }
  },
  methods: {
    onChartLoaded() {
      this.$emit('chart-loaded');
    }
  },
  mounted() {
    if (this.chartPath) {
      this.loading = true;
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 550px;
  overflow: visible;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

.chart-content {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.loading, .no-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  font-size: 16px;
  color: #666;
}
</style>