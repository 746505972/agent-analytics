<template>
  <div class="preview-container">
    <div class="indexheader">
      <div class="inner">
        <div class="header-left">
          <a href="javascript:void(0)" class="back-link" @click="showDeleteConfirmation">
            <span>返回</span>
          </a>
        </div>
        <div class="header-right">
          <router-link class="hollow-button" to="/dashboard" @click.native="enterAnalysisFromHeader">
            进入分析
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="main-content">
      <div class="upload-steps">
        <div class="step-item completed-step">
          <span><i class="icon-checkmark"></i></span>
          上传文件
        </div>
        <hr>
        <div class="step-item active-step">
          <span>2</span>
          数据预览
        </div>
      </div>
      <div class="preview-section">
        <DataPreview
          v-if="!loading"
          :column-headers="columnHeaders"
          :row-data="rowData"
          :total-rows="totalRows"
          :total-pages="totalPages"
          :current-page="currentPage"
          :header-width="headerWidth"
          :document-name="documentName"
          @prev-page="prevPage"
          @next-page="nextPage"
          @change-page="changePage"
        />
        <div class="loading-section" v-else>
          <div class="loading-spinner">加载中...</div>
        </div>
        <div class="operation-buttons">
          <button class="hollow-button previous-page" @click="goBack">上一步</button>
          <button class="blue-button jin" @click="enterAnalysis">进入分析</button>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <DeleteConfirmationModal 
      :visible="showDeleteConfirm"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script>
import DataPreview from '@/components/DataPreview.vue';
import DeleteConfirmationModal from '@/components/DeleteConfirmationModal.vue';
import {backendBaseUrl} from "@/api/apiConfig";

export default {
  name: 'Preview',
  components: {
    DataPreview,
    DeleteConfirmationModal
  },
  data() {
    return {
      documentName: '数据分析示例文档',
      isTextFormat: true,
      currentPage: 1,
      pageSize: 10,
      showDeleteConfirm: false,
      loading: true,
      
      // 数据相关
      dataId: '',
      columnHeaders: [],
      rowData: [],
      totalRows: 0,
      totalPages: 0,
      
      // 添加一个标志，用于标识是否确认离开
      isLeaving: false,
      // 添加一个标志，用于标识是否要进入分析页面
      isEnteringAnalysis: false
    }
  },
  computed: {
    headerWidth() {
      return this.columnHeaders.length > 0 ? `${100 / this.columnHeaders.length}%` : '100px'
    }
  },
  async mounted() {
    // 从路由参数或本地存储获取dataId
    this.dataId = this.$route.query.dataId || localStorage.getItem('currentDataId')
    if (this.dataId) {
      await this.loadData()
    } else {
      // 如果没有dataId，使用示例数据
      this.useSampleData()
    }
  },
  // 添加路由守卫钩子
  beforeRouteLeave(to, from, next) {
    // 如果已经确认离开，则直接离开
    if (this.isLeaving) {
      next();
      return;
    }
    
    // 如果是要进入分析页面，则不显示删除确认弹窗
    if (this.isEnteringAnalysis) {
      next();
      return;
    }
    
    // 显示删除确认弹窗
    this.showDeleteConfirmation();
    // 阻止默认的路由跳转
    next(false);
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        // 调用后端API获取数据
        const response = await fetch(`${backendBaseUrl}/data/${this.dataId}?page=${this.currentPage}&page_size=${this.pageSize}`, {
          credentials: 'include' // 包含cookies，用于session管理
        })

        const result = await response.json()
        if (result.success) {
          this.columnHeaders = result.data.columns
          this.rowData = result.data.data
          this.totalRows = result.data.rows
          this.totalPages = result.data.total_pages
          this.documentName = result.data.data_id  // 使用data_id作为文档名
        } else {
          console.error("获取数据失败:", result.error)
          this.useSampleData()
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        this.useSampleData()
      } finally {
        this.loading = false
      }
    },
    
    useSampleData() {
      this.loading = false
      this.columnHeaders = ['示例数据0', '示例数据1', '示例数据2', '示例数据3']
      this.rowData = []
      for (let i = 1; i <= 30; i++) {
        this.rowData.push({
          '示例数据0': '示例数据',
          '示例数据1': '示例数据',
          '示例数据2': '示例数据',
          '示例数据3': '示例数据',
        })
      }
      this.totalRows = this.rowData.length
      this.totalPages = Math.ceil(this.totalRows / this.pageSize)
      this.documentName = '示例数据文档'
    },
    
    changePage(page) {
      this.currentPage = page
      if (this.dataId) {
        this.loadData()
      }
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.changePage(this.currentPage - 1)
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.changePage(this.currentPage + 1)
      }
    },
    
    // 修改 goBack 方法，显示删除确认弹窗
    goBack() {
      this.showDeleteConfirmation()
    },

    enterAnalysis() {
      this.isEnteringAnalysis = true
      this.$router.push('/dashboard')
    },
    
    enterAnalysisFromHeader() {
      this.isEnteringAnalysis = true
    },
    
    showDeleteConfirmation() {
      this.showDeleteConfirm = true
    },
    
    cancelDelete() {
      this.showDeleteConfirm = false
    },
    
    // 确认删除后真正离开页面
    async confirmDeleteAndLeave() {
      // 调用后端删除API
      try {
        const response = await fetch(`${backendBaseUrl}/data/${this.dataId}`, {
          method: 'DELETE',
          credentials: 'include' // 包含cookies，用于session管理
        });

        const result = await response.json();
        if (result.success) {
          console.log('数据删除成功');
          // 关闭弹窗
          this.showDeleteConfirm = false;
          // 设置离开标志
          this.isLeaving = true;
          // 真正离开页面
          this.$router.go(-1);
        } else {
          console.error('删除失败:', result.error);
        }
      } catch (error) {
        console.error('删除数据时发生错误:', error);
      }
    },
    
    // 修改 confirmDelete 方法，调用新的 confirmDeleteAndLeave
    async confirmDelete() {
      await this.confirmDeleteAndLeave();
    }
  }
}
</script>

<style scoped>
.preview-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.indexheader {
  flex-shrink: 0;
  background-color: #fff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  padding: 10px 0;
}

.inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 15px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 15px auto;
  padding: 0 15px;
  overflow: hidden;
}

.upload-steps {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.header-left .back-link {
  text-decoration: none;
  color: #333;
  font-size: 16px;
}

.header-right .hollow-button {
  display: inline-block;
  padding: 8px 16px;
  border: 1px solid #409eff;
  color: #409eff;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
}

.header-right .hollow-button:hover {
  background-color: #409eff;
  color: white;
}

.step-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #909399;
}

.step-item.completed-step {
  color: #67c23a;
}

.step-item.active-step {
  color: #409eff;
}

.step-item span {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #f5f5f5;
  margin-right: 8px;
  font-weight: bold;
  font-size: 12px;
}

.step-item.completed-step span {
  background-color: #67c23a;
  color: white;
}

.step-item.active-step span {
  background-color: #409eff;
  color: white;
}

.upload-steps hr {
  flex: 1;
  margin: 0 15px;
  border: none;
  height: 1px;
  background-color: #ebeef5;
}

.preview-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 6px 0 rgba(0, 0, 0, 0.1);
  padding: 15px;
  overflow: hidden;
}

.data-info-content p {
  color: #606266;
  font-size: 13px;
  margin-left: 10px;
}

.loading-section {
  flex: 1;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 6px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  font-size: 16px;
  color: #409eff;
}

.operation-buttons {
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.hollow-button {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
  font-size: 13px;
}

.hollow-button:hover {
  border-color: #409eff;
  color: #409eff;
}

.blue-button {
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
}

.blue-button:hover {
  background-color: #66b1ff;
}

@media (max-width: 768px) {
  .inner {
    flex-direction: column;
    gap: 10px;
  }
  
  .upload-steps {
    flex-direction: column;
    gap: 10px;
  }
  
  .upload-steps hr {
    width: 100%;
  }

  .operation-buttons {
    flex-direction: column;
    gap: 10px;
  }

  .operation-buttons button {
    width: 100%;
  }
  
  .main-content {
    margin: 10px auto;
    padding: 0 10px;
  }

  .upload-steps {
    padding: 10px;
  }
}
</style>