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
import { jsPDF } from 'jspdf';
import {Document, Paragraph, TextRun, Packer, HeadingLevel} from 'docx';
import { marked } from 'marked';
import html2canvas from "html2canvas";

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
      exportFormat: 'docx', // 默认导出格式
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

      if (this.exportFormat === 'pdf') {
        await this.exportToPdf(this.selectedMessages);
      } else if (this.exportFormat === 'docx') {
        const selectedMsgs = this.selectedMessages
          .map(index => this.messages[index])
          .map(msg => ({
            role: msg.type === 'sent' ? 'user' : this.model,
            content: msg.content
          }))
          .filter(Boolean);
        await this.exportToDocx(selectedMsgs);
      }

      // 导出完成后关闭对话框
      this.$emit('update:isShowingExportDialog', !this.isShowingExportDialog);
    },

    async exportToPdf(messageIDs) {
      const pdf = new jsPDF();
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 10;
      const maxWidth = pageWidth - margin * 2;
      
      let yPosition = margin;
      
      for (let i = 0; i < messageIDs.length; i++) {
        const element = document.getElementById('message-preview-' + messageIDs[i]);
        
        // 计算元素在PDF中的尺寸
        const elementWidth = element.offsetWidth;
        const elementHeight = element.offsetHeight;
        
        // 根据原始宽高比计算缩放后的尺寸
        let scaledWidth = maxWidth;
        let scaledHeight = (elementHeight * maxWidth) / elementWidth;
        
        // 如果当前页面空间不足，则添加新页面
        if (yPosition + scaledHeight > pageHeight - margin && i > 0) {
          pdf.addPage();
          yPosition = margin;
        }
        
        // 如果单个元素高度超过页面剩余空间，需要调整或分割
        if (scaledHeight > pageHeight - margin * 2) {
          // 对于超长元素，保持比例但限制最大高度
          scaledHeight = pageHeight - margin * 2;
          scaledWidth = (elementWidth * scaledHeight) / elementHeight;
        }
        
        // 检查是否需要新页面（确保有足够的空间）
        if (yPosition + scaledHeight > pageHeight - margin) {
          pdf.addPage();
          yPosition = margin;
        }
        
        const canvas = await html2canvas(element, {
          scale: 2,
          useCORS: true,
          scrollX: 0,
          scrollY: 0
        });
        
        const imgData = canvas.toDataURL('image/png');
        
        // 将元素渲染为图像并添加到PDF
        pdf.addImage(imgData, 'PNG', margin, yPosition, scaledWidth, scaledHeight);
        
        // 更新Y位置
        yPosition += scaledHeight + 5; // 添加一些间距
        
        // 如果到达页面底部，重置yPosition以开始新页面
        if (yPosition >= pageHeight - margin) {
          yPosition = margin;
        }
      }
      
      pdf.save(`chat_export_${new Date().toISOString().slice(0, 19)}.pdf`);

    },
    
    async exportToDocx(messages) {
      const docMessages = [];
      
      for (const msg of messages) {
        if (this.isShowingRole) {
          // 如果显示角色，则创建角色段落
          docMessages.push(
            new Paragraph({
              children: [
                new TextRun({
                  text: `${msg.role}:`,
                  bold: true,
                })
              ],
              heading: HeadingLevel.HEADING_1,
            })
          );
        }
        // 解析markdown内容并转换为docx段落
        const parsedContent = this.parseMarkdownToDocx(msg.content);
        docMessages.push(...parsedContent);
      }

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
    },
    
    // 将markdown内容转换为docx段落
    parseMarkdownToDocx(markdown) {
      const docMessages = [];
      
      // 使用marked解析markdown为tokens
      const tokens = marked.lexer(markdown);
      console.log(tokens);
      for (const token of tokens) {

        switch (token.type) {
          case 'paragraph':
            docMessages.push(new Paragraph({
              children: this.parseInlineMarkdown(token.text || '')
            }));
            break;
          case 'heading':
            docMessages.push(new Paragraph({
              children: [new TextRun({
                text: token.text || '',
                bold: true,
                size: 16 - (token.depth - 1) * 2 // 标题级别越大，字体越小
              })],
              heading: `heading_${token.depth}`
            }));
            break;
          case 'list':
            if (token.items) {
              token.items.forEach((item, index) => {
                docMessages.push(new Paragraph({
                  children: this.parseInlineMarkdown((item.text || '').replace(/^\s*[\*\+\-]\s*/, '')),
                  bullet: { level: 0 }
                }));
              });
            }
            break;
          case 'code':
            docMessages.push(new Paragraph({
              children: [new TextRun({
                text: token.code || token.text || '',
                fontFamily: 'Courier New'
              })],
              indent: { left: 720 } // 左缩进
            }));
            break;
          case 'table':
            // 处理表格
            const tableRows = [];
            // 表头
            const headerRow = [];
            if (token.header) {
              token.header.forEach(cell => {
                headerRow.push(cell);
              });
            }
            
            // 表体
            const bodyRows = [];
            if (token.rows) {
              token.rows.forEach(row => {
                const cells = [];
                row.forEach(cell => {
                  cells.push(cell);
                });
                bodyRows.push(cells);
              });
            }
            
            // 这里我们简化处理，将表格转换为文本形式
            // 表头
            if (headerRow.length > 0) {
              docMessages.push(new Paragraph({
                children: [new TextRun({
                  text: '| ' + headerRow.join(' | ') + ' |',
                  bold: true
                })]
              }));
              
              // 分隔线
              docMessages.push(new Paragraph({
                children: [new TextRun('| ' + headerRow.map(() => '---').join(' | ') + ' |')]
              }));
            }
            
            // 表体
            bodyRows.forEach(row => {
              docMessages.push(new Paragraph({
                children: [new TextRun('| ' + row.join(' | ') + ' |')]
              }));
            });
            
            break;
          case 'space':
            // 处理空格，插入换行
            if (token.raw) {
              docMessages.push(new Paragraph({
                children: [new TextRun({
                  text: token.raw
                })]
              }));
            }
            break;
          default:
            // 对于其他类型的token，作为普通段落处理
            if (token.text !== undefined) {
              docMessages.push(new Paragraph({
                children: this.parseInlineMarkdown(token.text || '')
              }));
            } else if (token.raw) {
              // 如果没有text属性但有raw属性，使用raw
              docMessages.push(new Paragraph({
                children: this.parseInlineMarkdown(token.raw || '')
              }));
            }
            break;
        }
      }
      
      return docMessages;
    },
    
    // 解析行内markdown格式，返回TextRun数组
    parseInlineMarkdown(text) {
      // 确保text是字符串类型
      if (typeof text !== 'string') {
        text = String(text);
      }
      
      // 定义正则表达式来匹配不同的markdown格式
      const rules = [
        // 匹配粗体 **text** 或 __text__
        { regex: /\*\*(.*?)\*\*/g, type: 'bold' },
        { regex: /__(.*?)__/g, type: 'bold' },
        // 匹配斜体 *text* 或 _text_
        { regex: /\*(.*?)\*/g, type: 'italic' },
        { regex: /_(.*?)_/g, type: 'italic' },
        // 匹配行内代码 `code`
        { regex: /`(.*?)`/g, type: 'code' }
      ];
      
      // 创建TextRun数组
      let parts = [{ text, formatting: {} }];
      
      // 应用所有格式规则
      for (const rule of rules) {
        const newParts = [];
        
        for (const part of parts) {
          if (part.formatting[rule.type]) {
            // 如果已经有此格式，跳过
            newParts.push(part);
            continue;
          }
          
          // 确保 part.text 是字符串
          let remainingText = typeof part.text === 'string' ? part.text : String(part.text);
          let lastIndex = 0;
          let match;
          
          while ((match = rule.regex.exec(remainingText)) !== null) {
            // 添加匹配前的文本
            if (match.index > lastIndex) {
              newParts.push({
                text: remainingText.substring(lastIndex, match.index),
                formatting: { ...part.formatting }
              });
            }
            
            // 添加匹配的文本，带格式
            const newFormatting = { ...part.formatting };
            newFormatting[rule.type] = true;
            
            // 确保 match[1] 存在
            const matchedText = match[1] || '';
            
            newParts.push({
              text: matchedText,
              formatting: newFormatting
            });
            
            lastIndex = match.index + match[0].length;
            rule.regex.lastIndex = lastIndex; // 重置正则表达式的lastIndex
          }
          
          // 添加剩余文本
          if (lastIndex < remainingText.length) {
            newParts.push({
              text: remainingText.substring(lastIndex),
              formatting: { ...part.formatting }
            });
          }
          
          parts = newParts;
        }
      }
      
      // 将parts转换为TextRun对象
      return parts.map(part => {
        const options = {};
        
        if (part.formatting.bold) {
          options.bold = true;
        }
        if (part.formatting.italic) {
          options.italic = true;
        }
        if (part.formatting.code) {
          options.fontFamily = 'Courier New';
          options.color = {
            rgb: 'C0C0C0'
          };
        }
        
        // 确保 part.text 是字符串
        const textValue = typeof part.text === 'string' ? part.text : String(part.text);
        
        return new TextRun({
          text: textValue,
          ...options
        });
      });
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