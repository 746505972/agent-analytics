<template>
  <div class="method-selection-section">
    <div class="method-categories">
      <div 
        v-for="category in methodCategories" 
        :key="category.id"
        class="method-category"
        :class="{ active: expandedCategories.includes(category.id) }"
      >
        <div class="category-header" @click="toggleCategory(category.id)">
          <h4>{{ category.name }}</h4>
          <span class="toggle-icon">{{ expandedCategories.includes(category.id) ? '−' : '+' }}</span>
        </div>
        <div v-show="expandedCategories.includes(category.id)" class="category-methods">
          <button 
            v-for="method in category.methods" 
            :key="method.id"
            :class="{ active: currentMethod === method.id }"
            @click="selectMethod(method.id)"
            class="method-tab"
          >
            {{ method.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MethodSelection",
  props: {
    methodCategories: {
      type: Array,
      required: true
    },
    currentMethod: {
      type: String,
      required: true
    },
    expandedCategories: {
      type: Array,
      required: true
    }
  },
  emits: ['select-method', 'toggle-category'],
  methods: {
    selectMethod(methodId) {
      this.$emit('select-method', methodId);
    },
    toggleCategory(categoryId) {
      this.$emit('toggle-category', categoryId);
    }
  }
}
</script>

<style scoped>
.method-selection-section {
  background: white;
  padding-top: 10px;
  margin-bottom: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.method-selection-section h3 {
  margin-top: 0;
  padding-left: 10px;
  padding-bottom: 10px;
  margin-bottom: 10px;
  color: #303133;
}

.method-categories {
  margin-bottom: 15px;
}

.method-category {
  margin-bottom: 10px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  background-color: #f5f7fa;
}

.method-category.active .category-header {
  background-color: #ecf5ff;
}

.category-header h4 {
  margin: 0;
  color: #303133;
}

.toggle-icon {
  font-size: 18px;
  font-weight: bold;
  color: #909399;
  user-select: none;
}

.category-methods {
  padding: 5px 7px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
}

.method-tab {
  padding: 8px 5px;
  background-color: #f5f7fa;
  border: 1px solid #f5f7fa;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
  word-break: break-word;
  display: flex;
  align-items: center;
  justify-content: center;
}

.method-tab:hover {
  background-color: #ecf5ff;
  border-color: #409eff;
}

.method-tab.active {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}
</style>