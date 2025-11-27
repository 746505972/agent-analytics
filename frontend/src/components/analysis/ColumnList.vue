<template>
  <div class="column-list-section">
    <div v-if="['missing_value_interpolation','delete_columns'].includes(currentMethod)">
      <h3>选择需要处理的列</h3>
      <p>点击选择列，支持 Ctrl/Shift 多选</p>
      <p>不选则处理所有列</p>
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
            clickable: ['missing_value_interpolation','delete_columns'].includes(currentMethod)
          }"
          @click="toggleColumnSelection($event, column, index)"
      >
        {{ column }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "ColumnList",
  props: {
    currentMethod: {
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
    }
  },
  emits: ['toggle-column'],
  methods: {
    isColumnSelected(column) {
      const interpolationMethods = ['missing_value_interpolation', 'delete_columns'];
      if (!interpolationMethods.includes(this.currentMethod)) {
        return false;
      }
      return this.selectedColumns.includes(column);
    },
    toggleColumnSelection(event, column, index) {
      this.$emit('toggle-column', { event, column, index });
    }
  }
}
</script>

<style scoped>
.column-list-section {
  background: white;
  padding: 20px;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);*/
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
  border-bottom: 1px solid #ebeef5;
  color: #606266;
}

.column-item:last-child {
  border-bottom: none;
}

.column-item {
  padding: 8px 12px;
  cursor: default;
  border-radius: 4px;
  margin-bottom: 4px;
  transition: all 0.3s;
}

.column-item.clickable {
  cursor: pointer;
}

.column-item.clickable:hover {
  background-color: #f0f0f0;
}

.column-item.selected {
  background-color: #409eff;
  color: white;
}
</style>