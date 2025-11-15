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
      
      <div class="data-info">
        <h2>数据文档名称</h2>
        <div class="data-info-content">
          <input type="text" v-model="documentName" placeholder="请输入文档名称">
          <p>当前样本量：<span>{{ totalRows }}</span></p>
        </div>
      </div>
      
      <div class="preview-section" v-if="!loading">
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
            <button 
              v-for="page in Math.min(3, totalPages)" 
              :key="page" 
              :class="{ active: currentPage === page }"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
            <span v-if="totalPages > 3">...</span>
            <button 
              v-if="totalPages > 3"
              :class="{ active: currentPage === totalPages }"
              @click="changePage(totalPages)"
            >
              {{ totalPages }}
            </button>
          </template>
          <button @click="nextPage" :disabled="currentPage === totalPages">&gt;</button>
        </div>
        
        <div class="operation-buttons">
          <button class="hollow-button previous-page" @click="goBack">上一步</button>
          <button class="blue-button jin" @click="enterAnalysis">进入分析</button>
        </div>
      </div>
      
      <div class="loading-section" v-else>
        <div class="loading-spinner">加载中...</div>
      </div>
    </div>
    
    <!-- 删除确认弹窗 -->
    <div class="danger-window" v-if="showDeleteConfirm">
      <div class="danger-box">
        <div class="top-header">
          <h2>提示</h2>
          <button class="icon-button inputno" @click="cancelDelete"></button>
        </div>
        <div class="ml36">
          <h3 class="warning">是否确定删除？</h3>
          <p>数据删除后不能恢复，请确认！</p>
        </div>
        <div>
          <button class="red-button inputyes" @click="confirmDelete">删除</button>
          <button class="noborder-button inputno" @click="cancelDelete">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Preview',
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
    displayedRows() {
      return this.rowData
    },
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
        // 这里应该调用后端API获取数据
        // 暂时使用示例数据
        const response = await fetch(`http://localhost:8000/data/${this.dataId}?page=${this.currentPage}&page_size=${this.pageSize}`, {
          credentials: 'include' // 包含cookies，用于session管理
        })
        
        if (response.ok) {
          const result = await response.json()
          if (result.success) {
            this.columnHeaders = result.data.columns
            this.rowData = result.data.data
            this.totalRows = result.data.rows
            this.totalPages = result.data.total_pages
            this.documentName = this.dataId  // 使用原始文件名作为文档名
          } else {
            this.useSampleData()
          }
        } else {
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
      this.columnHeaders = ['编号', '姓名', '年龄', '性别', '学历', '收入', '日期']
      this.rowData = []
      for (let i = 1; i <= 30; i++) {
        this.rowData.push({
          '编号': i,
          '姓名': `姓名${i}`,
          '年龄': 20 + (i % 50),
          '性别': i % 2 === 0 ? '男' : '女',
          '学历': ['本科', '硕士', '博士'][(i % 3)],
          '收入': 5000 + (i * 100),
          '日期': `2021/8/${1 + (i % 30)}`
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
    
    uploadMore() {
      this.$router.push('/upload')
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
        const response = await fetch(`http://localhost:8000/data/${this.dataId}`, {
          method: 'DELETE',
          credentials: 'include' // 包含cookies，用于session管理
        });
        
        if (response.ok) {
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
        } else {
          console.error('删除请求失败，状态码:', response.status);
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
  background-color: #f5f5f5;
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
  background: white;
  padding: 15px;
  border-radius: 6px;
  box-shadow: 0 1px 6px 0 rgba(0, 0, 0, 0.1);
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

.data-info-content input {
  flex: 1;
  padding: 8px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 13px;
}

.data-info-content p {
  color: #606266;
  font-size: 13px;
}

.data-info-content p span {
  font-weight: bold;
  color: #409eff;
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

.danger-window {
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

.danger-box {
  background: white;
  border-radius: 6px;
  width: 350px;
  padding: 15px;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.top-header h2 {
  font-size: 16px;
  color: #303133;
}

.icon-button {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #909399;
}

.ml36 {
  margin-left: 30px;
  margin-bottom: 15px;
}

.ml36 .warning {
  color: #e6a23c;
  font-size: 14px;
  margin-bottom: 8px;
}

.ml36 p {
  color: #606266;
  font-size: 13px;
}

.red-button {
  padding: 8px 16px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 8px;
  font-size: 13px;
}

.red-button:hover {
  background-color: #f78989;
}

.noborder-button {
  padding: 8px 16px;
  background: none;
  color: #606266;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
}

.noborder-button:hover {
  color: #409eff;
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
  
  .preview-section {
    padding: 10px;
  }
  
  .data-info-content {
    padding: 10px;
  }
  
  .upload-steps {
    padding: 10px;
  }
}
</style>