<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <div class="header-content">
        <div class="file-selector-trigger" @click="toggleFileSection">
          <h3>选择分析文件</h3>
          <span class="toggle-icon">{{ isFileSectionCollapsed ? '+' : '-' }}</span>
        </div>
        <div v-if="selectedFile" class="selected-file-info">
          当前选中: {{ getSelectedFileName() }}
        </div>
        <h2>欢迎使用 Agent-Analytics 智能数据分析平台</h2>
          <a href="https://github.com/746505972/agent-analytics" target="_blank" class="github-link">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="20" alt="GitHub">
          </a>
      </div>
    </div>
    
    <!-- 分析历史区域 -->
    <div class="analysis-history" v-if="analysisHistory.length > 0">
      <div class="history-title">分析历史:</div>
      <div class="history-buttons">
        <div
          v-for="(historyItem, index) in analysisHistory"
          :key="index"
          class="history-item"
          :class="{ active: isHistoryItemActive(historyItem) }"
        >
          <button
            @click="loadAnalysisFromHistory(historyItem)"
            class="history-button"
          >
            {{ getMethodName(historyItem.method) }}{{ index + 1 }}
          </button>
          <button
            @click="removeFromHistory(index)"
            class="delete-history-button"
          >
            ×
          </button>
        </div>
      </div>
    </div>

    <!-- 文件选择悬浮区域 -->
    <div v-if="!isFileSectionCollapsed" class="file-selection-overlay" v-click-outside="closeFileSelection">
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
    
    <div class="dashboard-content">
      <!-- 左侧：方法选择区域 -->
      <div class="left-section">
        <!-- 方法选择区域移到左栏 -->
        <div v-if="selectedFile" class="method-selection-section">

          <div class="method-categories">
            <div 
              v-for="category in methodCategories" 
              :key="category.id"
              class="method-category"
              :class="{ active: expandedCategories.includes(category.id) }"
            >
              <div class="category-header" @click="toggleCategory(category.id)">
                <h4>{{ category.name }}</h4>
                <span class="toggle-icon">{{ expandedCategories.includes(category.id) ? '−' : '+' }}</span>
              </div>
              <div v-show="expandedCategories.includes(category.id)" class="category-methods">
                <button 
                  v-for="method in category.methods" 
                  :key="method.id"
                  :class="{ active: currentMethod === method.id }"
                  @click="selectMethod(method.id) ; switchToConfigView()"
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
        <!-- 结果渲染区 -->
        <div v-if="middleSectionView === 'result'" class="result-section">
          <div class="result-header">
            <button @click="switchToConfigView" class="back-button">← 返回参数配置</button>
            <h2>{{ getMethodName(currentMethod) }}分析结果</h2>
          </div>
          
          <div class="result-content">
            <!-- 基本信息分析结果 -->
            <div v-if="currentMethod === 'basic_info' && datasetDetails" class="analysis-section">
              <div class="basic-info-details">
                <h3>数据集基本信息</h3>
                <div class="info-grid">
                  <div class="info-item">
                    <span class="info-label">文件名:</span>
                    <span class="info-value">{{ datasetDetails.filename }}</span>
                  </div>
                  <div class="info-item">
                    <div>
                      <span class="info-label">行数:</span>
                      <span class="info-value">{{ datasetDetails.rows.toLocaleString() }}</span>
                    </div>
                    <div>
                      <span class="info-label">列数:</span>
                      <span class="info-value">{{ datasetDetails.columns.toLocaleString() }}</span>
                    </div>
                  </div>
                  <div class="info-item">
                    <div>
                      <span class="info-label">完整性:</span>
                      <span class="info-value">{{ (datasetDetails.completeness * 100).toFixed(2) }}%</span>
                    </div>
                    <div>
                      <span class="info-label">总单元格数:</span>
                      <span class="info-value">{{ datasetDetails.total_cells.toLocaleString() }}</span>
                    </div>
                    <div>
                      <span class="info-label">缺失值总数:</span>
                      <span class="info-value">{{ datasetDetails.total_missing.toLocaleString() }}</span>
                    </div>
                  </div>
                </div>
                
                <h4>列信息:</h4>
                <div class="column-table-container">
                  <table class="column-table">
                    <thead>
                      <tr>
                        <th>列名</th>
                        <th>数据类型</th>
                        <th>缺失值数量</th>
                        <th>列完整性</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(dtype, columnName) in datasetDetails.dtypes" :key="columnName">
                        <td>{{ columnName }}</td>
                        <td>{{ dtype }}</td>
                        <td>{{ datasetDetails.missing_values[columnName].toLocaleString() || 0 }}</td>
                        <td>{{ (datasetDetails.completeness_values[columnName] * 100).toFixed(2) + '%' || 'unknown' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h4>数值型列统计信息:</h4>
                <div class="stats-table-container">
                  <table class="stats-table">
                    <thead>
                      <tr>
                        <th>列名</th>
                        <th>最小值</th>
                        <th>最大值</th>
                        <th>平均值</th>
                        <th>标准差</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(stats, columnName) in datasetDetails.numeric_stats" :key="columnName">
                        <td>{{ columnName }}</td>
                        <td>{{ stats.min !== null ? stats.min.toLocaleString() : 'N/A' }}</td>
                        <td>{{ stats.max !== null ? stats.max.toLocaleString() : 'N/A' }}</td>
                        <td>{{ stats.mean !== null ? Number(stats.mean.toFixed(2)).toLocaleString() : 'N/A' }}</td>
                        <td>{{ stats.std !== null ? Number(stats.std.toFixed(2)).toLocaleString() : 'N/A' }}</td>
                      </tr>
                      <tr v-if="Object.keys(datasetDetails.numeric_stats).length === 0">
                        <td colspan="5" class="no-data">无数值型列</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h4>分类型列统计信息:</h4>
                <div class="stats-table-container">
                  <table class="stats-table">
                    <thead>
                      <tr>
                        <th>列名</th>
                        <th>唯一值数量</th>
                        <th>常见值</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(stats, columnName) in datasetDetails.categorical_stats" :key="columnName">
                        <td>{{ columnName }}</td>
                        <td>{{ stats.unique_count }}</td>
                        <td>
                          <div v-for="(count, value) in stats.top_values" :key="value" class="top-value-item">
                            <span class="highlight-param">{{ value }}</span> 出现 <span class="highlight-param">{{ count }}</span> 次
                          </div>
                        </td>
                      </tr>
                      <tr v-if="Object.keys(datasetDetails.categorical_stats).length === 0">
                        <td colspan="3" class="no-data">无分类型列</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <h4>前5行数据预览:</h4>
                <div class="data-preview">
                  <table>
                    <thead>
                      <tr>
                        <th v-for="col in datasetDetails.column_names" :key="col">{{ col }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, index) in datasetDetails.head" :key="index">
                        <td v-for="col in datasetDetails.column_names" :key="col">{{ row[col] }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            
            <!-- 统计摘要分析结果 -->
            <div v-else-if="currentMethod === 'statistical_summary'" class="analysis-section">
              <h3>统计摘要</h3>
              <p>此功能正在开发中...</p>
            </div>
            
            <!-- 数据可视化分析结果 -->
            <div v-else-if="currentMethod === 'visualization'" class="analysis-section">
              <h3>数据可视化</h3>
              <p>此功能正在开发中...</p>
            </div>
            
            <!-- 机器学习分析结果 -->
            <div v-else-if="currentMethod === 'ml_analysis'" class="analysis-section">
              <h3>机器学习分析</h3>
              <p>此功能正在开发中...</p>
            </div>
            
            <!-- 加载状态 -->
            <div v-else-if="loadingDetails" class="analysis-section">
              <div class="loading-spinner">加载分析结果中...</div>
            </div>
            
            <!-- 错误状态 -->
            <div v-else class="analysis-section">
              <p>无法加载分析结果</p>
            </div>
          </div>
        </div>
        
        <!-- 参数配置区 -->
        <div v-else class="config-section">
          <!-- 方法描述和执行按钮移到中栏 -->
          <div v-if="selectedFile" class="method-description-section">
            <div class="method-description-content">
              <div class="method-content">
                <div v-if="currentMethod === 'basic_info'">
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
                <div v-else-if="currentMethod === 'add_header'" class="add-header-method">
                  <h4>添加/修改标题行</h4>
                  <p>为没有标题行的文件添加自定义列名，或修改现有标题行。</p>
                  <div class="header-mode-toggle">
                    <label>
                      <input 
                        type="radio" 
                        v-model="headerEditMode" 
                        :value="false" 
                        @change="handleHeaderModeChange"
                      > 添加标题行
                    </label>
                    <label>
                      <input 
                        type="radio" 
                        v-model="headerEditMode" 
                        :value="true" 
                        @change="handleHeaderModeChange"
                      > 修改标题行
                    </label>
                    <label>
                      <input 
                        type="radio" 
                        v-model="headerEditMode" 
                        value="remove" 
                        @change="handleHeaderModeChange"
                      > 删除首行
                    </label>
                  </div>
                </div>
              </div>
              <div class="method-actions">
                <button 
                  v-if="currentMethod === 'add_header'"
                  @click="applyHeaderNames"
                  class="execute-button"
                >
                  应用标题
                </button>
                <button
                  v-else-if="currentMethod === 'data_cleaning'"
                  @click=""
                  class="execute-button"
                >
                  执行清洗
                </button>
                <button 
                  v-else
                  @click="executeMethod"
                  class="execute-button"
                >
                  执行分析
                </button>
              </div>
            </div>
          </div>
          
          <!-- 列名列表和添加标题行区域 -->
          <div v-if="selectedFile && selectedFileColumns.length > 0" class="column-add-header-container">
            <!-- 列名列表区域 -->
            <div class="column-list-section">
              <h3>列名列表</h3>
              <ul class="column-list">
                <li v-for="(column, index) in selectedFileColumns" :key="index" class="column-item">
                  {{ column }}
                </li>
              </ul>
            </div>
            
            <!-- 添加标题行操作区域 -->
            <div v-if="currentMethod === 'add_header' && headerEditMode !== 'remove'" class="add-header-section">
              <h3>设置列名</h3>
              <div class="add-header-content">
                <div class="column-inputs">
                  <div 
                    v-for="(column, index) in selectedFileColumns" 
                    :key="index" 
                    class="column-input-item"
                  >
                    <input 
                      :id="'column-' + index"
                      v-model="newColumnNames[index]" 
                      :placeholder="'列' + (index + 1)"
                      type="text"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div v-else-if="currentMethod === 'data_cleaning'" class="add-header-section">
              <h3>设置参数</h3>
              <div class="add-header-content">
                <div class="data-cleaning-options">
                  <div class="option-row">
                    <label>
                      <input 
                        type="checkbox" 
                        v-model="removeDuplicates"
                      /> 去除重复行
                    </label>
                  </div>
                  <div class="option-row">
                    <label>
                      行缺失阈值:
                      <input 
                        type="number" 
                        v-model="rowMissingThreshold" 
                        min="0" 
                        max="1" 
                        step="0.01"
                        class="threshold-input"
                      />
                    </label>
                  </div>
                  <div class="option-row">
                    <label>
                      列缺失阈值:
                      <input 
                        type="number" 
                        v-model="columnMissingThreshold" 
                        min="0" 
                        max="1" 
                        step="0.01"
                        class="threshold-input"
                      />
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：聊天分析区域 -->
      <div :class="['right-section', { collapsed: isRightSectionCollapsed }]">
        <div class="collapse-toggle" @click="toggleRightSection">
          {{ isRightSectionCollapsed ? '<' : '>' }}
        </div>
        <div v-show="!isRightSectionCollapsed" class="chat-section">
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
    
    <!-- 添加标题行弹窗 -->
    <div class="add-header-modal" v-if="showAddHeaderModal">
      <div class="add-header-modal-content">
        <div class="add-header-modal-header">
          <h3>添加标题行</h3>
          <button class="close-button" @click="closeAddHeaderModal">×</button>
        </div>
        <div class="add-header-modal-body">
          <p>正在为文件添加标题行，请稍候...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';

export default {
  name: "Dashboard",
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
      isFileSectionCollapsed: true, // 默认收起文件选择区域
      isWaitingForResponse: false,
      // 添加折叠右侧区域的状态
      isRightSectionCollapsed: false,
      // 新增方法选择相关数据
      currentMethod: 'basic_info',
      expandedCategories: ['statistics', 'ml', 'visualization', 'nlp', 'data_processing'], // 默认全部展开
      methodCategories: [
        {
          id: 'data_processing',
          name: '数据处理',
          methods: [
            { id: 'data_cleaning', name: '数据清洗' },
            { id: 'data_transformation', name: '数据转换' },
            { id: 'add_header', name: '添加/修改标题行' }
          ]
        },
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
      },
      // 添加标题行相关数据
      showAddHeaderModal: false,
      newColumnNames: [],
      headerEditMode: true,  // 修改：默认为修改模式
      // 分析历史相关数据
      analysisHistory: [],
      // 控制中间区域显示内容的状态
      middleSectionView: 'config', // 'config' 表示参数配置区，'result' 表示结果渲染区
      // 数据集详情
      datasetDetails: null,
      loadingDetails: false,
      // 数据清洗参数
      removeDuplicates: false,
      rowMissingThreshold: 1,
      columnMissingThreshold: 1
    }
  },
  async mounted() {
    await this.loadUploadedFiles();
    // 恢复保存的状态
    this.restoreState();
    // 检查是否有刚上传的文件需要默认选中
    this.checkAndSelectUploadedFile();
    
    // 初始化列名输入框状态
    if (this.currentMethod === 'add_header') {
      this.headerEditMode = true;
      if (this.selectedFileColumns.length > 0) {
        this.newColumnNames = [...this.selectedFileColumns];
      }
    }

    // 恢复分析历史
    this.restoreAnalysisHistory();
  },
  methods: {
    // 清除localStorage中的数据
    clearLocalStorage() {
      // 清除与文件相关的localStorage项
      localStorage.removeItem('currentDataId');
      localStorage.removeItem('dashboardChatMessages');
      localStorage.removeItem('analysisHistory');
      localStorage.removeItem('selectedMethod');
      localStorage.removeItem('selectedFile');
      localStorage.removeItem('isFileSectionCollapsed');
      localStorage.removeItem('session_id');
    },

    // 添加获取方法名称的方法
    getMethodName(methodId) {
      const methods = {
        'basic_info': '基本信息',
        'statistical_summary': '统计摘要',
        'correlation_analysis': '相关性分析',
        'distribution_analysis': '分布分析',
        'visualization': '数据可视化',
        'ml_analysis': '机器学习分析',
        'clustering': '聚类分析',
        'classification': '分类分析',
        'regression': '回归分析',
        'text_analysis': '文本分析',
        'sentiment_analysis': '情感分析',
        'data_cleaning': '数据清洗',
        'data_transformation': '数据转换',
        'add_header': '添加/修改标题行'
      };
      return methods[methodId] || '未知分析';
    },


    removeFromHistory(index) {
      // 从历史记录中移除
      this.analysisHistory.splice(index, 1);

      // 更新localStorage
      localStorage.setItem('analysisHistory', JSON.stringify(this.analysisHistory));
    },

    restoreAnalysisHistory() {
      // 从localStorage恢复分析历史
      const savedHistory = localStorage.getItem('analysisHistory');
      if (savedHistory) {
        try {
          this.analysisHistory = JSON.parse(savedHistory);
        } catch (e) {
          console.error("解析分析历史失败:", e);
          this.analysisHistory = [];
        }
      }
    },

    // goToAnalysis(dataId, method) {
    //   // 跳转到分析页面
    //   // Analysis.vue已弃用
    //   this.$router.push({
    //     name: 'Analysis',
    //     query: {
    //       data_id: dataId,
    //       method: method
    //     }
    //   });
    // },

    // 从历史记录加载分析结果
    async loadAnalysisFromHistory(historyItem) {
      // 设置当前选中的文件和方法
      this.selectedFile = historyItem.dataId;
      this.currentMethod = historyItem.method;
      
      // 保存选中的文件和方法到localStorage
      localStorage.setItem('selectedFile', this.selectedFile);
      localStorage.setItem('selectedMethod', this.currentMethod);
      
      // 获取文件的列名信息
      await this.selectFile(this.selectedFile);
      
      // 如果历史记录中有结果数据，则直接显示
      if (historyItem.result) {
        this.datasetDetails = historyItem.result;
        this.switchToResultView();
      } else {
        // 否则执行方法获取结果
        await this.executeMethod();
      }
    },

    // 添加检查历史记录项是否为当前选中项的方法
    isHistoryItemActive(historyItem) {
      return this.selectedFile === historyItem.dataId && this.currentMethod === historyItem.method;
    },
    
    // 添加切换右侧区域显示/隐藏的方法
    toggleRightSection() {
      this.isRightSectionCollapsed = !this.isRightSectionCollapsed;
    },
    
    // 添加Markdown渲染方法
    renderMarkdown(content) {
      if (!content) return '';
      return marked.parse(content);
    },
    
    // 处理标题行模式切换
    handleHeaderModeChange() {
      if (this.headerEditMode === true && this.selectedFileColumns.length > 0) {
        // 修改模式：填入当前列名
        this.newColumnNames = [...this.selectedFileColumns];
      } else if (this.headerEditMode === 'remove') {
        // 删除模式：不需要处理列名

      } else {
        // 添加模式：清空列名
        this.newColumnNames = new Array(this.selectedFileColumns.length).fill('');
      }
    },
    
    toggleFileSection(event) {
      // 阻止事件冒泡，避免触发clickOutside
      if (event) {
        event.stopPropagation();
      }
      
      this.isFileSectionCollapsed = !this.isFileSectionCollapsed;
      // 保存文件选择区域的展开/收起状态到localStorage
      localStorage.setItem('isFileSectionCollapsed', this.isFileSectionCollapsed.toString());
    },
    
    // 关闭文件选择区域
    closeFileSelection() {
      this.isFileSectionCollapsed = true;
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
            this.session_id = result.session_id;
            const storedSessionId = localStorage.getItem('session_id');
            if (storedSessionId && this.session_id !== storedSessionId) {
              // 如果session_id变化，清除localStorage中的数据
              this.clearLocalStorage();
              localStorage.setItem('session_id', this.session_id);
            }
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
            // 初始化新的列名数组
            this.newColumnNames = [...result.data.column_names]; // 默认填入原列名
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
      if (category && !this.expandedCategories.includes(category.id)) {
        this.expandedCategories.push(category.id);
        // 保存展开状态到localStorage
        localStorage.setItem('expandedCategories', JSON.stringify(this.expandedCategories));
      }
      
      // 如果选择的是添加标题行方法，设置编辑模式
      if (methodId === 'add_header') {
        this.headerEditMode = true; // 修改：默认为修改模式
        // 初始化列名输入框为当前列名
        if (this.selectedFileColumns.length > 0) {
          this.newColumnNames = [...this.selectedFileColumns];
        }
      }
    },
    async executeMethod() {
      if (!this.selectedFile || !this.currentMethod) {
        return;
      }
      
      // 如果是添加标题行方法，不跳转到分析页面，而是在当前页面处理
      if (this.currentMethod === 'add_header') {
        // 显示添加标题行的UI
        return;
      }
      
      // 保存聊天记录到localStorage
      localStorage.setItem('dashboardChatMessages', JSON.stringify(this.chatMessages));
      
      // 保存文件选择区域的展开/收起状态
      localStorage.setItem('isFileSectionCollapsed', this.isFileSectionCollapsed.toString());
      
      // 保存当前选中的方法
      localStorage.setItem('selectedMethod', this.currentMethod);
      
      // 直接调用API获取分析结果
      this.loadingDetails = true;
      const result = await this.fetchAnalysisResult(this.selectedFile, this.currentMethod);
      this.loadingDetails = false;
      
      if (result) {
        // 将结果保存到历史记录中
        this.addToHistory(this.selectedFile, this.currentMethod, result);
        
        // 设置分析结果数据
        this.datasetDetails = result;
        
        // 切换到结果视图
        this.switchToResultView();
      }
    },
    
    switchToResultView() {
      this.middleSectionView = 'result';
    },
    
    switchToConfigView() {
      this.middleSectionView = 'config';
    },
    
    // 调用API获取分析结果
    async fetchAnalysisResult(dataId, method) {
      try {
        if (method === 'basic_info') {
          const response = await fetch(`/data/${dataId}/details`, {
            credentials: 'include'
          });
          
          if (response.ok) {
            const result = await response.json();
            if (result.success) {
              return result.data;
            } else {
              console.error("获取分析结果失败:", result.error);
              return null;
            }
          } else {
            console.error("获取分析结果失败，状态码:", response.status);
            return null;
          }
        }
        // 其他分析方法可以在这里添加
        return null;
      } catch (error) {
        console.error("加载分析结果失败:", error);
        return null;
      }
    },
    
    // 修改添加到历史记录的方法，增加result参数
    addToHistory(dataId, method, result) {
      // 添加到历史记录
      this.analysisHistory.push({
        dataId,
        method,
        result // 保存结果
      });

      // 保存到localStorage
      localStorage.setItem('analysisHistory', JSON.stringify(this.analysisHistory));
    },

    // 应用自定义标题行
    async applyHeaderNames() {
      if (!this.selectedFile) return;

      // 检查是否所有列都已命名（仅在非删除模式下）
      if (this.headerEditMode !== 'remove') {
        const emptyNames = this.newColumnNames.filter(name => !name.trim()).length;
        if (emptyNames > 0) {
          alert(`还有 ${emptyNames} 个列未命名，请为所有列提供名称。`);
          return;
        }
      }

      try {
        this.showAddHeaderModal = true;
        
        // 确定模式参数
        let mode = "add";
        if (this.headerEditMode === true) {
          mode = "modify";
        } else if (this.headerEditMode === 'remove') {
          mode = "remove";
        }
        
        const response = await fetch(`/data/${this.selectedFile}/add_header`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            column_names: this.newColumnNames,
            mode: mode  // 添加模式参数
          }),
          credentials: 'include'
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            // 自动选择新生成的文件
            await this.loadUploadedFiles(); // 刷新文件列表
            await this.selectFile(result.data.data_id); // 选择新文件
            
            // 显示成功消息
            if (this.headerEditMode === 'remove') {
              alert('首行删除成功，已自动选择新文件');
            } else if (this.headerEditMode) {
              alert('标题行修改成功，已自动选择新文件');
            } else {
              alert('标题行添加成功，已自动选择新文件');
            }
          } else {
            console.error("添加标题行失败:", result.error);
            alert("添加标题行失败: " + result.error);
          }
        } else {
          console.error("添加标题行请求失败，状态码:", response.status);
          alert("添加标题行失败，状态码: " + response.status);
        }
      } catch (error) {
        console.error("添加标题行时发生错误:", error);
        alert("添加标题行时发生错误: " + error.message);
      } finally {
        this.showAddHeaderModal = false;
      }
    },
    
    // 关闭添加标题行弹窗
    closeAddHeaderModal() {
      this.showAddHeaderModal = false;
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
      const savedExpandedCategories = localStorage.getItem('expandedCategories');
      if (savedExpandedCategories) {
        this.expandedCategories = JSON.parse(savedExpandedCategories);
      }
      
      // 初始化添加/修改标题行模式
      if (this.currentMethod === 'add_header') {
        this.headerEditMode = true; // 修改：默认为修改模式
        if (this.selectedFileColumns.length > 0) {
          this.newColumnNames = [...this.selectedFileColumns];
        }
      }
    },
    
    // 检查并选中刚上传的文件
    checkAndSelectUploadedFile() {
      // 从localStorage获取刚上传的文件ID
      const currentDataId = localStorage.getItem('currentDataId');
      if (currentDataId && this.files.some(file => file.data_id === currentDataId)) {
        // 如果有刚上传的文件且在文件列表中存在，则默认选中它
        this.selectFile(currentDataId);
      }
    },
    
    toggleCategory(categoryId) {
      const index = this.expandedCategories.indexOf(categoryId);
      if (index > -1) {
        // 如果已经展开，则收起
        this.expandedCategories.splice(index, 1);
      } else {
        // 如果收起，则展开
        this.expandedCategories.push(categoryId);
      }
      // 保存展开状态到localStorage
      localStorage.setItem('expandedCategories', JSON.stringify(this.expandedCategories));
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
        
        if (response.ok && response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let done = false;
          let accumulatedContent = "";
          let toolCalls = [];
          
          // 逐步接收流式响应
          while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;
            
            if (value) {
              const chunk = decoder.decode(value, { stream: true });
              const lines = chunk.split('\n');
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  
                  if (data === '[DONE]') {
                    done = true;
                    break;
                  }
                  
                  try {
                    const parsed = JSON.parse(data);
                    if (parsed.content !== undefined) {
                      accumulatedContent += parsed.content;
                      // 更新AI回复内容
                      this.chatMessages[aiMessageIndex].content = accumulatedContent;
                      // 滚动到底部并触发更新
                      await this.$nextTick(() => {
                        const messagesContainer = document.querySelector('.messages');
                        if (messagesContainer) {
                          messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        }
                      });
                                          
                      // 每累积一定字符数就强制更新DOM以实现实时显示效果
                      if (accumulatedContent.length % 5 === 0) {
                        await this.$nextTick();
                      }
                    } else if (parsed.tool_calls !== undefined) {
                      // 处理工具调用信息
                      toolCalls = parsed.tool_calls;
                      
                      // 如果是添加标题行工具，需要刷新文件列表并选中新文件
                      for (const toolCall of toolCalls) {
                        if (toolCall.name === 'add_header_tool') {
                          // 显示工具调用信息
                          const toolInfo = `
                            **工具调用详情:**
                            - 工具名称: ${toolCall.name}
                            - 参数: ${JSON.stringify(toolCall.args, null, 2)}`;
                          this.chatMessages[aiMessageIndex].content += toolInfo;
                          
                          // 等待一段时间后刷新文件列表
                          setTimeout(async () => {
                            await this.loadUploadedFiles();
                            // 查找新创建的文件并选中
                            const files = this.files;
                            // 查找最近添加的文件（根据文件名判断）
                            const newFile = files.find(file => 
                              file.filename.includes('_add_header_') || 
                              file.filename.includes('_modify_header_')
                            );
                            
                            if (newFile) {
                              await this.selectFile(newFile.data_id);
                              // 显示通知
                              this.showCopyNotification(`工具执行成功，已自动选中新文件: ${newFile.filename}`, false);
                            }
                          }, 1000);
                        } else {
                          // 显示其他工具调用信息
                          const toolInfo = `
                            **工具调用详情:**
                            - 工具名称: ${toolCall.name}
                            - 参数: ${JSON.stringify(toolCall.args, null, 2)}`;
                          this.chatMessages[aiMessageIndex].content += toolInfo;
                        }
                      }
                    } else if (parsed.error) {
                      this.chatMessages[aiMessageIndex].content = `错误: ${parsed.error}`;
                      done = true;
                    }
                  } catch (e) {
                    // 即使解析失败，也尝试显示原始内容
                    this.chatMessages[aiMessageIndex].content = `解析错误: ${data}`;
                    
                    // 强制更新DOM
                    await this.$nextTick();
                  }
                }
              }
            }
          }
        } else {
          this.chatMessages[aiMessageIndex].content = `抱歉，无法连接到AI助手。状态码: ${response.status}`;
        }
      } catch (error) {
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
    
    // 复制消息文本
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
      return file ? file.filename : "无";
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
  position: relative;
}

.dashboard-header {
  text-align: center;
  padding: 10px 0 10px 0 ;
  border-bottom: 1px solid #ebeef5;
  position: relative;
}

/* 分析历史区域样式 */
.analysis-history {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.history-title {
  font-weight: bold;
  margin-right: 15px;
  color: #303133;
}

.history-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.history-item {
  display: flex;
  align-items: center;
}

.history-item:not(.active) .history-button {
  background-color: #909399; /* 灰色 */
  color: #ffffff;
}

.history-item:not(.active) .history-button:hover {
  background-color: #a0a3a9;
}

.history-button {
  padding: 5px 10px;
  background-color: #409eff; /* 蓝色 */
  color: white;
  border: none;
  border-radius: 4px 0 0 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.history-button:hover {
  background-color: #66b1ff;
}

.delete-history-button {
  padding: 5px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.delete-history-button:hover {
  background-color: #ff4d4f;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 30px;
  position: relative;
}

.selected-file-info {
  display: flex;
  color: #909399;
  font-size: 14px;
  white-space: nowrap;
}

.file-selector-trigger {
  display: flex;
  align-items: center;
  gap: 40px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #f5f7fa;
  transition: background-color 0.3s;
  position: relative;
  z-index: 101;
}

.file-selector-trigger:hover {
  background-color: #e1e6ee;
}

.file-selector-trigger h3 {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.dashboard-header h2 {
  color: #303133;
  margin: 0;
}

/* 文件选择悬浮区域样式 */
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

.dashboard-content {
  display: flex;
  height: calc(100vh - 120px);
  padding: 0 1px;
  gap: 0;
  margin-top: 0;
}

.left-section {
  flex: 0.5;
  padding-left: 0;
  overflow-y: auto;
  max-height: 100%;
  border-right: 1px solid #ebeef5;
}

.middle-section {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  max-height: 100%;
}

.right-section {
  flex: 1;
  padding-right: 10px;
  overflow-y: auto;
  max-height: 100%;
  position: relative;
  transition: all 0.3s ease;
}

.right-section.collapsed {
  flex: 0 0 30px;
  padding: 0;
}

.collapse-toggle {
  position: absolute;
  top: 25px;
  transform: translateY(-50%);
  width: 20px;
  height: 40px;
  background-color: #419fff;
  color: white;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  font-weight: bold;
}

.chat-section {
  background: white;
  border-radius: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.config-section,
.result-section {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.section-header h3 {
  margin: 0;
  color: #303133;
}

.toggle-icon {
  font-size: 20px;
  font-weight: bold;
  color: #909399;
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
  padding-top: 10px;
  margin-bottom: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.method-selection-section h3 {
  margin-top: 0;
  padding-left: 10px;
  padding-bottom: 10px;
  margin-bottom: 10px;
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
  padding: 20px;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);*/
  flex: 1;
  display: flex;
  flex-direction: column;
  border-top: 1px solid #ededed;
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

/* 列名列表和添加标题行容器 */
.column-add-header-container {
  display: flex;
  gap: 0;
  flex: 1;
}

.result-header {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
  gap: 20px;
}

.result-header h2 {
  margin: 0;
  color: #303133;
}

.back-button {
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #66b1ff;
}

.result-content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.analysis-section {
  min-height: 500px;
}

.loading-spinner {
  text-align: center;
  padding: 50px;
  color: #409eff;
  font-size: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  overflow-wrap: break-word;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.info-label {
  font-size: 14px;
  color: #606266;
}

.info-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.column-details {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.column-item {
  display: flex;
  padding: 8px 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
}

.column-name {
  font-weight: bold;
  margin-right: 8px;
  color: #303133;
}

.column-type {
  color: #606266;
}

.data-preview {
  overflow-x: auto;
}

.data-preview table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.data-preview th,
.data-preview td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  white-space: nowrap;
}

.data-preview th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.stats-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.stats-table th,
.stats-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.stats-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.no-data {
  text-align: center;
  color: #909399;
  font-style: italic;
}

.top-value-item {
  margin-bottom: 3px;
}

.column-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.column-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.column-table th,
.column-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.column-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.highlight-param {
  font-family: 'Courier New', monospace;
}

/* 添加标题行区域样式 */
.add-header-section {
  background: white;
  padding: 20px;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ededed;
  border-top: 1px solid #ededed;
}

.add-header-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #303133;
}

.add-header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.header-mode-toggle {
  margin-bottom: 15px;
}

.header-mode-toggle label {
  margin-right: 15px;
  font-weight: normal;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.header-mode-toggle input[type="radio"] {
  margin-right: 5px;
}

.column-inputs {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.column-input-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
  margin-bottom: 0;
}

.column-input-item label {
  width: 100px;
  margin-right: 10px;
  color: #606266;
}

.column-input-item input {
  flex: 1;
  padding: 8px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
}

/* 添加标题行弹窗样式 */
.add-header-modal {
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

.add-header-modal-content {
  background: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  padding: 20px;
}

.add-header-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.add-header-modal-header h3 {
  margin: 0;
  color: #303133;
}

.header-mode-toggle {
  margin-top: 10px;
}

.header-mode-toggle label {
  margin-right: 15px;
  font-weight: normal;
  cursor: pointer;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
}

.add-header-modal-body {
  text-align: center;
  padding: 20px 0;
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
  margin-bottom: 0;
}

.chat-header h2 {
  padding-left: 20px;
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
  margin-top: 10px;
  margin-bottom: 10px;
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

/* 数据清洗选项样式 */
.data-cleaning-options {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.option-row {
  display: flex;
  align-items: center;
}

.option-row label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: normal;
  margin: 0;
}

.threshold-input {
  width: 80px;
  padding: 5px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
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
  padding: 0;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
  margin-bottom: 0;
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
  background-color: white;
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
  
  .header-content {
    flex-direction: column;
    gap: 10px;
  }
  
  .file-selection-overlay {
    width: 95%;
    top: 100px;
    left: 2.5%;
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
