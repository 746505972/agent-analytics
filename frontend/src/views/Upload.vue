<template>
  <div class="upload-container">
    <div class="indexheader">
      <div class="inner">
        <div class="header-left">
          <Icon />
        </div>
        <div class="header-right">
          <router-link class="hollow-button" to="/dashboard">
            进入分析
          </router-link>
        </div>
      </div>
    </div>
    
    <div class="upload-box">
      <div class="upload-steps">
        <div class="step-item active-step">
          <span>1</span>
          上传文件
        </div>
        <hr>
        <div class="step-item">
          <span>2</span>
          数据预览
        </div>
      </div>
      
      <div class="upload-section">
        <FileUploader @file-selected="handleFileSelect" @file-error="handleFileError" />
        <DBConnector v-model:db-config="dbConfig" @connect-db="connectToDatabase"/>
      </div>
      <ChartsExample />
    </div>

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">文件上传中...</div>
    </div>

    <UploadError v-if="uploadError" @close="clearError">
      {{ uploadError }}
    </UploadError>
  </div>
</template>

<script>
import FileUploader from '@/components/FileUploader.vue';
import ChartsExample from "@/components/ChartsExample.vue";
import Icon from "@/components/Icon.vue";
import UploadError from "@/components/UploadError.vue";
import DBConnector from "@/components/DBConnector.vue";
import { encryptPassword } from '@/utils/cryptoUtils';

export default {
  name: 'Upload',
  components: {
    DBConnector,
    UploadError,
    Icon,
    FileUploader,
    ChartsExample
  },
  data() {
    return {
      isLoading: false,
      selectedFile: null,
      uploadError: null,
      dbConfig: {
        type: 'mysql',
        host: '',
        port: '',
        username: '',
        password: '',
        database: '',
        table: ''
      }
    }
  },
  methods: {
    handleFileSelect(file) {
      this.selectedFile = file
      this.uploadFile(file)
    },
    
    handleFileError(errorMessage) {
      this.uploadError = errorMessage
    },

    async uploadFile(file) {
      // 文件大小检查 (1000MB)
      if (file.size > 1000 * 1024 * 1024) {
        this.uploadError = '文件大小超过1000MB限制'
        return
      }

      this.isLoading = true
      this.uploadError = null

      try {
        // 创建 FormData 对象
        const formData = new FormData()
        formData.append('file', file)

        // 发送文件到后端
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData,
          credentials: 'include' // 包含cookies，用于session管理
        })

        const result = await response.json()

        if (result.success) {
          // 保存 data_id 到本地存储
          localStorage.setItem('currentDataId', result.data.data_id)

          // 上传完成后跳转到数据预览页面
          this.$router.push({
            path: '/preview',
            query: { dataId: result.data.data_id }
          })
        } else {
          this.uploadError = result.error || '上传失败'
        }
      } catch (error) {
        console.error('上传文件时出错:', error)
        this.uploadError = '网络错误，请检查后端服务是否运行'
      } finally {
        this.isLoading = false
      }
    },

    async connectToDatabase() {
      this.isLoading = true;
      this.uploadError = null;

      try {
        // 创建数据库配置副本，并对密码进行加密
        const dbConfigToSend = { ...this.dbConfig };
        if (dbConfigToSend.password) {
          dbConfigToSend.password = encryptPassword(dbConfigToSend.password);
        }

        const response = await fetch('/upload/db', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(dbConfigToSend),
          credentials: 'include'
        });

        const result = await response.json();

        if (result.success) {
          // 保存 data_id 到本地存储
          localStorage.setItem('currentDataId', result.data.data_id);

          // 连接成功后跳转到数据预览页面
          this.$router.push({
            path: '/preview',
            query: { dataId: result.data.data_id }
          });
        } else {
          this.uploadError = result.error || '数据库连接失败';
        }
      } catch (error) {
        console.error('连接数据库时出错:', error);
        this.uploadError = '网络错误，请检查后端服务是否运行';
      } finally {
        this.isLoading = false;
      }
    },

    clearError() {
      this.uploadError = null
    }
  }
}
</script>

<style scoped>
.upload-container {
  min-height: 100vh;
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

.upload-box {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 20px;
}

.upload-steps {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.step-item {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #909399;
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

.upload-section {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.upload-instructions {
  flex: 1;
  padding: 20px;
  list-style: none;
}

.upload-instructions li {
  padding: 5px 0;
  color: #606266;
  line-height: 1.6;
}

.upload-instructions h3 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 18px;
}

.loading-overlay {
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

.loading-spinner {
  width: 50px;
  height: 50px;
  color: white;
  font-size: 16px;
}

@media (max-width: 768px) {
  .upload-section {
    flex-direction: column;
  }
  
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
}
</style>