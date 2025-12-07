<template>
  <div v-if="selectedFile && selectedFileColumns.length > 0" class="column-add-header-container">
    <!-- 列名列表区域 -->
    <div class="column-list-section">
      <div v-if="['missing_value_interpolation'].includes(currentMethod)">
        <h3>选择需要处理的列</h3>
        <p>点击选择列，支持 Ctrl/Shift 多选</p>
        <p>不选则处理所有列</p>
      </div>
      <div v-else-if="['data_transformation','delete_columns'].includes(currentMethod)">
        <h3>选择需要处理的列</h3>
        <p>点击选择列，支持 Ctrl/Shift 多选</p>
      </div>
      <div v-else-if="['statistical_summary','correlation_analysis'].includes(currentMethod)">
        <h3>选择需要分析的列</h3>
        <p>点击选择列，支持 Ctrl/Shift 多选</p>
        <p>不选则分析所有数值型列</p>
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
              clickable: ['missing_value_interpolation','delete_columns', 'data_transformation', 'statistical_summary', 'correlation_analysis'].includes(currentMethod)
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
      :remove-duplicates="removeDuplicates"
      :remove-duplicates-cols="removeDuplicatesCols"
      :remove-constant-cols="removeConstantCols"
      :row-missing-threshold="rowMissingThreshold"
      :column-missing-threshold="columnMissingThreshold"
      @update:removeDuplicates="$emit('update:removeDuplicates', $event)"
      @update:removeDuplicatesCols="$emit('update:removeDuplicatesCols', $event)"
      @update:removeConstantCols="$emit('update:removeConstantCols', $event)"
      @update:rowMissingThreshold="$emit('update:rowMissingThreshold', $event)"
      @update:columnMissingThreshold="$emit('update:columnMissingThreshold', $event)"
    />

    <MissingValueInterpolationConfig
      v-else-if="currentMethod === 'missing_value_interpolation'"
      :interpolation-method="interpolationMethod"
      :fill-value="fillValue"
      :knn-neighbors="knnNeighbors"
      @update:interpolationMethod="$emit('update:interpolationMethod', $event)"
      @update:fillValue="$emit('update:fillValue', $event)"
      @update:knnNeighbors="$emit('update:knnNeighbors', $event)"
    />

    <DataTransformationConfig
      v-else-if="currentMethod === 'data_transformation'"
      :selected-file-columns="selectedFileColumns"
      :selected-columns="selectedColumns"
      :data-transformation-config="dataTransformationConfig"
      @update:dataTransformationConfig="$emit('update:dataTransformationConfig', $event)"
    />

    <CorrelationAnalysisConfig
      v-else-if="currentMethod === 'correlation_analysis'"
      :correlation-method="correlationMethod"
      @update:correlationMethod="$emit('update:correlationMethod', $event)"
    />
  </div>
</template>

<script>
import AddHeaderConfig from "./AddHeaderConfig.vue";
import InvalidSamplesConfig from "./InvalidSamplesConfig.vue";
import MissingValueInterpolationConfig from "./MissingValueInterpolationConfig.vue";
import DataTransformationConfig from "./DataTransformationConfig.vue";
import CorrelationAnalysisConfig from "./CorrelationAnalysisConfig.vue";

export default {
  name: "MethodParameterConfig",
  components: {
    AddHeaderConfig,
    InvalidSamplesConfig,
    MissingValueInterpolationConfig,
    DataTransformationConfig,
    CorrelationAnalysisConfig
  },
  props: {
    currentMethod: {
      type: String,
      required: true
    },
    selectedFile: {
      type: String,
      required: true
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
    removeDuplicates: {
      type: Boolean,
      default: false
    },
    removeDuplicatesCols: {
      type: Boolean,
      default: false
    },
    removeConstantCols: {
      type: Boolean,
      default: false
    },
    rowMissingThreshold: {
      type: Number,
      default: 1
    },
    columnMissingThreshold: {
      type: Number,
      default: 1
    },
    interpolationMethod: {
      type: String,
      default: 'linear'
    },
    fillValue: {
      type: String,
      default: ''
    },
    knnNeighbors: {
      type: Number,
      default: 5
    },
    lastSelectedColumnIndex: {
      type: Number,
      default: -1
    },
    dataTransformationConfig: {
      type: Object,
      default: () => ({})
    },
    correlationMethod: {
      type: String,
      default: 'pearson'
    }
  },
  emits: [
    'update:removeDuplicates',
    'update:removeDuplicatesCols',
    'update:removeConstantCols',
    'update:rowMissingThreshold',
    'update:columnMissingThreshold',
    'update:interpolationMethod',
    'update:fillValue',
    'update:knnNeighbors',
    'update:newColumnNames',
    'update:dataTransformationConfig',
    'update:correlationMethod',
    'toggleColumnSelection'
  ],
  methods: {
    isColumnSelected(column) {
      return this.selectedColumns.includes(column);
    },
    
    toggleColumnSelection(event, column, index) {
      // 双重验证
      const selectableMethods = [
        'missing_value_interpolation', 
        'delete_columns', 
        'data_transformation', 
        'statistical_summary',
        'correlation_analysis'
      ];

      if (!selectableMethods.includes(this.currentMethod)) {
        return;
      }
      
      this.$emit('toggleColumnSelection', { event, column, index });
    },
    
    handleNewColumnNamesUpdate({ index, value }) {
      this.$emit('update:newColumnNames', { index, value });
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

.param-config-section {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.default-config-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
}
</style>