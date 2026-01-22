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
                <input type="radio" v-model="exportFormat" value="pdf" />
                PDF
              </label>
              <label class="radio-option">
                <input type="radio" v-model="exportFormat" value="docx" />
                Word
              </label>
            </div>
          </div>
          
          <div class="select-all-section">
            <label class="checkbox-label">
              <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
              全选
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
                <div class="message-preview">
                  <span class="message-role">{{ message.type === 'sent' ? 'user' : model }}:</span>
                  <div v-html="renderMarkdown(message.content)"></div>
                </div>
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
import { jsPDF } from 'jspdf';
import { Document, Paragraph, TextRun, Packer } from 'docx';
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
      exportFormat: 'pdf', // 默认导出格式
      selectedMessages: [], // 选中的消息索引
      selectAll: false
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

      const selectedMsgs = this.selectedMessages
        .map(index => this.messages[index])
        .map(msg => ({
          role: msg.type === 'sent' ? 'user' : this.model,
          content: msg.content
        }))
        .filter(Boolean);

      if (this.exportFormat === 'pdf') {
        await this.exportToPdf(selectedMsgs);
      } else if (this.exportFormat === 'docx') {
        await this.exportToDocx(selectedMsgs);
      }

      // 导出完成后关闭对话框
      this.$emit('update:isShowingExportDialog', !this.isShowingExportDialog);
    },

    async exportToPdf(messages) {
      const pdf = new jsPDF();

      let yPosition = 20;
      pdf.setFontSize(12);

      messages.forEach((msg, index) => {
        const roleText = `${msg.role}: `;
        const fullText = `${roleText}${msg.content}`;
        
        // 添加角色
        pdf.setFont(undefined, 'bold');
        pdf.text(roleText, 10, yPosition);
        
        // 计算内容起始位置
        const roleWidth = pdf.getTextWidth(roleText);
        const startX = 10 + roleWidth;
        
        // 添加内容（自动换行）
        const contentLines = pdf.splitTextToSize(msg.content, 180 - roleWidth);
        pdf.setFont(undefined, 'normal');
        
        contentLines.forEach((line, lineIndex) => {
          if (yPosition > 280) { // 如果快到底部则添加新页面
            pdf.addPage();
            yPosition = 20;
          }
          
          if (lineIndex === 0) {
            pdf.text(line, startX, yPosition);
          } else {
            pdf.text(line, 10, yPosition);
          }
          yPosition += 10;
        });
        
        yPosition += 10; // 消息间距
        
        if (yPosition > 280 && index < messages.length - 1) { // 不是最后一个消息且需要新页
          pdf.addPage();
          yPosition = 20;
        }
      });

      // 保存PDF
      pdf.save(`chat_export_${new Date().toISOString().slice(0, 19)}.pdf`);
    },

    async exportToDocx(messages) {
      const docMessages = messages.map(msg => {
        return new Paragraph({
          children: [
            new TextRun({
              text: `${msg.role}: `,
              bold: true
            }),
            new TextRun(msg.content)
          ]
        });
      });

      const doc = new Document({
        sections: [{
          properties: {},
          children: docMessages
        }]
      });

      // 生成并下载
      const blob = await Packer.toBlob(doc);
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `chat_export_${new Date().toISOString().slice(0, 19)}.docx`;
      document.body.appendChild(a);
      a.click();
      
      // 清理
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 100);
    }
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
}

.select-all-section {
  margin-top: 15px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
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

.message-text {
  word-break: break-word;
  white-space: pre-wrap;
  color: #606266;
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
</style>