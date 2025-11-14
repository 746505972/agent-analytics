<template>
  <div class="preview-container">
    <div class="indexheader">
      <div class="inner">
        <div class="header-left">
          <router-link to="/upload" class="back-link">
            <span>返回</span>
          </router-link>
        </div>
        <div class="header-right">
          <router-link class="hollow-button" to="/analysis">
            进入SPSSAU
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
          <label>
            <input class="btn-text-change" type="checkbox" v-model="isTextFormat" checked>文字格式
          </label>
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
          <button 
            v-for="page in totalPages" 
            :key="page" 
            :class="{ active: currentPage === page }"
            @click="changePage(page)"
          >
            {{ page }}
          </button>
        </div>
        
        <div class="operation-buttons">
          <button class="hollow-button previous-page" @click="goBack">上一步</button>
          <button class="hollow-button updata" @click="uploadMore">继续上传</button>
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
      totalPages: 0
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
  methods: {
    async loadData() {
      this.loading = true
      try {
        // 这里应该调用后端API获取数据
        // 暂时使用示例数据
        const response = await fetch(`http://localhost:8000/data/${this.dataId}?page=${this.currentPage}&page_size=${this.pageSize}`)
        
        if (response.ok) {
          const result = await response.json()
          if (result.success) {
            this.columnHeaders = result.data.columns
            this.rowData = result.data.data
            this.totalRows = result.data.rows
            this.totalPages = result.data.total_pages
            this.documentName = `数据文档-${this.dataId}`
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
      this.rowData = [
        { '编号': '1', '姓名': '张三', '年龄': '28', '性别': '男', '学历': '本科', '收入': '8000', '日期': '2021/8/12' },
        { '编号': '2', '姓名': '李四', '年龄': '32', '性别': '女', '学历': '硕士', '收入': '12000', '日期': '2021/8/13' },
        { '编号': '3', '姓名': '王五', '年龄': '45', '性别': '男', '学历': '博士', '收入': '20000', '日期': '2021/8/14' },
        { '编号': '4', '姓名': '赵六', '年龄': '29', '性别': '女', '学历': '本科', '收入': '9500', '日期': '2021/8/15' },
        { '编号': '5', '姓名': '钱七', '年龄': '37', '性别': '男', '学历': '硕士', '收入': '15000', '日期': '2021/8/16' },
        { '编号': '6', '姓名': '孙八', '年龄': '26', '性别': '女', '学历': '本科', '收入': '7800', '日期': '2021/8/17' },
        { '编号': '7', '姓名': '周九', '年龄': '40', '性别': '男', '学历': '博士', '收入': '18000', '日期': '2021/8/18' },
        { '编号': '8', '姓名': '吴十', '年龄': '24', '性别': '女', '学历': '硕士', '收入': '11000', '日期': '2021/8/19' },
        { '编号': '9', '姓名': '郑一', '年龄': '33', '性别': '男', '学历': '本科', '收入': '10000', '日期': '2021/8/20' },
        { '编号': '10', '姓名': '王二', '年龄': '31', '性别': '女', '学历': '博士', '收入': '13000', '日期': '2021/8/21' }
      ]
      this.totalRows = this.rowData.length
      this.totalPages = 1
      this.documentName = '示例数据文档'
    },
    
    changePage(page) {
      this.currentPage = page
      if (this.dataId) {
        this.loadData()
      }
    },
    
    goBack() {
      this.$router.push('/upload')
    },
    
    uploadMore() {
      this.$router.push('/upload')
    },
    
    enterAnalysis() {
      this.$router.push('/analysis')
    },
    
    showDeleteConfirmation() {
      this.showDeleteConfirm = true
    },
    
    cancelDelete() {
      this.showDeleteConfirm = false
    },
    
    confirmDelete() {
      // 实际项目中这里应该调用删除API
      console.log('删除数据')
      this.showDeleteConfirm = false
    }
  }
}
</script>

<style scoped>
.preview-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.indexheader {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 15px 0;
}

.inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
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

.main-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}

.upload-steps {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.step-item {
  display: flex;
  align-items: center;
  font-size: 16px;
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
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #f5f5f5;
  margin-right: 10px;
  font-weight: bold;
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
  margin: 0 20px;
  border: none;
  height: 1px;
  background-color: #ebeef5;
}

.data-info h2 {
  font-size: 20px;
  color: #303133;
  margin-bottom: 15px;
}

.data-info-content {
  display: flex;
  align-items: center;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.data-info-content input {
  flex: 1;
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.data-info-content p {
  color: #606266;
  font-size: 14px;
}

.data-info-content p span {
  font-weight: bold;
  color: #409eff;
}

.preview-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  padding: 20px;
}

.loading-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  padding: 50px;
  text-align: center;
}

.loading-spinner {
  font-size: 18px;
  color: #409eff;
}

.preview-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.preview-top h3 {
  font-size: 18px;
  color: #303133;
}

.preview-top h3 p {
  display: inline;
  font-size: 14px;
  color: #606266;
  margin-left: 10px;
}

.preview-top h3 p span {
  font-weight: bold;
}

.preview-top label {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
}

.preview-wrap {
  overflow: auto;
  margin-bottom: 20px;
  max-height: calc(100vh - 365px);
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
}

.preview-table th,
.preview-table td {
  padding: 12px 15px;
  text-align: left;
  border: 1px solid #ebeef5;
  white-space: nowrap;
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
  gap: 10px;
  margin-bottom: 20px;
}

.pagination button {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination button.active,
.pagination button:hover {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.operation-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.hollow-button {
  padding: 10px 20px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
}

.hollow-button:hover {
  border-color: #409eff;
  color: #409eff;
}

.blue-button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
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
  border-radius: 8px;
  width: 400px;
  padding: 20px;
}

.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.top-header h2 {
  font-size: 18px;
  color: #303133;
}

.icon-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.ml36 {
  margin-left: 36px;
  margin-bottom: 20px;
}

.ml36 .warning {
  color: #e6a23c;
  font-size: 16px;
  margin-bottom: 10px;
}

.ml36 p {
  color: #606266;
  font-size: 14px;
}

.red-button {
  padding: 10px 20px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 10px;
}

.red-button:hover {
  background-color: #f78989;
}

.noborder-button {
  padding: 10px 20px;
  background: none;
  color: #606266;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.noborder-button:hover {
  color: #409eff;
}

@media (max-width: 768px) {
  .inner {
    flex-direction: column;
    gap: 15px;
  }
  
  .upload-steps {
    flex-direction: column;
    gap: 15px;
  }
  
  .upload-steps hr {
    width: 100%;
  }
  
  .data-info-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .preview-top {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .operation-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .operation-buttons button {
    width: 100%;
  }
}
</style>