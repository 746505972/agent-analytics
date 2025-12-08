<template>
  <div class="preview-modal" v-if="visible">
    <div class="preview-modal-content">
      <div class="preview-header">
        <h3>数据预览</h3>
        <button class="close-button" @click="closeModal">×</button>
      </div>
      <div class="preview-body">
        <DataPreview
          v-if="!loading"
          :column-headers="previewData.columnHeaders"
          :row-data="previewData.rowData"
          :total-rows="previewData.totalRows"
          :total-pages="previewData.totalPages"
          :current-page="previewData.currentPage"
          :header-width="previewData.headerWidth"
          :document-name="previewData.documentName"
          @prev-page="prevPage"
          @next-page="nextPage"
          @change-page="changePage"
        />
        <div class="loading-section" v-else>
          <div class="loading-spinner">加载中...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DataPreview from "@/components/DataPreview.vue";

export default {
  name: "PreviewModal",
  components: {
    DataPreview
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    previewData: {
      type: Object,
      default: () => ({
        documentName: '',
        columnHeaders: [],
        rowData: [],
        displayedRows: [],
        totalRows: 0,
        totalPages: 0,
        currentPage: 1,
        pageSize: 10,
        headerWidth: '100px'
      })
    }
  },
  emits: ['close', 'prev-page', 'next-page', 'change-page'],
  methods: {
    closeModal() {
      this.$emit('close');
    },
    prevPage() {
      this.$emit('prev-page');
    },
    nextPage() {
      this.$emit('next-page');
    },
    changePage(page) {
      this.$emit('change-page', page);
    }
  }
}
</script>

<style scoped>
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

@media (max-width: 768px) {
  .preview-modal-content {
    width: 95%;
    height: 95%;
  }
  
  .preview-body {
    padding: 10px;
  }
}
</style>