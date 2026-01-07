<template>
  <div class="clustering-config">
    <div class="clustering-type-selector">
      <h3>聚类方法</h3>
      <div class="radio-group">
        <label v-for="method in clusteringMethods" :key="method.value" class="radio-label">
          <input 
            type="radio" 
            :value="method.value" 
            v-model="localConfig.method"
            @change="onConfigChange"
          >
          {{ method.label }}
        </label>
      </div>
    </div>

    <div class="clustering-config-content">
      <!-- 方法描述 -->
      <div class="method-description" v-if="localConfig.method === 'kmeans'">
        <p>K-Means是最常用的聚类算法之一，它将数据划分为预定义数量的簇。算法通过迭代优化簇中心，使得每个点到其所属簇中心的距离最小化。</p>
        <p>优点：简单、快速、易于理解和实现。缺点：需要预先指定簇的数量，对初始值敏感。</p>
      </div>
      <div class="method-description" v-else-if="localConfig.method === 'hierarchical'">
        <p>层次聚类创建一个树状结构（称为树状图），显示数据点如何逐步合并或拆分。可以是凝聚式（自底向上）或分裂式（自顶向下）。</p>
        <p>优点：不需要预先指定簇的数量，可以提供数据的层次结构信息。缺点：计算复杂度高，不适合大数据集。</p>
      </div>
      <div class="method-description" v-else-if="localConfig.method === 'dbscan'">
        <p>基于密度的聚类算法，能够发现任意形状的簇，并能识别噪声点。它将数据点分为核心点、边界点和噪声点。</p>
        <p>优点：能发现任意形状的簇，对噪声鲁棒，不需要预先指定簇的数量。缺点：对参数敏感，不适合密度差异很大的数据集。</p>
      </div>
      <div class="method-description" v-else-if="localConfig.method === 'gmm'">
        <p>概率模型，假设数据由多个高斯分布混合而成。每个高斯分布代表一个簇，通过期望最大化(EM)算法进行参数估计。</p>
        <p>优点：提供软聚类（概率分配），能拟合椭圆形簇。缺点：计算复杂度较高，需要指定簇的数量。</p>
      </div>

      <!-- 簇数量设置 -->
      <div v-if="localConfig.method !== 'dbscan'" class="config-section">
        <div class="form-group">
          <label class="section-title">簇数量</label>
          <input
            type="number"
            v-model.number="localConfig.n_clusters"
            @input="onConfigChange"
            min="2"
            max="20"
            class="form-control"
          >
          <p class="form-help-text">指定要生成的簇的数量</p>
        </div>
      </div>

      <!-- 算法特定参数 -->
      <div v-if="localConfig.method === 'kmeans'" class="config-section">
        <div class="form-group">
          <label class="section-title">初始化方法</label>
          <select
            v-model="localConfig.params.init"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="k-means++">k-means++</option>
            <option value="random">random</option>
          </select>
        </div>
        <div class="form-group">
          <label class="section-title">最大迭代次数</label>
          <input
            type="number"
            v-model.number="localConfig.params.max_iter"
            @input="onConfigChange"
            min="10"
            max="1000"
            class="form-control"
          >
        </div>
      </div>

      <div v-if="localConfig.method === 'dbscan'" class="config-section">
        <div class="form-group">
          <label class="section-title">邻域半径 (eps)</label>
          <input
            type="number"
            step="0.1"
            v-model.number="localConfig.params.eps"
            @input="onConfigChange"
            min="0.1"
            max="2.0"
            class="form-control"
          >
        </div>
        <div class="form-group">
          <label class="section-title">最小样本数</label>
          <input
            type="number"
            v-model.number="localConfig.params.min_samples"
            @input="onConfigChange"
            min="2"
            max="20"
            class="form-control"
          >
        </div>
      </div>

      <div v-if="localConfig.method === 'hierarchical'" class="config-section">
        <div class="form-group">
          <label class="section-title">链接方法</label>
          <select
            v-model="localConfig.params.linkage"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="ward">Ward</option>
            <option value="complete">Complete</option>
            <option value="average">Average</option>
            <option value="single">Single</option>
          </select>
        </div>
      </div>

      <div v-if="localConfig.method === 'gmm'" class="config-section">
        <div class="form-group">
          <label class="section-title">协方差类型</label>
          <select
            v-model="localConfig.params.covariance_type"
            @change="onConfigChange"
            class="form-control"
          >
            <option value="full">Full</option>
            <option value="tied">Tied</option>
            <option value="diag">Diag</option>
            <option value="spherical">Spherical</option>
          </select>
        </div>
        <div class="form-group">
          <label class="section-title">最大迭代次数</label>
          <input
            type="number"
            v-model.number="localConfig.params.max_iter"
            @input="onConfigChange"
            min="10"
            max="1000"
            class="form-control"
          >
        </div>
      </div>

      <!-- 数据预处理选项 -->
      <div class="config-section">
        <div class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="localConfig.params.standardize"
              @change="onConfigChange"
            >
            标准化数据
          </label>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ClusteringConfig',
  props: {
    config: {
      type: Object,
      default: () => ({
        method: 'kmeans',
        n_clusters: 3,
        params: {
          standardize: true,
          init: 'k-means++',
          max_iter: 300,
          eps: 0.5,
          min_samples: 5,
          linkage: 'ward',
          covariance_type: 'full'
        }
      })
    },
    availableColumns: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localConfig: { ...this.config },
      clusteringMethods: [
        { value: 'kmeans', label: 'K-Means聚类' },
        { value: 'hierarchical', label: '层次聚类' },
        { value: 'dbscan', label: 'DBSCAN聚类' },
        { value: 'gmm', label: '高斯混合模型(GMM)' }
      ]
    };
  },
  watch: {
    config: {
      handler(newConfig) {
        this.localConfig = { ...newConfig };
      },
      deep: true
    }
  },
  methods: {
    onConfigChange() {
      this.$emit('update:config', { ...this.localConfig });
    }
  },
  mounted() {
    this.$emit('update:config', this.localConfig);
  }
};
</script>

<style scoped>
.clustering-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.clustering-type-selector {
  margin-bottom: 20px;
}

.clustering-type-selector h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.radio-label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
  margin-right: 15px;
}

.radio-label input[type="radio"] {
  margin-right: 5px;
}

.clustering-config-content {
  flex: 1;
}

.config-section {
  margin-bottom: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #606266;
}

.section-title {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #409eff;
}

.form-help-text {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}

.method-description {
  background-color: #f5f5f5;
  border-left: 4px solid #409eff;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.method-description p {
  margin: 0 0 5px 0;
}

.method-description .formula {
  font-family: 'Cambria Math', 'Arial Unicode MS', serif;
  margin: 5px 0;
}

.method-description .formula-desc {
  font-size: 12px;
  color: #888;
  margin: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin-right: 5px;
}
</style>