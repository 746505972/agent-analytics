<template>
  <div class="data-transformation-config">
    <div class="transformation-type-selector">
      <h3>数据转换类型</h3>
      <div class="radio-group">
        <label v-for="type in transformationTypes" :key="type.value" class="radio-label">
          <input 
            type="radio" 
            :value="type.value" 
            v-model="selectedTransformationType"
            @change="onTransformationTypeChange"
          >
          {{ type.label }}
        </label>
      </div>
    </div>

    <div class="transformation-config">
      <!-- 量纲处理配置 -->
      <div v-if="selectedTransformationType === 'dimensionless'">
        <h3>量纲处理</h3>
        <div class="form-group">
          <label>处理方法:</label>
          <select v-model="dimensionlessMethod" class="form-control">
            <option value="standard">Z-score标准化</option>
            <option value="minmax">最小-最大归一化 [0,1]</option>
            <option value="robust">鲁棒缩放</option>
            <option value="unit">单位向量化 (L2范数)</option>
            <option value="quantile">分位数变换</option>
            <option value="yeo-johnson">Yeo-Johnson变换</option>
            <option value="box-cox">Box-Cox变换</option>
            <option value="l1">L1范数标准化</option>
            <option value="l2">L2范数标准化</option>
            <option value="max">最大值标准化</option>
          </select>
        </div>

        <!-- 特定方法的额外参数 -->
        <div v-if="dimensionlessMethod === 'quantile'" class="form-group">
          <label>分位数数量:</label>
          <input 
            type="number" 
            v-model.number="quantileParams.n_quantiles" 
            class="form-control"
            min="1"
            max="1000"
          >
          
          <label>输出分布:</label>
          <select v-model="quantileParams.output_distribution" class="form-control">
            <option value="uniform">均匀分布</option>
            <option value="normal">正态分布</option>
          </select>
        </div>
        
        <div v-if="dimensionlessMethod === 'yeo-johnson' || dimensionlessMethod === 'box-cox'" class="form-group">
          <label>
            <input 
              type="checkbox" 
              v-model="powerParams.standardize"
            >
            标准化
          </label>
        </div>
      </div>

      <!-- 科学计算配置 -->
      <div v-else-if="selectedTransformationType === 'scientific'">
        <h3>科学计算</h3>
        <div class="form-group">
          <label>计算类型:</label>
          <select v-model="scientificOperation" class="form-control">
            <option value="log">对数变换</option>
            <option value="exp">指数变换</option>
            <option value="power">幂变换</option>
            <option value="sqrt">平方根变换</option>
            <option value="poly">多项式特征</option>
          </select>
        </div>

        <!-- 特定操作的参数 -->
        <div v-if="scientificOperation === 'power'" class="form-group">
          <label>幂指数:</label>
          <input 
            type="number" 
            v-model.number="powerParams.power" 
            class="form-control"
            step="0.1"
          >
        </div>
        
        <div v-else-if="scientificOperation === 'poly'" class="form-group">
          <label>多项式度数:</label>
          <input 
            type="number" 
            v-model.number="polyParams.degree" 
            class="form-control"
            min="2"
            max="5"
          >
        </div>
      </div>

      <!-- 独热编码配置 -->
      <div v-else-if="selectedTransformationType === 'onehot'">
        <h3>独热编码</h3>
        <div class="form-group">
          <label>
            <input 
              type="checkbox" 
              v-model="onehotParams.drop_first"
            >
            删除第一个虚拟变量（避免多重共线性）
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataTransformationConfig",
  props: {
    selectedFileColumns: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      // 转换类型选项
      transformationTypes: [
        { value: 'dimensionless', label: '量纲处理' },
        { value: 'scientific', label: '科学计算' },
        { value: 'onehot', label: '独热编码' }
      ],
      
      // 当前选中的转换类型
      selectedTransformationType: 'dimensionless',
      
      // 量纲处理参数
      dimensionlessMethod: 'standard',
      quantileParams: {
        n_quantiles: 100,
        output_distribution: 'uniform'
      },
      powerParams: {
        standardize: true,
        power: 2
      },
      
      // 科学计算参数
      scientificOperation: 'log',
      polyParams: {
        degree: 2
      },
      
      // 独热编码参数
      onehotParams: {
        drop_first: false
      }
    };
  },
  methods: {
    onTransformationTypeChange() {
      // 当转换类型改变时，通知父组件
      this.$emit('config-change', this.getConfig());
    },
    
    getConfig() {
      // 返回当前配置
      return {
        transformationType: this.selectedTransformationType,
        dimensionless: {
          method: this.dimensionlessMethod,
          ...(this.dimensionlessMethod === 'quantile' && { params: this.quantileParams }),
          ...( (this.dimensionlessMethod === 'yeo-johnson' || this.dimensionlessMethod === 'box-cox') && { params: this.powerParams })
        },
        scientific: {
          operation: this.scientificOperation,
          ...(this.scientificOperation === 'power' && { params: { power: this.powerParams.power } }),
          ...(this.scientificOperation === 'poly' && { params: this.polyParams })
        },
        onehot: {
          drop_first: this.onehotParams.drop_first
        }
      };
    }
  },
  watch: {
    // 监听所有配置的变化并通知父组件
    dimensionlessMethod() {
      this.$emit('config-change', this.getConfig());
    },
    scientificOperation() {
      this.$emit('config-change', this.getConfig());
    },
    'quantileParams.n_quantiles'() {
      this.$emit('config-change', this.getConfig());
    },
    'quantileParams.output_distribution'() {
      this.$emit('config-change', this.getConfig());
    },
    'powerParams.standardize'() {
      this.$emit('config-change', this.getConfig());
    },
    'powerParams.power'() {
      this.$emit('config-change', this.getConfig());
    },
    'polyParams.degree'() {
      this.$emit('config-change', this.getConfig());
    },
    'onehotParams.drop_first'() {
      this.$emit('config-change', this.getConfig());
    }
  },
  mounted() {
    // 初始化时发送一次配置
    this.$emit('config-change', this.getConfig());
  }
};
</script>

<style scoped>
.data-transformation-config {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.transformation-type-selector {
  margin-bottom: 20px;
}

.transformation-type-selector h3 {
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

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #606266;
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

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 5px;
}
</style>
