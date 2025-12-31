/**
 * 获取分析结果的API函数
 * 根据不同的分析方法调用相应的后端接口
 */
import { backendBaseUrl } from './apiConfig.js';

export async function fetchResult(dataId, method, options = {}){
  if(method === 'data_visualization'){
    return await fetchCompleteData(dataId);
  }else{
    return await fetchAnalysisResult(dataId, method, options);
  }
}
/**
 * 获取完整数据
 * @param {string} dataId - 数据文件ID
 * @returns {Promise<Object|null>} 完整数据或null（如果失败）
 * 该方法现已更改，只传回列信息
 */
export async function fetchCompleteData(dataId) {
  try {
    const response = await fetch(`${backendBaseUrl}/data/${dataId}/complete`, {
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
import { getDefaultConfigs } from '@/utils/configDefaults.js'
export async function fetchAnalysisResult(dataId, method, options = {}) {
  const { selectedColumns = [],
      configs =  getDefaultConfigs(),
} = options;
  
  try {
    if (method === 'basic_info') {
      const response = await fetch(`${backendBaseUrl}/data/${dataId}/details`, {
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
      
      const response = await fetch(`${backendBaseUrl}/data/${dataId}/statistical_summary`, {
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
      
      const response = await fetch(`${backendBaseUrl}/data/${dataId}/correlation_analysis`, {
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
      
      const response = await fetch(`${backendBaseUrl}/data/${dataId}/t_test`, {
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

      const response = await fetch(`${backendBaseUrl}/data/${dataId}/f_test`, {
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

      const response = await fetch(`${backendBaseUrl}/data/${dataId}/chi_square_test`, {
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
    } else if (method === 'non_parametric_test') {
      // 准备非参数检验请求体
      const requestBody = {
        test_type: configs.nonParametricTestConfig.testType,
        alpha: configs.nonParametricTestConfig.alpha,
        params: {
          alternative: configs.nonParametricTestConfig.alternative
        }
      };
      
      // 添加分组列（如果有）
      if (configs.nonParametricTestConfig.groupBy) {
        requestBody.group_by = configs.nonParametricTestConfig.groupBy;
      }
      
      // 添加分布类型（如果适用）
      if (configs.nonParametricTestConfig.distribution && 
          configs.nonParametricTestConfig.testType === 'kolmogorov_smirnov') {
        requestBody.params.distribution = configs.nonParametricTestConfig.distribution;
      }
      
      // 添加选中的列
      if (selectedColumns && selectedColumns.length > 0) {
        requestBody.columns = selectedColumns;
      }

      const response = await fetch(`${backendBaseUrl}/data/${dataId}/non_parametric_test`, {
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
        throw new Error(result.error || "获取非参数检验结果失败");
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
      
      const response = await fetch(`${backendBaseUrl}/data/${dataId}/normality_test`, {
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

      const response = await fetch(`${backendBaseUrl}/nlp/${dataId}/wordcloud`, {
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

      const response = await fetch(`${backendBaseUrl}/nlp/${dataId}/sentiment`, {
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
    } else if (method === 'linear_regression') {
      // 准备线性回归请求体
      const requestBody = {
        x_columns: selectedColumns || [],
        y_column: configs.linearRegressionConfig.y_column,
        method: configs.linearRegressionConfig.method || 'ols',
        alpha: configs.linearRegressionConfig.alpha || 1.0,
        l1_ratio: configs.linearRegressionConfig.l1_ratio || 0.5,
        params: {
          max_iter: configs.linearRegressionConfig.params.max_iter || 1000,
          tol: configs.linearRegressionConfig.params.tol || 0.0001,
          fit_intercept: configs.linearRegressionConfig.params.fit_intercept !== undefined ? configs.linearRegressionConfig.params.fit_intercept : true
        }
      };

      // 验证Y列是否已选择
      if (!requestBody.y_column) {
        throw new Error("请选择因变量(Y列)");
      }

      const response = await fetch(`${backendBaseUrl}/data/${dataId}/linear_regression`, {
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
        throw new Error(result.error || "获取线性回归结果失败");
      }
    }
    // 其他分析方法可以在这里添加
    return null;
  } catch (error) {
    console.error("加载分析结果失败:", error);
    throw error;
  }
}