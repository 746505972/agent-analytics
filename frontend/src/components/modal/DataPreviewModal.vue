<template>
  <div class="preview-modal">
    <div class="preview-modal-content">
      <div class="preview-header">
        <h3>数据预览</h3>
        <button class="close-button" @click="closeModal">×</button>
      </div>
      <div class="preview-body">
        <div class="data-info">
          <div class="data-info-content">
            <span class="document-name">{{ previewData.documentName }}</span>
            <p>当前样本量：<span>{{ previewData.totalRows }}</span></p>
          </div>
        </div>
        
        <div class="preview-section" v-if="!previewData.loading">
          <div class="preview-top">
            <h3>数据预览如下<p>（共<span>{{ previewData.totalRows }}</span>行）</p></h3>
          </div>
          
          <div class="preview-wrap">
            <table class="preview-table">
              <thead>
                <tr>
                  <th v-for="(header, index) in previewData.columnHeaders" :key="index">
                    {{ header }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, rowIndex) in previewData.displayedRows" :key="rowIndex">
                  <td v-for="(header, cellIndex) in previewData.columnHeaders" :key="cellIndex" :title="row[header]">
                    {{ row[header] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="pagination" v-if="previewData.totalPages > 1">
            <button @click="prevPage" :disabled="previewData.currentPage === 1">&lt;</button>
            <template v-if="previewData.totalPages <= 5">
              <button 
                v-for="page in previewData.totalPages" 
                :key="page" 
                :class="{ active: previewData.currentPage === page }"
                @click="changePage(page)"
              >
                {{ page }}
              </button>
            </template>
            <template v-else>
              <button 
                v-for="page in Math.min(3, previewData.totalPages)" 
                :key="page" 
                :class="{ active: previewData.currentPage === page }"
                @click="changePage(page)"
              >
                {{ page }}
              </button>
              <span v-if="previewData.totalPages > 3">...</span>
              <button 
                v-if="previewData.totalPages > 3"
                :class="{ active: previewData.currentPage === previewData.totalPages }"
                @click="changePage(previewData.totalPages)"
              >
                {{ previewData.totalPages }}
              </button>
            </template>
            <button @click="nextPage" :disabled="previewData.currentPage === previewData.totalPages">&gt;</button>
          </div>
        </div>
        
        <div class="loading-section" v-else>
          <div class="loading-spinner">加载中...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataPreviewModal",
  props: {
    previewData: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'change-page'],
  methods: {
    closeModal() {
      this.$emit('close');
    },
    changePage(page) {
      this.$emit('change-page', page);
    },
    prevPage() {
      if (this.previewData.currentPage > 1) {
        this.$emit('change-page', this.previewData.currentPage - 1);
      }
    },
    nextPage() {
      if (this.previewData.currentPage < this.previewData.totalPages) {
        this.$emit('change-page', this.previewData.currentPage + 1);
      }
    }
  }
}
</script>

<style scoped>
/* 数据预览弹窗样式 */
.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.preview-modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.preview-header h3 {
  margin: 0;
  color: #303133;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
}

.preview-body {
  flex: 1;
  padding: 20px;
  overflow: auto;
}

/* 预览部分样式（复用Preview.vue的样式） */
.data-info {
  margin-bottom: 15px;
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

.preview-section {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 6px;
  padding: 15px;
  overflow: hidden;
}

.loading-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px;
}

.loading-spinner {
  font-size: 16px;
  color: #409eff;
}

.preview-top {
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

.preview-wrap {
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
  .preview-modal-content {
    width: 95%;
    height: 95%;
  }
  
  .preview-body {
    padding: 10px;
  }
  
  .preview-top {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .data-info-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>