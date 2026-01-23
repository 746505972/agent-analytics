<template>
  <div v-if="isShowingExportDialog" class="export-overlay" @click="handleOverlayClick">
    <div class="export-dialog" @click.stop>
      <div class="export-header">
        <h3>导出对话记录</h3>
        <button class="close-btn" @click="$emit('update:isShowingExportDialog', false)">&times;</button>
      </div>
      
      <div class="export-content">
        <div class="export-options">
          <div class="option-group">
            <h4>选择导出格式</h4>
            <div class="format-options">
              <label class="radio-option">
                <input type="radio" v-model="exportFormat" value="html" />
                HTML
              </label>
              <label class="radio-option">
                <input type="radio" v-model="exportFormat" value="docx" />
                Word
              </label>
              <label class="radio-option">
                <input type="radio" v-model="exportFormat" value="pdf" />
                PDF
              </label>
            </div>
          </div>
          
          <div class="select-all-section">
            <label class="checkbox-label">
              <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
              全选
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="isShowingRole"/>
              显示角色
            </label>
          </div>
        </div>
        
        <div class="messages-container">
          <h4>选择要导出的对话</h4>
          <div class="message-list">
            <div 
              v-for="(message, index) in messages" 
              :key="index" 
              class="message-item"
            >
              <label class="message-checkbox">
                <input 
                  type="checkbox" 
                  :value="index" 
                  v-model="selectedMessages" 
                />
                <span class="message-preview" :id="'message-preview-' + index">
                  <span v-if="isShowingRole" class="message-role">{{ message.type === 'sent' ? 'user' : model }}:</span>
                  <span class="message" v-html="renderMarkdown(message.content)"></span>
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <div class="export-footer">
        <button @click="$emit('update:isShowingExportDialog', false)" class="btn btn-cancel">取消</button>
        <button @click="handleExport" class="btn btn-export" :disabled="selectedMessages.length === 0">
          导出({{ selectedMessages.length }})
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';

export default {
  name: 'ExportDialog',
  props: {
    messages: {
      type: Array,
      default: () => []
    },
    isShowingExportDialog: {
      type: Boolean,
      default: false
    },
    model: {
      type: String,
      default: ''
    }
  },
  emits: ['update:isShowingExportDialog'],
  data() {
    return {
      exportFormat: 'html', // 默认导出格式
      selectedMessages: [], // 选中的消息索引
      selectAll: false,
      isShowingRole: true
    }
  },
  watch: {
    messages: {
      handler() {
        // 当消息更新时，重新初始化选中状态
        this.initializeSelection();
      },
      deep: true
    },
    selectedMessages: {
      handler() {
        // 当选中消息更新时，更新全选状态
        this.selectAll = this.selectedMessages.length === this.messages.length;
      },
      deep: true
    }
  },
  methods: {
    initializeSelection() {
      // 初始化时全选所有消息
      this.selectedMessages = this.messages.map((_, index) => index);
      this.selectAll = this.messages.length > 0;
    },
    
    toggleSelectAll() {
      if (this.selectAll) {
        this.selectedMessages = this.messages.map((_, index) => index);
      } else {
        this.selectedMessages = [];
      }
    },
    
    handleOverlayClick(event) {
      // 点击overlay关闭对话框
      if (event.target === event.currentTarget) {
        this.$emit('update:isShowingExportDialog', !this.isShowingExportDialog);
      }
    },

    renderMarkdown(content) {
      if (!content) return '';
      return marked.parse(content);
    },
    
    async handleExport() {
      if (this.selectedMessages.length === 0) return;

      // 排序
      this.selectedMessages.sort((a, b) => a - b);
      await this.exportUnified(this.selectedMessages, this.exportFormat);

      // 导出完成后关闭对话框
      this.$emit('update:isShowingExportDialog', !this.isShowingExportDialog);
    },

    async exportUnified(messageIDs, format) {
      // 构建HTML内容
      let htmlContent = '';
      
      // 获取选中的消息
      const selectedMsgs = messageIDs
        .map(index => this.messages[index])
        .map(msg => ({
          role: msg.type === 'sent' ? 'user' : this.model,
          content: msg.content
        }))
        .filter(Boolean);
      
      for (const msg of selectedMsgs) {
        if (this.isShowingRole) {
          // 添加角色信息
          htmlContent += `<h3>${msg.role}:</h3>`;
        }
        
        // 使用marked解析markdown内容
        const renderedHtml = await marked.parse(msg.content);
        htmlContent += renderedHtml;
      }
      
      // 构建完整的HTML文档
      const fullHtml = `
        <html
              xmlns="http://www.w3.org/TR/REC-html40">
          <head>
            <meta charset="utf-8">
            <title>Chat Export</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
              h1 { color: #409eff; font-size: 1.2em; }
              h3 { color: #409eff; font-size: 1.1em; margin: 15px 0 5px 0; }
              table { border-collapse: collapse; width: 100%; margin: 10px 0; }
              th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
              th { background-color: #f5f7fa; font-weight: bold; }
              code { background-color: #f6f8fa; padding: 2px 4px; border-radius: 4px; font-family: monospace; }
              pre { background-color: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; white-space: pre-wrap; }
              blockquote { border-left: 4px solid #ddd; margin: 0; padding-left: 16px; color: #666; }
              ul, ol { padding-left: 20px; }
              li { margin: 5px 0; }
              hr { border: 0; border-top: 1px solid #ccc; margin: 15px 0; }
              img { max-width: 100%; height: auto; }
              @media print {
                body { -webkit-print-color-adjust: exact; color-adjust: exact; }
                @page { margin: 20px; size: A4; }
                .page-break { page-break-before: always; }
              }
            </style>
          </head>
          <body>
            ${htmlContent}
          </body>
        </html>
      `;
      
      if (format === 'pdf') {
        // 创建一个隐藏的iframe用于打印
        const iframe = document.createElement('iframe');
        iframe.style.position = 'fixed';
        iframe.style.right = '0';
        iframe.style.bottom = '0';
        iframe.style.width = '0';
        iframe.style.height = '0';
        iframe.style.border = 'none';
        iframe.style.zIndex = '-1';
        iframe.srcdoc = fullHtml;
        
        iframe.onload = () => {
          // 延迟执行以确保内容完全加载
          setTimeout(() => {
            iframe.contentWindow.focus();
            iframe.contentWindow.print();
            
            // 打印完成后移除iframe
            setTimeout(() => {
              document.body.removeChild(iframe);
            }, 1000);
          }, 500);
        };
        
        document.body.appendChild(iframe);
      } else {
        // 处理HTML和DOCX格式
        let mimeType, fileName;
        
        if (format === 'html') {
          mimeType = 'text/html';
          fileName = `chat_export_${new Date().toISOString().slice(0, 19)}.html`;
        } else { // doc
          mimeType = 'application/msword';
          fileName = `chat_export_${new Date().toISOString().slice(0, 19)}.doc`;
        }
        
        // 创建Blob对象
        const blob = new Blob(['\ufeff', fullHtml], { type: mimeType });
        
        // 创建并触发下载
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        
        // 清理DOM元素
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
      }
    },
  },
  
  mounted() {
    this.initializeSelection();
  }
};
</script>

<style scoped>
.export-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.export-dialog {
  width: 700px;
  max-height: 80vh;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.export-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dcdfe6;
  background-color: #f8f9fa;
}

.export-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #606266;
}

.export-content {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
}

.export-options {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.option-group h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.format-options {
  display: flex;
  gap: 20px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  user-select: none;
}

.select-all-section {
  margin-top: 15px;
  display: flex;
  gap: 20px
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  user-select: none;
}

.messages-container h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #303133;
}

.message-list {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.message-item {
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
}

.message-item:last-child {
  border-bottom: none;
}

.message-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
}

.message-preview {
  flex-grow: 1;
}

.message-role {
  font-weight: bold;
  color: #409eff;
  margin-right: 8px;
}

.export-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #dcdfe6;
  background-color: #f8f9fa;
}

.btn {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-cancel {
  background-color: #f4f4f5;
  color: #606266;
}

.btn-cancel:hover {
  background-color: #e6e6e7;
}

.btn-export {
  background-color: #409eff;
  color: white;
}

.btn-export:hover:not(:disabled) {
  background-color: #3a8ee6;
}

.btn-export:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
}

/* Markdown 表格样式 */
.message :deep(table) {
  border-collapse: collapse;
  margin: 15px 0;
  font-size: 0.9em;
  font-family: sans-serif;
  min-width: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 0;
}

.message :deep(table th),
.message :deep(table td) {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  text-align: left;
}

.message :deep(table th) {
  background-color: #f5f7fa;
  font-weight: 600;
}

.message :deep(table tbody tr:nth-of-type(even)) {
  background-color: #f8f9fa;
}

.message :deep(table tbody tr:hover) {
  background-color: #f0f2f5;
}

/* Markdown 代码块样式 */
.message :deep(code) {
  background-color: #f6f8fa;
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.875em;
  font-family: 'SFMono-Regular', Consolas, 'Courier New', monospace;
  color: #24292f;
}

.message :deep(pre) {
  background-color: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  border: 1px solid #d0d7de;
}

.message :deep(pre code) {
  background-color: transparent;
  padding: 0;
  font-size: 0.875em;
  color: #24292f;
}
</style>