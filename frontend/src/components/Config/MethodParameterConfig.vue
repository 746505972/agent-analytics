<template>
  <!-- 加载指示器 -->
  <Waiting v-if="isWaitingForResponse"/>
  <div v-else>
    <div v-if="selectedFile && selectedFileColumns.length > 0" class="column-add-header-container">
      <!-- 列名列表区域 -->
      <div class="column-list-section">
        <div v-if="['missing_value_interpolation'].includes(currentMethod)">
          <div class="header">
            <h3>选择需要处理的列</h3> <DeleteColumns @click="clearSelectedColumns" />
          </div>
          <p>点击选择列，支持 Ctrl/Shift 多选</p>
          <p>不选则处理所有列</p>
        </div>
        <div v-else-if="['data_transformation','delete_columns'].includes(currentMethod)">
          <div class="header">
            <h3>选择需要处理的列</h3> <DeleteColumns @click="clearSelectedColumns" />
          </div>
          <p>点击选择列，支持 Ctrl/Shift 多选</p>
        </div>
        <div v-else-if="['statistical_summary','correlation_analysis', 't_test', 'normality_test','f_test','chi_square_test', 'non_parametric_test','clustering_analysis'].includes(currentMethod)">
          <div class="header">
            <h3>选择需要分析的列</h3> <DeleteColumns @click="clearSelectedColumns" />
          </div>
          <p>点击选择列，支持 Ctrl/Shift 多选</p>
          <p>不选则分析所有数值型列</p>
        </div>
        <div v-else-if="['linear_regression','logistic_regression'].includes(currentMethod)">
          <div class="header">
            <h3>选择自变量 (X)</h3> <DeleteColumns @click="clearSelectedColumns" />
          </div>
          <p>点击选择列，支持 Ctrl/Shift 多选</p>
          <p>不选则使用所有数值型列</p>
        </div>
        <div v-else-if="['text_analysis', 'sentiment_analysis'].includes(currentMethod)">
          <div class="header">
            <h3>选择需要处理的列</h3> <DeleteColumns @click="clearSelectedColumns" />
          </div>
          <p>点击选择一列，用于分析文本数据</p>
          <p>多选则默认分析第一列</p>
        </div>
        <div v-else>
          <h3>列名列表</h3>
        </div>

        <ul class="column-list">
          <li v-for="(column, index) in selectedFileColumns"
              :key="index"
              class="column-item"
              :class="{
                selected: isColumnSelected(column),
                clickable: selectableMethods.includes(currentMethod)
              }"
              @click="toggleColumnSelection($event, column, index)"
          >
            {{ column }}
          </li>
        </ul>
      </div>

      <!-- 参数配置区域 -->
      <AddHeaderConfig
        v-if="currentMethod === 'add_header' && headerEditMode !== 'remove'"
        :selected-file-columns="selectedFileColumns"
        :new-column-names="newColumnNames"
        @update:newColumnNames="handleNewColumnNamesUpdate"
      />

      <InvalidSamplesConfig
        v-else-if="currentMethod === 'invalid_samples'"
        v-model:config="configs.invalidSamplesConfig"
      />

      <MissingValueInterpolationConfig
        v-else-if="currentMethod === 'missing_value_interpolation'"
        v-model:config="configs.interpolationConfig"
      />

      <DataTransformationConfig
        v-else-if="currentMethod === 'data_transformation'"
        :selected-file-columns="selectedFileColumns"
        :selected-columns="selectedColumns"
        :data-transformation-config="dataTransformationConfig"
        @update:dataTransformationConfig="$emit('update:dataTransformationConfig', $event)"
        @config-change="$emit('update:dataTransformationConfig', $event)"
      />

      <CorrelationAnalysisConfig
        v-else-if="currentMethod === 'correlation_analysis'"
        v-model:correlation-method="configs.correlationMethod"
      />

      <TTestConfig
        v-else-if="currentMethod === 't_test'"
        v-model:config="configs.tTestConfig"
        :categorical-columns="selectedFileColumns"
      />

      <FTestConfig
        v-else-if="currentMethod === 'f_test'"
        v-model:config="configs.fTestConfig"
        :categorical-columns="selectedFileColumns"
      />

      <ChiSquareTestConfig
        v-else-if="currentMethod === 'chi_square_test'"
        v-model:config="configs.chiSquareTestConfig"
        :categorical-columns="selectedFileColumns"
      />

      <NonParametricTestConfig
        v-else-if="currentMethod === 'non_parametric_test'"
        v-model:config="configs.nonParametricTestConfig"
        :categorical-columns="selectedFileColumns"
      />

      <NormalityTestConfig
        v-else-if="currentMethod === 'normality_test'"
        v-model:config="configs.normalityTestConfig"
        :categorical-columns="selectedFileColumns"
      />

      <LinearRegressionConfig
        v-else-if="currentMethod === 'linear_regression'"
        v-model:config="configs.linearRegressionConfig"
        :available-columns="selectedFileColumns"
      />

      <LogisticRegressionConfig
        v-else-if="currentMethod === 'logistic_regression'"
        v-model:config="configs.logisticRegressionConfig"
        :available-columns="selectedFileColumns"
      />

      <ClusteringConfig
        v-else-if="currentMethod === 'clustering_analysis'"
        v-model:config="configs.clusteringConfig"
        :available-columns="selectedFileColumns"
      />

      <WordCloudConfig
        v-else-if="currentMethod === 'text_analysis'"
        :selected-file-columns="selectedFileColumns"
        v-model:wordcloud-config="configs.wordcloudConfig"
      />

      <SentimentAnalysisConfig
        v-else-if="currentMethod === 'sentiment_analysis'"
        :selected-file-columns="selectedFileColumns"
        v-model:sentiment-config="configs.sentimentConfig"
      />
    </div>

    <div v-else class="choose-file">
      <span>请选择一个文件</span>
    </div>
  </div>
</template>

<script>
import AddHeaderConfig from "./AddHeaderConfig.vue";
import InvalidSamplesConfig from "./InvalidSamplesConfig.vue";
import MissingValueInterpolationConfig from "./MissingValueInterpolationConfig.vue";
import DataTransformationConfig from "./DataTransformationConfig.vue";
import CorrelationAnalysisConfig from "./CorrelationAnalysisConfig.vue";
import TTestConfig from "./TTestConfig.vue";
import NormalityTestConfig from "./NormalityTestConfig.vue";
import WordCloudConfig from "./WordCloudConfig.vue";
import SentimentAnalysisConfig from "./SentimentAnalysisConfig.vue";
import FTestConfig from "@/components/Config/FTestConfig.vue";
import ChiSquareTestConfig from "@/components/Config/ChiSquareTestConfig.vue";
import NonParametricTestConfig from "@/components/Config/NonParametricTestConfig.vue";
import LinearRegressionConfig from "@/components/Config/LinearRegressionConfig.vue";
import { getDefaultConfigs } from '@/utils/configDefaults.js'
import Waiting from "@/components/Waiting.vue";
import LogisticRegressionConfig from "@/components/Config/LogisticRegressionConfig.vue";
import DeleteColumns from "@/components/DeleteColumns.vue";
import ClusteringConfig from "@/components/Config/ClusteringConfig.vue";

export default {
  name: "MethodParameterConfig",
  components: {
    ClusteringConfig,
    DeleteColumns,
    Waiting,
    ChiSquareTestConfig,
    FTestConfig,
    AddHeaderConfig,
    InvalidSamplesConfig,
    MissingValueInterpolationConfig,
    DataTransformationConfig,
    CorrelationAnalysisConfig,
    TTestConfig,
    NormalityTestConfig,
    WordCloudConfig,
    SentimentAnalysisConfig,
    LogisticRegressionConfig,
    NonParametricTestConfig,
    LinearRegressionConfig
  },
  props: {
    currentMethod: {
      type: String,
      required: true
    },
    selectedFile: {
      type: String,
      default: null
    },
    selectedFileColumns: {
      type: Array,
      required: true
    },
    selectedColumns: {
      type: Array,
      default: () => []
    },
    headerEditMode: {
      type: String,
      default: 'add'
    },
    newColumnNames: {
      type: Array,
      default: () => []
    },
    lastSelectedColumnIndex: {
      type: Number,
      default: -1
    },
    dataTransformationConfig: {
      type: Object,
      default: () => ({})
    },
    configs: {
      type: Object,
      default: getDefaultConfigs()
    },
    isWaitingForResponse: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    'update:removeDuplicates',
    'update:removeDuplicatesCols',
    'update:removeConstantCols',
    'update:rowMissingThreshold',
    'update:columnMissingThreshold',
    'update:newColumnNames',
    'update:dataTransformationConfig',
    'toggleColumnSelection',
    'clearSelectedColumns'
  ],
  data() {
    return {
      selectableMethods: [
        'missing_value_interpolation',
        'delete_columns',
        'data_transformation',
        'statistical_summary',
        'correlation_analysis',
        'text_analysis',
        'sentiment_analysis',
        't_test',
        'normality_test',
        'f_test',
        'chi_square_test',
        'non_parametric_test',
        'linear_regression',
        'logistic_regression',
        'clustering_analysis'
      ]
    };
  },
  methods: {
    isColumnSelected(column) {
      return this.selectedColumns.includes(column);
    },
    
    toggleColumnSelection(event, column, index) {
      // 双重验证
      if (!this.selectableMethods.includes(this.currentMethod)) {
        return;
      }
      
      this.$emit('toggleColumnSelection', { event, column, index });
    },
    
    handleNewColumnNamesUpdate({ index, value }) {
      this.$emit('update:newColumnNames', { index, value });
    },
    clearSelectedColumns(){
      this.$emit('clearSelectedColumns');
    }
  }
}
</script>

<style scoped>
.column-add-header-container {
  display: flex;
  gap: 0;
  flex: 1;
}

.column-list-section {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-top: 1px solid #ededed;
}

.column-list-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.column-list-section p {
  margin-bottom: 5px;
}

.column-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
  overflow-y: auto;
}

.column-item {
  padding: 8px 12px;
  cursor: default;
  border-radius: 4px;
  margin-bottom: 4px;
  transition: all 0.3s;
  color: #606266;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  background-color: #f5f7fa;
  font-size: 14px;
}

.column-item:last-child {
  border-bottom: none;
}

.column-item.clickable {
  cursor: pointer;
  user-select: none;
}

.column-item.clickable:hover {
  background-color: #e1e1e1;
}

.column-item.selected {
  background-color: #409eff;
  color: white;
}

.choose-file{
  display: flex;
  align-items: center;
  justify-content: center;
}

.header{
  display: flex;
  justify-content: space-between;
}
</style>