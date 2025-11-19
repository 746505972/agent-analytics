<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>欢迎使用 Agent-Analytics 智能数据分析平台</h2>
    </div>
    
    <div class="dashboard-content">
      <!-- 左侧：文件选择区域 -->
      <div class="left-section">
        <div class="file-selection-section">
          <div class="section-header" @click="toggleFileSection">
            <h2>选择分析文件</h2>
            <span class="toggle-icon">{{ isFileSectionCollapsed ? '+' : '-' }}</span>
          </div>
          
          <div v-show="!isFileSectionCollapsed" class="file-section-content">
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
        
        <!-- 方法选择区域移到左栏 -->
        <div v-if="selectedFile" class="method-selection-section">
          <h3>方法选择</h3>
          <div class="method-categories">
            <div 
              v-for="category in methodCategories" 
              :key="category.id"
              class="method-category"
              :class="{ active: currentCategory === category.id }"
            >
              <div class="category-header" @click="selectCategory(category.id)">
                <h4>{{ category.name }}</h4>
                <span class="toggle-icon">{{ currentCategory === category.id ? '−' : '+' }}</span>
              </div>
              <div v-show="currentCategory === category.id" class="category-methods">
                <button 
                  v-for="method in category.methods" 
                  :key="method.id"
                  :class="{ active: currentMethod === method.id }"
                  @click="selectMethod(method.id)"
                  class="method-tab"
                >
                  {{ method.name }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 中间：列名列表区域 -->
      <div class="middle-section">
        <!-- 方法描述和执行按钮移到中栏 -->
        <div v-if="selectedFile" class="method-description-section">
          <div class="method-description-content">
            <div class="method-content">
              <div v-if="currentMethod === 'basic_info'" class="basic-info-method">
                <h4>数据集基本信息</h4>
                <p>查看数据集的基本信息，包括行列数、列名、数据类型等。</p>
              </div>
              <div v-else-if="currentMethod === 'statistical_summary'" class="statistical-summary-method">
                <h4>统计摘要</h4>
                <p>获取数据集的统计摘要信息，包括均值、中位数、标准差等。</p>
              </div>
              <div v-else-if="currentMethod === 'correlation_analysis'" class="correlation-analysis-method">
                <h4>相关性分析</h4>
                <p>分析数据集中各变量之间的相关性。</p>
              </div>
              <div v-else-if="currentMethod === 'distribution_analysis'" class="distribution-analysis-method">
                <h4>分布分析</h4>
                <p>分析数据集中各变量的分布情况。</p>
              </div>
              <div v-else-if="currentMethod === 'visualization'" class="visualization-method">
                <h4>数据可视化</h4>
                <p>生成数据集的可视化图表，帮助理解数据分布和关系。</p>
              </div>
              <div v-else-if="currentMethod === 'ml_analysis'" class="ml-analysis-method">
                <h4>机器学习分析</h4>
                <p>执行机器学习分析任务，如聚类、分类、回归等。</p>
              </div>
              <div v-else-if="currentMethod === 'clustering'" class="clustering-method">
                <h4>聚类分析</h4>
                <p>使用聚类算法对数据进行分组分析。</p>
              </div>
              <div v-else-if="currentMethod === 'classification'" class="classification-method">
                <h4>分类分析</h4>
                <p>使用分类算法对数据进行分类预测。</p>
              </div>
              <div v-else-if="currentMethod === 'regression'" class="regression-method">
                <h4>回归分析</h4>
                <p>使用回归算法分析变量之间的关系。</p>
              </div>
              <div v-else-if="currentMethod === 'text_analysis'" class="text-analysis-method">
                <h4>文本分析</h4>
                <p>对文本数据进行分析，提取关键信息和模式。</p>
              </div>
              <div v-else-if="currentMethod === 'sentiment_analysis'" class="sentiment-analysis-method">
                <h4>情感分析</h4>
                <p>分析文本数据中的情感倾向。</p>
              </div>
              <div v-else-if="currentMethod === 'data_cleaning'" class="data-cleaning-method">
                <h4>数据清洗</h4>
                <p>清理数据中的噪声和异常值。</p>
              </div>
              <div v-else-if="currentMethod === 'data_transformation'" class="data-transformation-method">
                <h4>数据转换</h4>
                <p>对数据进行转换操作，如标准化、归一化等。</p>
              </div>
            </div>
            <div class="method-actions">
              <button @click="executeMethod" class="execute-button">执行分析</button>
            </div>
          </div>
        </div>
        
        <!-- 列名列表区域 -->
        <div v-if="selectedFile && selectedFileColumns.length > 0" class="column-list-section">
          <h3>列名列表</h3>
          <ul class="column-list">
            <li v-for="(column, index) in selectedFileColumns" :key="index" class="column-item">
              {{ column }}
            </li>
          </ul>
        </div>
      </div>
      
      <!-- 右侧：聊天分析区域 -->
      <div class="right-section">
        <div class="chat-section">
          <div class="chat-header">
            <h2>数据分析助手</h2>
            <button @click="clearChatHistory" class="clear-chat-btn">清除历史记录</button>
          </div>
          <div class="chat-box">
            <div class="messages">
              <div 
                v-for="(message, index) in chatMessages" 
                :key="index"
                class="message"
                :class="message.type"
              >
                <span v-if="message.type === 'received' && message.content === '' && isWaitingForResponse" class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
                <div v-else class="message-content-wrapper">
                  <div v-html="renderMarkdown(message.content)" class="message-content"></div>
                  <button 
                    v-if="message.content" 
                    @click="copyMessageText(message.content)"
                    class="copy-button"
                    :class="{ copied: message.copied }"
                    :title="message.copied ? '已复制' : '复制文本'"
                  >
                    {{ message.copied ? '✓ 已复制' : '复制' }}
                  </button>
                </div>
              </div>
            </div>
            <div class="input-area">
              <input 
                type="text" 
                placeholder="输入您的分析需求..." 
                v-model="userInput"
                @keyup.enter="sendMessage"
                :disabled="!selectedFile || isWaitingForResponse"
              />
              <button @click="sendMessage" :disabled="!selectedFile || isWaitingForResponse">发送</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 数据预览弹窗 -->
    <div class="preview-modal" v-if="showPreviewModal">
      <div class="preview-modal-content">
        <div class="preview-header">
          <h3>数据预览</h3>
          <button class="close-button" @click="closePreviewModal">×</button>
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
  </div>
</template>

<script>
import { marked } from 'marked';

export default {
  name: "Dashboard",
  data() {
    return {
      files: [],
      selectedFile: null,
      selectedFileColumns: [],
      userInput: "",
      chatMessages: [
        {
          type: "received",
          content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
        }
      ],
      isFileSectionCollapsed: false,
      isWaitingForResponse: false,
      // 新增方法选择相关数据
      currentMethod: 'basic_info',
      currentCategory: 'statistics',
      methodCategories: [
        {
          id: 'statistics',
          name: '统计方法',
          methods: [
            { id: 'basic_info', name: '基本信息' },
            { id: 'statistical_summary', name: '统计摘要' },
            { id: 'correlation_analysis', name: '相关性分析' },
            { id: 'distribution_analysis', name: '分布分析' }
          ]
        },
        {
          id: 'ml',
          name: '机器学习',
          methods: [
            { id: 'ml_analysis', name: '机器学习分析' },
            { id: 'clustering', name: '聚类分析' },
            { id: 'classification', name: '分类分析' },
            { id: 'regression', name: '回归分析' }
          ]
        },
        {
          id: 'visualization',
          name: '可视化',
          methods: [
            { id: 'visualization', name: '数据可视化' }
          ]
        },
        {
          id: 'nlp',
          name: '文本分析',
          methods: [
            { id: 'text_analysis', name: '文本分析' },
            { id: 'sentiment_analysis', name: '情感分析' }
          ]
        },
        {
          id: 'data_processing',
          name: '数据处理',
          methods: [
            { id: 'data_cleaning', name: '数据清洗' },
            { id: 'data_transformation', name: '数据转换' }
          ]
        }
      ],
      // 数据预览弹窗相关数据
      showPreviewModal: false,
      previewData: {
        documentName: '',
        columnHeaders: [],
        rowData: [],
        displayedRows: [],
        totalRows: 0,
        totalPages: 0,
        currentPage: 1,
        pageSize: 10,
        loading: true
      }
    }
  },
  async mounted() {
    await this.loadUploadedFiles();
    // 恢复保存的状态
    this.restoreState();
    // 检查是否有刚上传的文件需要默认选中
    this.checkAndSelectUploadedFile();
  },
  methods: {
    // 添加Markdown渲染方法
    renderMarkdown(content) {
      if (!content) return '';
      return marked.parse(content);
    },
    
    toggleFileSection() {
      this.isFileSectionCollapsed = !this.isFileSectionCollapsed;
      // 保存文件选择区域的展开/收起状态到localStorage
      localStorage.setItem('isFileSectionCollapsed', this.isFileSectionCollapsed.toString());
    },
    
    async loadUploadedFiles() {
      // 调用后端API获取用户上传的文件列表
      try {
        const response = await fetch('/user/files', {
          credentials: 'include' // 包含cookies，用于session管理
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            this.files = result.data;
          } else {
            console.error("获取文件列表失败:", result.error);
          }
        } else {
          console.error("获取文件列表失败，状态码:", response.status);
        }
      } catch (error) {
        console.error("加载文件列表失败:", error);
      }
    },
    
    async deleteFile(fileId) {
      if (!confirm('确定要删除这个文件吗？')) {
        return;
      }
      
      try {
        const response = await fetch(`/data/${fileId}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            // 从文件列表中移除已删除的文件
            this.files = this.files.filter(file => file.data_id !== fileId);
            
            // 如果删除的是当前选中的文件，清空选中状态和列名
            if (this.selectedFile === fileId) {
              this.selectedFile = null;
              this.selectedFileColumns = [];
              // 清除保存的选中文件状态
              localStorage.removeItem('selectedFile');
            }
            
            console.log('文件删除成功');
          } else {
            console.error('删除失败:', result.error);
          }
        } else {
          console.error('删除请求失败，状态码:', response.status);
        }
      } catch (error) {
        console.error('删除文件时发生错误:', error);
      }
    },
    
    async selectFile(fileId) {
      this.selectedFile = fileId;
      // 保存选中的文件状态
      localStorage.setItem('selectedFile', fileId);
      
      // 获取选中文件的列名
      try {
        const response = await fetch(`/data/${fileId}/info`, {
          credentials: 'include'
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            this.selectedFileColumns = result.data.column_names;
          } else {
            console.error("获取列名失败:", result.error);
            this.selectedFileColumns = [];
          }
        } else {
          console.error("获取列名失败，状态码:", response.status);
          this.selectedFileColumns = [];
        }
      } catch (error) {
        console.error("加载列名失败:", error);
        this.selectedFileColumns = [];
      }
    },
    
    selectMethod(methodId) {
      this.currentMethod = methodId;
      // 保存选中的方法到localStorage
      localStorage.setItem('selectedMethod', methodId);
      
      // 根据选中的方法自动展开对应的大类
      const category = this.methodCategories.find(cat => 
        cat.methods.some(method => method.id === methodId)
      );
      if (category) {
        this.currentCategory = category.id;
        // 保存当前展开的大类
        localStorage.setItem('selectedCategory', category.id);
      }
    },
    
    selectCategory(categoryId) {
      this.currentCategory = this.currentCategory === categoryId ? null : categoryId;
      // 保存当前展开的大类
      localStorage.setItem('selectedCategory', this.currentCategory || '');
    },
    
    executeMethod() {
      if (!this.selectedFile || !this.currentMethod) {
        return;
      }
      
      // 保存聊天记录到localStorage
      localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      
      // 保存文件选择区域的展开/收起状态
      localStorage.setItem('isFileSectionCollapsed', this.isFileSectionCollapsed.toString());
      
      // 保存当前选中的方法和大类
      localStorage.setItem('selectedMethod', this.currentMethod);
      localStorage.setItem('selectedCategory', this.currentCategory);
      
      // 根据选择的方法跳转到相应的分析页面
      this.$router.push({
        name: 'Analysis',
        query: {
          data_id: this.selectedFile,
          method: this.currentMethod
        }
      });
    },
    
    // 新增方法：恢复保存的状态
    restoreState() {
      // 恢复选中的文件
      const savedSelectedFile = localStorage.getItem('selectedFile');
      if (savedSelectedFile) {
        this.selectedFile = savedSelectedFile;
        // 获取选中文件的列名
        this.selectFile(savedSelectedFile);
      }
      
      // 恢复选中的方法
      const savedSelectedMethod = localStorage.getItem('selectedMethod');
      if (savedSelectedMethod) {
        this.currentMethod = savedSelectedMethod;
      }
      
      // 恢复展开的大类
      const savedSelectedCategory = localStorage.getItem('selectedCategory');
      if (savedSelectedCategory) {
        this.currentCategory = savedSelectedCategory;
      } else if (savedSelectedMethod) {
        // 如果没有保存的大类状态但有选中的方法，则自动确定大类
        const category = this.methodCategories.find(cat => 
          cat.methods.some(method => method.id === savedSelectedMethod)
        );
        if (category) {
          this.currentCategory = category.id;
        }
      }
      
      // 恢复聊天记录
      const savedChatMessages = localStorage.getItem('dashboardChatMessages');
      if (savedChatMessages) {
        try {
          this.chatMessages = JSON.parse(savedChatMessages);
        } catch (e) {
          console.error("解析保存的聊天记录失败:", e);
        }
      }
      
      // 恢复文件选择区域的展开/收起状态
      const savedFileSectionState = localStorage.getItem('isFileSectionCollapsed');
      if (savedFileSectionState !== null) {
        this.isFileSectionCollapsed = savedFileSectionState === 'true';
      }
    },
    
    // 新增方法：检查并选中刚上传的文件
    checkAndSelectUploadedFile() {
      // 从localStorage获取刚上传的文件ID
      const currentDataId = localStorage.getItem('currentDataId');
      if (currentDataId && this.files.some(file => file.data_id === currentDataId)) {
        // 如果有刚上传的文件且在文件列表中存在，则默认选中它
        this.selectFile(currentDataId);
      }
    },
    
    // 页面激活时恢复状态（从其他页面返回时调用）
    activated() {
      this.restoreState();
    },
    
    async sendMessage() {
      if (this.userInput.trim() === "" || this.isWaitingForResponse) {
        return;
      }
      
      // 添加用户消息到聊天记录
      const userMessage = {
        type: "sent",
        content: this.userInput
      };
      
      this.chatMessages.push(userMessage);
      const userQuery = this.userInput;
      this.userInput = "";
      this.isWaitingForResponse = true;
      
      // 保存聊天记录到localStorage
      localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      
      // 添加AI回复占位符
      const aiMessageIndex = this.chatMessages.length;
      this.chatMessages.push({
        type: "received",
        content: ""
      });
      
      // 保存聊天记录到localStorage
      localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      
      try {
        // 准备请求数据
        const requestData = {
          message: userQuery,
          data_id: this.selectedFile,
          history: this.chatMessages.slice(0, -1) // 不包括刚添加的AI回复占位符
        };
        
        console.log("发送请求数据:", requestData);
        
        // 发起流式请求
        const response = await fetch('/chat/stream', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData),
          credentials: 'include'
        });
        
        console.log("收到响应:", response);
        
        if (response.ok && response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let done = false;
          let accumulatedContent = "";
          
          console.log("开始读取流式响应");
          
          // 逐步接收流式响应
          while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            
            if (value) {
              const chunk = decoder.decode(value, { stream: true });
              console.log("收到原始数据块:", JSON.stringify(chunk));
              const lines = chunk.split('\n');
              
              for (const line of lines) {
                console.log("处理行:", JSON.stringify(line));
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  console.log("解析数据:", JSON.stringify(data));
                  
                  if (data === '[DONE]') {
                    console.log("接收完成");
                    done = true;
                    break;
                  }
                  
                  try {
                    const parsed = JSON.parse(data);
                    console.log("解析后的数据:", parsed);
                    if (parsed.content !== undefined) {
                      accumulatedContent += parsed.content;
                      console.log("更新内容:", accumulatedContent);
                      // 更新AI回复内容
                      this.chatMessages[aiMessageIndex].content = accumulatedContent;
                      // 滚动到底部并触发更新
                      this.$nextTick(() => {
                        const messagesContainer = document.querySelector('.messages');
                        if (messagesContainer) {
                          messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        }
                      });
                                          
                      // 每累积一定字符数就强制更新DOM以实现实时显示效果
                      if (accumulatedContent.length % 5 === 0) {
                        await this.$nextTick();
                      }
                    } else if (parsed.error) {
                      console.error("流式响应错误:", parsed.error);
                      this.chatMessages[aiMessageIndex].content = `错误: ${parsed.error}`;
                      done = true;
                    }
                  } catch (e) {
                    console.error("解析流数据错误:", e, "原始数据:", data);
                    // 即使解析失败，也尝试显示原始内容
                    this.chatMessages[aiMessageIndex].content = `解析错误: ${data}`;
                    
                    // 强制更新DOM
                    await this.$nextTick();
                  }
                } else {
                  // 处理不以 'data: ' 开头的行，可能是错误信息
                  if (line.trim() !== '') {
                    console.log("处理非data行:", line);
                    try {
                      const parsed = JSON.parse(line);
                      if (parsed.error) {
                        console.error("直接错误响应:", parsed.error);
                        this.chatMessages[aiMessageIndex].content = `错误: ${parsed.error}`;
                        done = true;
                      }
                    } catch (e) {
                      console.log("非JSON格式行，跳过");
                    }
                  }
                  console.log("跳过非data行:", line);
                }
              }
            } else {
              console.log("收到空值");
            }
          }
          console.log("流处理完成，最终内容:", accumulatedContent);
        } else {
          console.error("响应失败，状态码:", response.status);
          this.chatMessages[aiMessageIndex].content = `抱歉，无法连接到AI助手。状态码: ${response.status}`;
        }
      } catch (error) {
        console.error("发送消息时发生错误:", error);
        this.chatMessages[aiMessageIndex].content = `抱歉，处理您的请求时出现错误: ${error.message}`;
      } finally {
        this.isWaitingForResponse = false;
        // 保存聊天记录到localStorage
        localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      }
    },
    
    clearChatHistory() {
      if (confirm('确定要清除聊天历史记录吗？')) {
        // 重置聊天记录为初始状态
        this.chatMessages = [
          {
            type: "received",
            content: "您好！我是您的数据分析助手，请选择一个文件并告诉我您需要什么分析？"
          }
        ];
        // 清除localStorage中的聊天记录
        localStorage.removeItem('dashboardChatMessages');
      }
    },
    
    // 添加复制消息文本的方法
    copyMessageText(text) {
      navigator.clipboard.writeText(text).then(() => {
        // 添加视觉反馈
        console.log('文本已复制到剪贴板');
        // 创建一个临时的提示元素
        this.showCopyNotification('文本已复制到剪贴板');
      }).catch(err => {
        console.error('复制失败:', err);
        this.showCopyNotification('复制失败: ' + err.message, true);
      });
    },
    
    // 显示复制通知
    showCopyNotification(message, isError = false) {
      // 创建通知元素
      const notification = document.createElement('div');
      notification.textContent = message;
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background-color: ${isError ? '#f56c6c' : '#67c23a'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        z-index: 2000;
        font-size: 14px;
      `;
      
      // 添加到页面
      document.body.appendChild(notification);
      
      // 3秒后移除
      setTimeout(() => {
        if (notification.parentNode) {
          notification.parentNode.removeChild(notification);
        }
      }, 3000);
    },
    
    getSelectedFileName() {
      const file = this.files.find(f => f.data_id === this.selectedFile);
      return file ? file.filename : "";
    },
    
    // 显示数据预览弹窗
    async showDataPreview() {
      if (!this.selectedFile) return;
      
      // 初始化预览数据
      this.previewData.currentPage = 1;
      this.previewData.loading = true;
      this.showPreviewModal = true;
      
      // 获取选中文件的信息
      const selectedFile = this.files.find(file => file.data_id === this.selectedFile);
      if (selectedFile) {
        this.previewData.documentName = selectedFile.filename;
      }
      
      // 加载数据
      await this.loadPreviewData();
    },
    
    // 关闭数据预览弹窗
    closePreviewModal() {
      this.showPreviewModal = false;
    },
    
    // 加载预览数据
    async loadPreviewData() {
      this.previewData.loading = true;
      try {
        const response = await fetch(`/data/${this.selectedFile}?page=${this.previewData.currentPage}&page_size=${this.previewData.pageSize}`, {
          credentials: 'include'
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            this.previewData.columnHeaders = result.data.columns;
            this.previewData.rowData = result.data.data;
            this.previewData.displayedRows = result.data.data;
            this.previewData.totalRows = result.data.rows;
            this.previewData.totalPages = result.data.total_pages;
            this.previewData.documentName = result.data.data_id;  // 使用data_id作为文档名
          } else {
            console.error("获取预览数据失败:", result.error);
            this.useSampleDataInPreview();
          }
        } else {
          console.error("获取预览数据失败，状态码:", response.status);
          this.useSampleDataInPreview();
        }
      } catch (error) {
        console.error('加载预览数据失败:', error);
        this.useSampleDataInPreview();
      } finally {
        this.previewData.loading = false;
      }
    },
    
    // 在预览中使用示例数据
    useSampleDataInPreview() {
      this.previewData.columnHeaders = ['示例数据0', '示例数据1', '示例数据2', '示例数据3'];
      this.previewData.rowData = [];
      for (let i = 1; i <= 30; i++) {
        this.previewData.rowData.push({
          '示例数据0': '示例数据',
          '示例数据1': '示例数据',
          '示例数据2': '示例数据',
          '示例数据3': '示例数据',
        });
      }
      this.previewData.displayedRows = this.previewData.rowData;
      this.previewData.totalRows = this.previewData.rowData.length;
      this.previewData.totalPages = Math.ceil(this.previewData.totalRows / this.previewData.pageSize);
      this.previewData.documentName = '示例数据文档';
    },
    
    // 翻页相关方法
    changePage(page) {
      this.previewData.currentPage = page;
      this.loadPreviewData();
    },
    
    prevPage() {
      if (this.previewData.currentPage > 1) {
        this.changePage(this.previewData.currentPage - 1);
      }
    },
    
    nextPage() {
      if (this.previewData.currentPage < this.previewData.totalPages) {
        this.changePage(this.previewData.currentPage + 1);
      }
    },
    
    // 下载文件方法
    downloadFile() {
      if (!this.selectedFile) return;
      
      // 获取选中的文件信息
      const selectedFile = this.files.find(file => file.data_id === this.selectedFile);
      if (!selectedFile) return;
      
      // 构造下载链接
      const downloadUrl = `/data/${this.selectedFile}/download`;
      
      // 创建一个隐藏的a标签用于下载
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = selectedFile.filename;
      link.style.display = 'none';
      
      // 添加到页面并触发点击
      document.body.appendChild(link);
      link.click();
      
      // 清理
      document.body.removeChild(link);
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 0;
  max-width: 100%;
  margin: 0;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 20px;
  padding: 10px;
}

.dashboard-header h1 {
  color: #303133;
  margin-bottom: 10px;
}

.dashboard-header p {
  color: #606266;
  font-size: 16px;
}

.dashboard-content {
  display: flex;
  height: calc(100vh - 120px);
  padding: 0 10px;
  gap: 10px;
}

.left-section {
  flex: 0.5;
  padding-left: 0px;
  overflow-y: auto;
  max-height: 100%;
}

.middle-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0 10px;
  overflow-y: auto;
  max-height: 100%;
}

.right-section {
  flex: 1;
  padding-right: 10px;
  overflow-y: auto;
  max-height: 100%;
}

.file-selection-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  cursor: pointer;
  border-bottom: 1px solid #ebeef5;
}

.section-header h2 {
  margin: 0;
  color: #303133;
}

.toggle-icon {
  font-size: 20px;
  font-weight: bold;
  color: #909399;
}

.file-section-content {
  padding: 0 20px 20px 20px;
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

/* 方法选择区域样式 */
.method-selection-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.method-selection-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.method-categories {
  margin-bottom: 15px;
}

.method-category {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 10px;
}

.method-category.active {
  border-color: #409eff;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  background-color: #f5f7fa;
}

.method-category.active .category-header {
  background-color: #ecf5ff;
  border-bottom: 1px solid #ebeef5;
}

.category-header h4 {
  margin: 0;
  color: #303133;
}

.toggle-icon {
  font-size: 18px;
  font-weight: bold;
  color: #909399;
}

.category-methods {
  padding: 10px 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.method-tab {
  padding: 8px 16px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.method-tab:hover {
  background-color: #ecf5ff;
  border-color: #409eff;
}

.method-tab.active {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.method-content {
  flex: 1;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.method-content h4 {
  margin-top: 0;
}

.method-actions {
  text-align: center;
}

.execute-button {
  padding: 10px 20px;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.execute-button:hover {
  background-color: #85ce61;
}

.column-list-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.column-list-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.column-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
  overflow-y: auto;
}

.column-item {
  padding: 8px 12px;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
}

.column-item:last-child {
  border-bottom: none;
}

.chat-section {
  background: white;
  border-radius: 8px;


  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chat-header h2 {
  margin: 0;
  color: #303133;
}

.clear-chat-btn {
  padding: 5px 10px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.clear-chat-btn:hover {
  background-color: #ff4d4f;
}

.chat-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #303133;
}

.chat-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 500px;
}

.messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 4px;
  max-width: 80%;
}

.message.sent {
  background-color: #409eff;
  color: white;
  margin-left: auto;
}

.message.received {
  background-color: #f5f5f5;
  color: #303133;
}

.message-content-wrapper {
  position: relative;
}

.copy-button {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 12px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.message:hover .copy-button {
  opacity: 1;
}

.copy-button:hover {
  background-color: #409eff;
  color: white;
}

.copy-button.copied {
  background-color: #67c23a;
  color: white;
  opacity: 1;
}

.typing-indicator {
  display: inline-block;
  width: 20px;
  height: 20px;
  position: relative;
}

.typing-indicator span {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #409eff;
  margin: 0 2px;
  animation: typing 1s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.input-area {
  display: flex;
  padding: 20px;
  border-top: 1px solid #ddd;
}

.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
}

.input-area input:disabled {
  background-color: #f5f7fa;
  cursor: not-allowed;
}

.input-area button {
  padding: 10px 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-area button:disabled {
  background-color: #a0cfff;
  cursor: not-allowed;
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
}

/* 下载文件链接样式 */
.download-file-link {
  color: #67c23a;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
}

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

/* 方法描述区域样式 */
.method-description-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  flex: 0 0 auto;
}

.method-description-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.method-content {
  flex: 1;
  margin-bottom: 0;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.method-content h4 {
  margin-top: 0;
}

.method-actions {
  flex: 0 0 auto;
  text-align: center;
  align-self: flex-start;
  margin-top: 15px;
}

.execute-button {
  padding: 10px 20px;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.execute-button:hover {
  background-color: #85ce61;
}

@media (max-width: 768px) {
  .dashboard-content {
    flex-direction: column;
    height: auto;
  }
  
  .left-section,
  .middle-section,
  .right-section {
    padding: 0 10px;
    max-height: none;
  }
  
  .file-list {
    max-height: 250px;
  }
  
  .chat-box {
    min-height: 300px;
  }
  
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
