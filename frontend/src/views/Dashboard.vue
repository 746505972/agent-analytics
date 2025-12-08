<template>
  <div class="dashboard-container">
    <!-- 导航栏 -->
    <DashboardHeader 
      :is-file-section-collapsed="isFileSectionCollapsed"
      :selected-file="selectedFile"
      :files="files"
      :analysis-history="analysisHistory"
      :current-method="currentMethod"
      @toggle-file-section="toggleFileSection"
      @load-analysis-from-history="loadAnalysisFromHistory"
      @remove-from-history="removeFromHistory"
      @show-preview="showDataPreview"
    />
    
    <!-- 文件选择悬浮区域 -->
    <FileSelectionOverlay 
      v-if="!isFileSectionCollapsed"
      :files="files"
      :selected-file="selectedFile"
      @select-file="selectFile"
      @delete-file="deleteFile"
      @close="closeFileSelection"
      @show-preview="showDataPreview"
      @download-file="downloadFile"
    />
    
    <div class="dashboard-content">
      <!-- 左侧：方法选择区域 -->
      <div class="left-section">
        <!-- 方法选择区域移到左栏 -->
        <MethodSelection
          v-if="selectedFile"
          :method-categories="methodCategories"
          :current-method="currentMethod"
          :expanded-categories="expandedCategories"
          @select-method="handleSelectMethod"
          @toggle-category="toggleCategory"
        />
        <div v-else>
            请选择一个文件
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
          
          <ResultContent
            :current-method="currentMethod"
            :dataset-details="datasetDetails"
            :loading-details="loadingDetails"
          />
        </div>
        
        <!-- 参数配置区 -->
        <div v-else class="config-section">
          <!-- 方法描述和执行按钮 -->
          <MethodDescription
            v-if="selectedFile"
            :current-method="currentMethod"
            :header-edit-mode="headerEditMode"
            @update:headerEditMode="handleHeaderModeChange"
            @apply-header-names="applyHeaderNames"
            @execute-invalid-samples="executeInvalidSamples"
            @execute-missing-value-interpolation="executeMissingValueInterpolation"
            @execute-delete-columns="executeDeleteColumns"
            @execute-method="executeMethod"
            @execute-data-transformation="executeDataTransformation"
          />
          <!-- 加载指示器 -->
          <div v-if="isWaitingForResponse" class="loading-overlay">
            <div class="loading-content">
              <img src="@/assets/images/loading.gif" alt="Loading..." class="loading-gif" />
              <p>正在处理中...</p>
            </div>
          </div>
          <!-- 列名列表和参数配置区域 -->
          <MethodParameterConfig
            v-else
            :current-method="currentMethod"
            :selected-file="selectedFile"
            :selected-file-columns="selectedFileColumns"
            :selected-columns="selectedColumns"
            :header-edit-mode="headerEditMode"
            :new-column-names="newColumnNames"
            :remove-duplicates="removeDuplicates"
            :remove-duplicates-cols="removeDuplicatesCols"
            :remove-constant-cols="removeConstantCols"
            :row-missing-threshold="rowMissingThreshold"
            :column-missing-threshold="columnMissingThreshold"
            :interpolation-method="interpolationMethod"
            :fill-value="fillValue"
            :knn-neighbors="knnNeighbors"
            :last-selected-column-index="lastSelectedColumnIndex"
            :data-transformation-config="dataTransformationConfig"
            :correlation-method="correlationMethod"
            @update:removeDuplicates="removeDuplicates = $event"
            @update:removeDuplicatesCols="removeDuplicatesCols = $event"
            @update:removeConstantCols="removeConstantCols = $event"
            @update:rowMissingThreshold="rowMissingThreshold = $event"
            @update:columnMissingThreshold="columnMissingThreshold = $event"
            @update:interpolationMethod="interpolationMethod = $event"
            @update:fillValue="fillValue = $event"
            @update:knnNeighbors="knnNeighbors = $event"
            @update:newColumnNames="handleNewColumnNamesUpdate"
            @update:dataTransformationConfig="updateDataTransformationConfig"
            @update:correlationMethod="correlationMethod = $event"
            @toggleColumnSelection="handleToggleColumnSelection"
          />
        </div>
      </div>

      <!-- 右侧：聊天分析区域 -->
      <div :class="['right-section', { collapsed: isRightSectionCollapsed }]">
        <div class="collapse-toggle" @click="toggleRightSection">
          {{ isRightSectionCollapsed ? '<' : '>' }}
        </div>
        <div v-show="!isRightSectionCollapsed">
          <ChatAssistant 
            :selected-file="selectedFile"
            :files="files"
            @refresh-files="loadUploadedFiles"
          />
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
          <DataPreview
            v-if="!previewData.loading"
            :column-headers="previewData.columnHeaders"
            :row-data="previewData.rowData"
            :total-rows="previewData.totalRows"
            :total-pages="previewData.totalPages"
            :current-page="previewData.currentPage"
            :header-width="previewData.headerWidth"
            :document-name="previewData.documentName"
            @prev-page="prevPage"
            @next-page="nextPage"
            @change-page="changePage"
          />
          <div class="loading-section" v-else>
            <div class="loading-spinner">加载中...</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import DataPreview from "@/components/DataPreview.vue";
import ChatAssistant from "@/components/ChatAssistant.vue";
import ResultContent from "@/components/ResultContent.vue";
import MethodDescription from "@/components/MethodDescription.vue";
import MethodSelection from "@/components/MethodSelection.vue";
import FileSelectionOverlay from "@/components/FileSelectionOverlay.vue";
import DashboardHeader from "@/components/DashboardHeader.vue";
import MethodParameterConfig from "@/components/Config/MethodParameterConfig.vue";
import { executeDataTransformation } from "@/api/dataTransformation.js";
import { executeDeleteColumns, executeMissingValueInterpolation } from "@/api/columnOperations.js";
import { applyHeaderNames } from "@/api/headerOperations.js";
import { 
  generateDataTransformationFeedback, 
  generateDeleteColumnsFeedback, 
  generateMissingValueInterpolationFeedback,
  generateInvalidSamplesFeedback
} from "@/api/feedbackHandler.js";
import { getMethodName } from "@/utils/methodUtils.js";

export default {
  name: "Dashboard",
  components: {
    MethodParameterConfig, FileSelectionOverlay, MethodDescription, ResultContent,
    DataPreview, ChatAssistant, DashboardHeader, MethodSelection
  },
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
      selectedFileColumns: [], // 用于显示选择的文件的列名
      selectedColumns: [], // 用于插值法选中的列
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
            { id: 'invalid_samples', name: '无效样本' }, // 已实现
            { id: 'delete_columns', name: '删除列' }, // 已实现
            { id: 'data_transformation', name: '数据转换' }, // 已实现
            { id: 'missing_value_interpolation', name: '插值法' }, // 已实现
            { id: 'add_header', name: '添加/修改标题行' }, // 已实现

          ]
        },
        {
          id: 'statistics',
          name: '统计方法',
          methods: [
            { id: 'basic_info', name: '基本信息' }, // 已实现
            { id: 'statistical_summary', name: '统计摘要' }, // 已实现
            { id: 'correlation_analysis', name: '相关性分析' }, // 已实现
            { id: 't_test', name: 'T检验' },
            { id: 'f_test', name: 'F检验' },
            { id: 'chi_square_test', name: '卡方检验' },
            { id: 'linear_regression', name: '线性回归' },
            { id: 'normality_test', name: '正态性检验' },
            { id: 'non_parametric_test', name: '非参数检验' }
          ]
        },
        {
          id: 'ml',
          name: '机器学习',
          methods: [
            { id: 'clustering', name: '聚类分析' },
            { id: 'classification', name: '分类分析' },
            { id: 'logistic_regression', name: '逻辑回归' },
            { id: 'decision_tree', name: '决策树' },
            { id: 'random_forest', name: '随机森林' },
            { id: 'knn', name: 'KNN' },
            { id: 'naive_bayes', name: '朴素贝叶斯' },
            { id: 'svm', name: '支持向量机' },
            { id: 'neural_network', name: '神经网络' },
            { id: 'xgboost', name: 'XGBoost' }
          ]
        },
        {
          id: 'visualization',
          name: '可视化',
          methods: [
            { id: 'line_chart', name: '折线图' },
            { id: 'scatter_plot', name: '散点图' },
            { id: 'bar_chart', name: '柱状图' },
            { id: 'histogram', name: '直方图' },
            { id: 'pie_chart', name: '饼图' },
            { id: 'box_plot', name: '箱线图' }
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
      newColumnNames: [],
      headerEditMode: 'add',
      // 分析历史相关数据
      analysisHistory: [],
      // 控制中间区域显示内容的状态
      middleSectionView: 'config', // 'config' 表示参数配置区，'result' 表示结果渲染区
      // 数据集详情
      datasetDetails: null,
      loadingDetails: false,
      // 无效样本参数
      removeDuplicates: false,
      removeDuplicatesCols: false,
      removeConstantCols: false,
      rowMissingThreshold: 1,
      columnMissingThreshold: 1,
      // 插值法参数
      interpolationMethod: 'linear',
      fillValue: '',
      knnNeighbors: 5,
      lastSelectedColumnIndex: -1,
      // 数据转换相关配置
      dataTransformationConfig: {},
      // 相关性分析参数
      correlationMethod: 'pearson',
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
      this.headerEditMode = 'add';
      this.initializeColumnNames();
    }

    // 恢复分析历史
    this.restoreAnalysisHistory();
  },
  methods: {
    getMethodName,
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
    
    // 添加切换右侧区域显示/隐藏的方法
    toggleRightSection() {
      this.isRightSectionCollapsed = !this.isRightSectionCollapsed;
    },
    
    // 处理标题行模式切换
    handleHeaderModeChange(mode) {
      this.headerEditMode = mode;
      if (mode === 'modify' && this.selectedFileColumns.length > 0) {
        // 修改模式：填入当前列名
        this.newColumnNames = [...this.selectedFileColumns];
      } else if (mode === 'remove') {
        // 删除模式：不需要处理列名

      } else {
        // 添加模式：清空列名
        this.newColumnNames = new Array(this.selectedFileColumns.length).fill('');
      }
    },
    
    // 添加一个方法来确保在选择文件后正确初始化newColumnNames
    initializeColumnNames() {
      if (this.currentMethod === 'add_header') {
        if (this.headerEditMode === 'modify' && this.selectedFileColumns.length > 0) {
          // 修改模式：填入当前列名
          this.newColumnNames = [...this.selectedFileColumns];
        } else if (this.headerEditMode === 'add') {
          // 添加模式：清空列名
          this.newColumnNames = new Array(this.selectedFileColumns.length).fill('');
        }
        // 删除模式不需要处理列名
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
            // 确保在选择文件后正确初始化列名（特别是对于add_header方法）
            this.initializeColumnNames();
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
        this.headerEditMode = 'add'; // 修改：默认为添加模式
        // 初始化列名输入框为当前列名
        this.initializeColumnNames();
      }
    },
    
    handleSelectMethod(methodId) {
      this.selectMethod(methodId);
      this.switchToConfigView();
    },

    async executeMethod() {
      if (!this.selectedFile || !this.currentMethod) {
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
    
    // 添加无效样本处理方法
    async executeInvalidSamples() {
      if (!this.selectedFile) {
        alert('请先选择一个文件');
        return;
      }

      this.isWaitingForResponse = true;
      try {
        const response = await fetch(`/user/${this.selectedFile}/remove_invalid_samples`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            remove_duplicates: this.removeDuplicates,
            remove_duplicate_cols: this.removeDuplicatesCols,
            remove_constant_cols: this.removeConstantCols,
            row_missing_threshold: this.rowMissingThreshold,
            col_missing_threshold: this.columnMissingThreshold
          }),
          credentials: 'include'
        });

        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            // 刷新文件列表并选中处理后的新文件
            await this.loadUploadedFiles();
            await this.selectFile(result.data.data_id);
            
            // 显示处理统计信息
            const feedbackMessage = generateInvalidSamplesFeedback(result);
            alert(feedbackMessage);
          } else {
            console.error("处理无效样本失败:", result.error);
            alert("处理无效样本失败: " + result.error);
          }
        } else {
          console.error("处理无效样本请求失败，状态码:", response.status);
          alert("处理无效样本失败，状态码: " + response.status);
        }
      } catch (error) {
        console.error("处理无效样本时发生错误:", error);
        alert("处理无效样本时发生错误: " + error.message);
      } finally {
        this.isWaitingForResponse = false;
      }
    },

    handleNewColumnNamesUpdate({ index, value }) {
      // 创建一个新的数组副本
      const updatedColumnNames = [...this.newColumnNames];
      // 更新指定索引的值
      updatedColumnNames[index] = value;
      // 更新整个数组
      this.newColumnNames = updatedColumnNames;
    },
    
    // 更新数据转换配置
    updateDataTransformationConfig(config) {
      this.dataTransformationConfig = config;
    },
    
    handleToggleColumnSelection({ event, column, index }) {
      // 双重验证
      const interpolationMethods = ['missing_value_interpolation', 'delete_columns', 'data_transformation', 'statistical_summary', 'correlation_analysis'];

      if (!interpolationMethods.includes(this.currentMethod)) {
        return;
      }
      const lastIndex = this.lastSelectedColumnIndex;

      if (event.ctrlKey || event.metaKey) {
        // Ctrl+点击：切换单个列的选中状态
        const selectedIndex = this.selectedColumns.indexOf(column);
        if (selectedIndex === -1) {
          this.selectedColumns.push(column);
        } else {
          this.selectedColumns.splice(selectedIndex, 1);
        }
      } else if (event.shiftKey && lastIndex !== -1) {
        // Shift+点击：选择范围

        const start = Math.min(lastIndex, index);
        const end = Math.max(lastIndex, index);
        this.selectedColumns = [];
        for (let i = start; i <= end; i++) {
          this.selectedColumns.push(this.selectedFileColumns[i]);
        }
      } else {
        // 普通点击：只选中当前列
        this.selectedColumns = [column];
      }

      this.lastSelectedColumnIndex = index;
    },

    // 执行插值法
    async executeMissingValueInterpolation() {
      this.isWaitingForResponse = true;
      try {
        const interpolationConfig = {
          interpolationMethod: this.interpolationMethod,
          fillValue: this.fillValue,
          knnNeighbors: this.knnNeighbors
        };

        const result = await executeMissingValueInterpolation(
          this.selectedFile,
          this.selectedColumns,
          interpolationConfig
        );

        // 刷新文件列表并选中处理后的新文件
        await this.loadUploadedFiles();
        await this.selectFile(result.data.data_id);
        
        // 显示处理统计信息
        const feedbackMessage = generateMissingValueInterpolationFeedback(result);
        alert(feedbackMessage);
      } catch (error) {
        console.error("插值处理时发生错误:", error);
        alert("插值处理时发生错误: " + error.message);
      } finally {
        this.isWaitingForResponse = false;
      }
    },

    // 执行数据转换
    async executeDataTransformation() {
      this.isWaitingForResponse = true;
      try {
        const result = await executeDataTransformation(
          this.selectedFile, 
          this.selectedColumns, 
          this.dataTransformationConfig
        );
        
        // 刷新文件列表并选中处理后的新文件
        await this.loadUploadedFiles();
        await this.selectFile(result.data.data_id);
        
        // 显示处理统计信息
        const feedbackMessage = generateDataTransformationFeedback(result);
        alert(feedbackMessage);
      } catch (error) {
        console.error("数据转换处理时发生错误:", error);
        alert("数据转换处理时发生错误: " + error.message);
      } finally {
        this.isWaitingForResponse = false;
      }
    },

    // 执行删除列
    async executeDeleteColumns() {
      if (!this.selectedFile) {
        alert('请先选择一个文件');
        return;
      }

      if (this.selectedColumns.length === 0) {
        alert('请选择要删除的列');
        return;
      }

      this.isWaitingForResponse = true;
      try {
        const result = await executeDeleteColumns(this.selectedFile, this.selectedColumns);
        
        // 刷新文件列表并选中处理后的新文件
        await this.loadUploadedFiles();
        await this.selectFile(result.data.data_id);
        
        // 显示成功信息
        const feedbackMessage = generateDeleteColumnsFeedback(result);
        alert(feedbackMessage);
        
        // 清空选中列
        this.selectedColumns = [];
      } catch (error) {
        console.error("删除列时发生错误:", error);
        alert("删除列时发生错误: " + error.message);
      } finally {
        this.isWaitingForResponse = false;
      }
    },

    switchToResultView() {
      this.middleSectionView = 'result';
    },
    // TODO:在这里添加清除参数
    switchToConfigView() {
      this.middleSectionView = 'config';
      this.selectedColumns=[]; // 用于插值法选中的列
      this.removeDuplicates= false;
      this.removeDuplicatesCols= false;
      this.removeConstantCols= false;
      this.rowMissingThreshold= 1;
      this.columnMissingThreshold= 1;
      // 插值法参数
      this.interpolationMethod= 'linear';
      this.fillValue= '';
      this.knnNeighbors= 5;
      this.lastSelectedColumnIndex= -1;
      this.newColumnNames= [];
      this.headerEditMode= 'add';  // 修改：统一使用字符串类型，默认为添加模式
      // 数据转换配置重置
      this.dataTransformationConfig = {};
      // 相关性分析参数重置
      this.correlationMethod = 'pearson';
    },
    
    // 调用API获取分析结果
    async fetchAnalysisResult(dataId, method) {
      try {
        this.isWaitingForResponse = true;
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
        } else if (method === 'statistical_summary') {
          // 准备请求体，包含选中的列
          const requestBody = {};
          if (this.selectedColumns && this.selectedColumns.length > 0) {
            requestBody.columns = this.selectedColumns;
          }
          
          const response = await fetch(`/data/${dataId}/statistical_summary`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody),
            credentials: 'include'
          });
          
          if (response.ok) {
            const result = await response.json();
            if (result.success) {
              return result.data;
            } else {
              console.error("获取统计摘要失败:", result.error);
              return null;
            }
          } else {
            console.error("获取统计摘要失败，状态码:", response.status);
            return null;
          }
        } else if (method === 'correlation_analysis') {
          // 准备请求体，包含选中的列和方法
          const requestBody = {
            method: this.correlationMethod
          };
          
          if (this.selectedColumns && this.selectedColumns.length > 0) {
            requestBody.columns = this.selectedColumns;
          }
          
          const response = await fetch(`/data/${dataId}/correlation_analysis`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody),
            credentials: 'include'
          });
          
          if (response.ok) {
            const result = await response.json();
            if (result.success) {
              return result.data;
            } else {
              console.error("获取相关性分析结果失败:", result.error);
              return null;
            }
          } else {
            console.error("获取相关性分析结果失败，状态码:", response.status);
            return null;
          }
        }
        // 其他分析方法可以在这里添加
        return null;
      } catch (error) {
        console.error("加载分析结果失败:", error);
        return null;
      } finally {
        this.isWaitingForResponse = false;
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

      this.isWaitingForResponse = true;
      try {
        const result = await applyHeaderNames(
          this.selectedFile, 
          this.newColumnNames, 
          this.headerEditMode
        );
            
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
      } catch (error) {
        console.error("添加标题行时发生错误:", error);
        alert("添加标题行时发生错误: " + error.message);
      } finally {
        this.isWaitingForResponse = false;
      }
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
        this.headerEditMode = 'modify'; // 修改：默认为修改模式
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
  flex: 0 0 20px;
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

.config-section,
.result-section {
  display: flex;
  flex-direction: column;
  height: 100%;
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

.loading-spinner {
  text-align: center;
  padding: 50px;
  color: #409eff;
  font-size: 16px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
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

.loading-overlay {
  width: 100%;
  height: 100%;
  background-color: rgb(241, 241, 241);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.loading-content {
  text-align: center;
}

.loading-gif {
  width: 50px;
  height: 50px;
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
  
  .preview-modal-content {
    width: 95%;
    height: 95%;
  }
  
  .preview-body {
    padding: 10px;
  }
}
</style>
