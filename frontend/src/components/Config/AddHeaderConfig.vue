<template>
  <div class="param-config-section">
    <h3>设置列名</h3>
    <div class="add-header-content">
      <div class="column-inputs">
        <div 
          v-for="(column, index) in selectedFileColumns" 
          :key="index" 
          class="column-input-item"
        >
          <input 
            :id="'column-' + index"
            :value="newColumnNames[index]" 
            @input="$emit('update:newColumnNames', {index, value: $event.target.value})"
            :placeholder="'列' + (index + 1)"
            type="text"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddHeaderConfig",
  props: {
    selectedFileColumns: {
      type: Array,
      default: () => []
    },
    newColumnNames: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:newColumnNames'],
  watch: {
    // 监听selectedFileColumns的变化，确保在首次选择修改模式时能正确填充
    selectedFileColumns: {
      handler(newVal) {
        // 当selectedFileColumns发生变化时，什么都不做，只是通知父组件
        // 父组件会根据模式决定如何处理newColumnNames
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.param-config-section {
  background: white;
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.param-config-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.add-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.column-inputs {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.column-input-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
  margin-bottom: 0;
}

.column-input-item label {
  width: 100px;
  margin-right: 10px;
  color: #606266;
}

.column-input-item input {
  flex: 1;
  padding: 8px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
}
</style>