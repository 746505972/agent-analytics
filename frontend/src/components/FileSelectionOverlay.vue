<template>
  <div class="file-selection-overlay" v-click-outside="closeFileSelection">
    <div class="file-selection-content">
      <div class="file-list-container">
        <div v-if="files.length === 0" class="no-files">
          暂无上传文件，请先上传文件
        </div>
        <div v-else class="file-list">
          <div 
            v-for="file in files" 
            :key="file.data_id"
            class="file-item"
            :class="{ selected: selectedFile === file.data_id }"
            @click="selectFile(file.data_id)"
          >
            <div class="file-name">
              {{ file.filename }}
              <span class="delete-file" @click.stop="deleteFile(file.data_id)">×</span>
            </div>
            <div class="file-info">
              <span>行数: {{ file.rows }}</span>
              <span>列数: {{ file.columns }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="file-actions">
        <router-link to="/upload" class="upload-button">上传新文件</router-link>
      </div>
      <!-- 添加查看数据链接 -->
      <div v-if="selectedFile" class="file-actions-container">
        <div class="view-data-link" @click="showDataPreview">
          查看数据
        </div>
        <div class="download-file-link" @click="downloadFile">
          下载文件
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FileSelectionOverlay",
  props: {
    files: {
      type: Array,
      required: true
    },
    selectedFile: {
      type: String,
      default: null
    }
  },
  emits: ['select-file', 'delete-file', 'close', 'show-preview', 'download-file'],
  directives: {
    clickOutside: {
      mounted(el, binding, vnode) {
        // 确保元素已经被添加到DOM中
        setTimeout(() => {
          el.clickOutsideEvent = function(event) {
            // 检查点击的元素是否在当前元素内部
            if (!(el === event.target || el.contains(event.target))) {
              // 检查绑定的值是否为函数
              const handler = binding.value;
              if (typeof handler === 'function') {
                // 调用绑定的方法
                handler(event);
              }
            }
          };
          // 将事件监听器添加到 document 上
          document.addEventListener('click', el.clickOutsideEvent);
        }, 0);
      },
      unmounted(el) {
        // 解除事件监听器
        if (el.clickOutsideEvent) {
          document.removeEventListener('click', el.clickOutsideEvent);
        }
      }
    }
  },
  methods: {
    selectFile(fileId) {
      this.$emit('select-file', fileId);
    },
    deleteFile(fileId) {
      this.$emit('delete-file', fileId);
    },
    closeFileSelection() {
      this.$emit('close');
    },
    showDataPreview() {
      this.$emit('show-preview');
    },
    downloadFile() {
      this.$emit('download-file');
    }
  }
}
</script>

<style scoped>
.file-selection-overlay {
  position: absolute;
  top: 60px;
  left: 0;
  width: 300px;
  background: white;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  z-index: 100;
  padding: 10px;
}

.file-list-container {
  min-height: 200px;
}

.no-files {
  text-align: center;
  color: #909399;
  padding: 40px 20px;
}

.file-list {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
}

.file-item {
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.file-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 6px 0 rgba(64, 158, 255, 0.2);
}

.file-item.selected {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.file-name {
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
  position: relative;
  padding-right: 20px;
  white-space: normal; /* 确保允许换行 */
  word-wrap: break-word;
  overflow-wrap: break-word;
  word-break: break-word; /* 更智能的断行 */
  user-select: none
}

.delete-file {
  position: absolute;
  right: 0;
  top: 0;
  color: #909399;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.delete-file:hover {
  color: #f56c6c;
  background-color: #fef0f0;
}

.file-info {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #909399;
  user-select: none
}

.file-actions {
  margin-top: 20px;
  text-align: center;
}

.upload-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #66b1ff;
}

/* 文件操作链接容器 */
.file-actions-container {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

/* 查看数据链接样式 */
.view-data-link {
  color: #409eff;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
  user-select: none
}

/* 下载文件链接样式 */
.download-file-link {
  color: #67c23a;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
  user-select: none
}

@media (max-width: 768px){
  .file-selection-overlay {
    width: 95%;
    top: 100px;
    left: 2.5%;
  }
  .file-list {
    max-height: 250px;
  }
}
</style>