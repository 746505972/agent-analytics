/**
 * 分析结果 API 模块
 * 提供获取各种分析结果功能的封装
 */
export async function fetchResult(dataId, method, options = {}){
  if(method === 'line_chart'){
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
 * @param {Array} options.selectedColumns - 选中的列
 * @param {string} options.correlationMethod - 相关性分析方法
 * @returns {Promise<Object|null>} 分析结果或null（如果失败）
 */
export async function fetchAnalysisResult(dataId, method, options = {}) {
  const { selectedColumns = [], correlationMethod = 'pearson' } = options;
  
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
        method: correlationMethod
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
    }
    // 其他分析方法可以在这里添加
    return null;
  } catch (error) {
    console.error("加载分析结果失败:", error);
    throw error;
  }
}