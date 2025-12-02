<template>
<div class="data-info">
    <div class="data-info-content">
      <span class="document-name">{{ documentName }}</span>
      <p>当前样本量：<span>{{ totalRows }}</span></p>
    </div>
</div>
<div class="preview-top">
  <h3>数据预览如下<p>（共<span>{{ totalRows }}</span>行）</p></h3>
</div>

<div class="preview-wrap">
  <table class="preview-table">
    <thead>
      <tr>
        <th v-for="(header, index) in columnHeaders" :key="index" :style="{ minWidth: headerWidth }">
          {{ header }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, rowIndex) in displayedRows" :key="rowIndex">
        <td v-for="(header, cellIndex) in columnHeaders" :key="cellIndex" :title="row[header]">
          {{ row[header] }}
        </td>
      </tr>
    </tbody>
  </table>
</div>

<div class="pagination" v-if="totalPages > 1">
  <button @click="prevPage" :disabled="currentPage === 1">&lt;</button>
  <template v-if="totalPages <= 5">
    <button
      v-for="page in totalPages"
      :key="page"
      :class="{ active: currentPage === page }"
      @click="changePage(page)"
    >
      {{ page }}
    </button>
  </template>
  <template v-else>
    <!-- 第一页 -->
    <button
      :class="{ active: currentPage === 1 }"
      @click="changePage(1)"
    >
      1
    </button>
    
    <!-- 前省略号 -->
    <span v-if="currentPage > 4">...</span>
    
    <!-- 当前页前后各两页 -->
    <button
      v-for="page in getPageRange()"
      :key="page"
      :class="{ active: currentPage === page }"
      @click="changePage(page)"
    >
      {{ page }}
    </button>
    
    <!-- 后省略号 -->
    <span v-if="currentPage < totalPages - 3">...</span>
    
    <!-- 最后一页 -->
    <button
      v-if="totalPages > 1"
      :class="{ active: currentPage === totalPages }"
      @click="changePage(totalPages)"
    >
      {{ totalPages }}
    </button>
  </template>
  <button @click="nextPage" :disabled="currentPage === totalPages">&gt;</button>
</div>
</template>

<script>
export default {
  name: 'DataPreview',
  props: {
    columnHeaders: {
      type: Array,
      default: () => []
    },
    rowData: {
      type: Array,
      default: () => []
    },
    totalRows: {
      type: Number,
      default: 0
    },
    totalPages: {
      type: Number,
      default: 0
    },
    currentPage: {
      type: Number,
      default: 1
    },
    headerWidth: {
      type: String,
      default: '100px'
    },
    documentName: {
      type: String,
      default: '数据分析示例文档'
    }
  },
  emits: ['prev-page', 'next-page', 'change-page', 'go-back', 'enter-analysis'],
  computed: {
    displayedRows() {
      return this.rowData
    }
  },
  methods: {
    prevPage() {
      this.$emit('prev-page')
    },
    nextPage() {
      this.$emit('next-page')
    },
    changePage(page) {
      this.$emit('change-page', page)
    },
    goBack() {
      this.$emit('go-back')
    },
    enterAnalysis() {
      this.$emit('enter-analysis')
    },
    getPageRange() {
      const pages = [];
      const start = Math.max(2, this.currentPage - 2);
      const end = Math.min(this.totalPages - 1, this.currentPage + 2);
      
      for (let i = start; i <= end; i++) {
        // 只有当不是第一页或最后一页时才添加
        if (i !== 1 && i !== this.totalPages) {
          pages.push(i);
        }
      }
      
      return pages;
    }
  }
}
</script>

<style scoped>

.data-info {
  flex-shrink: 0;
}

.data-info h2 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 10px;
}

.data-info-content {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px;
  border-radius: 6px;
}

.document-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  flex: 1;
}

.data-info-content p {
  color: #606266;
  font-size: 13px;
  margin-left: 10px;
}

.preview-top {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.preview-top h3 {
  font-size: 16px;
  color: #303133;
}

.preview-top h3 p {
  display: inline;
  font-size: 13px;
  color: #606266;
  margin-left: 8px;
}

.preview-top h3 p span {
  font-weight: bold;
}

.preview-top label {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-size: 13px;
  cursor: pointer;
}

.preview-wrap {
  flex: 1;
  overflow: auto;
  margin-bottom: 15px;
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
}

.preview-table th,
.preview-table td {
  padding: 8px 10px;
  text-align: left;
  border: 1px solid #ebeef5;
  white-space: nowrap;
  font-size: 13px;
}

.preview-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #606266;
  position: sticky;
  top: 0;
}

.preview-table tbody tr:hover {
  background-color: #f5f7fa;
}

.pagination {
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 15px;
}

.pagination button {
  padding: 6px 10px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button.active,
.pagination button:hover:not(:disabled) {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

@media (max-width: 768px) {
  .data-info-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .preview-top {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }


}
</style>