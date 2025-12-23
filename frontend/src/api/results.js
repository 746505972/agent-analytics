/**
 * 获取分析结果的API函数
 * 根据不同的分析方法调用相应的后端接口
 */
export async function fetchResult(dataId, method, options = {}){
  if(method === 'line_chart' || method === 'data_visualization'){
    return await fetchCompleteData(dataId);
  }else{
    return await fetchAnalysisResult(dataId, method, options);
  }
}
/**
 * 获取完整数据
 * @param {string} dataId - 数据文件ID
 * @returns {Promise<Object|null>} 完整数据或null（如果失败）
 */
export async function fetchCompleteData(dataId) {
  try {
    const response = await fetch(`/data/${dataId}/complete`, {
      credentials: 'include'
    });

    const result = await response.json();
    if (result.success) {
      return result.data;
    } else {
      throw new Error(result.error || "获取完整数据失败");
    }
  } catch (error) {
    console.error("加载完整数据失败:", error);
    throw error;
  }
}

/**
 * 获取分析结果
 * @param {string} dataId - 数据文件ID
 * @param {string} method - 分析方法
 * @param {Object} options - 选项参数
 * @returns {Promise<Object>} 分析结果
 */
export async function fetchAnalysisResult(dataId, method, options = {}) {
  const { selectedColumns = [],
      configs =  {
        correlationMethod : 'pearson' ,
        wordcloudConfig: {
        color:['#FF274B'],
        maxWords: 200,
        width: 1600,
        height: 900,
        backgroundColor: "#ffffff",
        maxFontSize: 200,
        minFontSize: 10,
        stopwords: [],
        maskShape: "default"
        },
        sentimentConfig : {
          stopwords: [],
          internetSlang: {}
        },
        tTestConfig : {
          testType: 'one_sample',
          alpha: 0.05,
          popmean: 0,
          groupCol: '',
          equalVar: true,
          normalityMethod: 'shapiro'
        },
        normalityTestConfig : {
          method: 'shapiro',
          alpha: 0.05,
          groupBy: ''
        },
        fTestConfig : {
          groupBy: '',
          alpha: 0.05
        },
        chiSquareTestConfig : {
          groupBy: '',
          alpha: 0.05
        }
      },
} = options;
  
  try {
    if (method === 'basic_info') {
      const response = await fetch(`/data/${dataId}/details`, {
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取分析结果失败");
      }
    } else if (method === 'statistical_summary') {
      // 准备请求体，包含选中的列
      const requestBody = {};
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }
      
      const response = await fetch(`/data/${dataId}/statistical_summary`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取统计摘要失败");
      }
    } else if (method === 'correlation_analysis') {
      // 准备请求体，包含选中的列和方法
      const requestBody = {
        method: configs.correlationMethod
      };
      
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }
      
      const response = await fetch(`/data/${dataId}/correlation_analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取相关性分析结果失败");
      }
    } else if (method === 't_test') {
      // 准备T检验请求体
      const requestBody = {
        test_type: configs.tTestConfig.testType,
        alpha: configs.tTestConfig.alpha,
        params: {}
      };
      
      // 根据检验类型添加参数
      if (configs.tTestConfig.testType === 'one_sample') {
        requestBody.params.popmean = configs.tTestConfig.popmean;
      } else if (configs.tTestConfig.testType === 'independent') {
        requestBody.params.group_col = configs.tTestConfig.groupCol;
        requestBody.params.equal_var = configs.tTestConfig.equalVar;
      }
      
      // 添加正态性检验方法
      requestBody.params.normality_method = configs.tTestConfig.normalityMethod;
      
      // 添加选中的列
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }
      
      const response = await fetch(`/data/${dataId}/t_test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取T检验结果失败");
      }
    } else if (method === 'f_test') {
      // 准备F检验请求体
      const requestBody = {
        alpha: configs.fTestConfig.alpha
      };
      
      // 添加分组列（如果有）
      if (configs.fTestConfig.groupBy) {
        requestBody.group_by = configs.fTestConfig.groupBy;
      }
      
      // 添加选中的列
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }

      const response = await fetch(`/data/${dataId}/f_test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取F检验结果失败");
      }
    } else if (method === 'chi_square_test') {
      // 准备卡方检验请求体
      const requestBody = {
        alpha: configs.chiSquareTestConfig.alpha
      };
      
      // 添加分组列（如果有）
      if (configs.chiSquareTestConfig.groupBy) {
        requestBody.group_by = configs.chiSquareTestConfig.groupBy;
      }
      
      // 添加选中的列
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }

      const response = await fetch(`/data/${dataId}/chi_square_test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取卡方检验结果失败");
      }
    } else if (method === 'normality_test') {
      // 准备正态性检验请求体
      const requestBody = {
        method: configs.normalityTestConfig.method,
        alpha: configs.normalityTestConfig.alpha
      };
      
      // 添加分组列（如果有）
      if (configs.normalityTestConfig.groupBy) {
        requestBody.group_by = configs.normalityTestConfig.groupBy;
      }
      
      // 添加选中的列
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }
      
      const response = await fetch(`/data/${dataId}/normality_test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取正态性检验结果失败");
      }
    } else if (method === 'text_analysis') {
      if (selectedColumns.length === 0){
        throw new Error("请选择要处理的列");
      }
      const requestBody = {
        column: selectedColumns[0],
        color: configs.wordcloudConfig.color || ['#FF274B'],
        max_words: configs.wordcloudConfig.maxWords || 200,
        width: configs.wordcloudConfig.width || 1600,
        height: configs.wordcloudConfig.height || 900,
        background_color: configs.wordcloudConfig.backgroundColor || "#ffffff",
        max_font_size: configs.wordcloudConfig.maxFontSize || 200,
        min_font_size: configs.wordcloudConfig.minFontSize || 10,
        stopwords: configs.wordcloudConfig.stopwords || [],
        mask_shape: configs.wordcloudConfig.maskShape || "default"
      };

      const response = await fetch(`/nlp/${dataId}/wordcloud`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取词云分析结果失败");
      }
    } else if (method === 'sentiment_analysis') {
      if (selectedColumns.length === 0){
        throw new Error("请选择要处理的列");
      }
      const requestBody = {
        column: selectedColumns[0],
        stopwords: configs.sentimentConfig.stopwords || [],
        internet_slang: configs.sentimentConfig.internetSlang || {}
      };

      const response = await fetch(`/nlp/${dataId}/sentiment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        credentials: 'include'
      });

      const result = await response.json();
      if (result.success) {
        return result.data;
      } else {
        throw new Error(result.error || "获取情感分析结果失败");
      }
    }
    // 其他分析方法可以在这里添加
    return null;
  } catch (error) {
    console.error("加载分析结果失败:", error);
    throw error;
  }
}