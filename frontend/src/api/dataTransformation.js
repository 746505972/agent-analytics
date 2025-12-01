/**
 * 数据转换 API 模块
 * 提供各种数据转换功能的封装
 */

/**
 * 执行数据转换
 * @param {string} fileId - 文件ID
 * @param {Array} selectedColumns - 选中的列
 * @param {Object} config - 转换配置
 * @returns {Promise<Object>} 转换结果
 */
export async function executeDataTransformation(fileId, selectedColumns, config) {
  if (!fileId) {
    throw new Error('请先选择一个文件');
  }

  if (selectedColumns.length === 0) {
    throw new Error('请选择至少一列进行处理');
  }

  let endpoint;
  let requestBody;

  // 根据转换类型调用不同的API
  switch (config.transformationType) {
    case 'dimensionless':
      endpoint = `/user/${fileId}/dimensionless_processing`;
      requestBody = {
        columns: selectedColumns,
        method: config.dimensionless.method,
        params: config.dimensionless.params
      };
      break;
      
    case 'scientific':
      endpoint = `/user/${fileId}/scientific_calculation`;
      requestBody = {
        columns: selectedColumns,
        operation: config.scientific.operation,
        params: config.scientific.params
      };
      break;
      
    case 'onehot':
      endpoint = `/user/${fileId}/one_hot_encoding`;
      requestBody = {
        columns: selectedColumns,
        drop_first: config.onehot.drop_first
      };
      break;
      
    default:
      throw new Error('未知的转换类型');
  }

  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody),
    credentials: 'include'
  });

  if (!response.ok) {
    throw new Error(`数据转换处理请求失败，状态码: ${response.status}`);
  }

  const result = await response.json();
  
  if (!result.success) {
    throw new Error(result.error || '数据转换处理失败');
  }

  return result;
}