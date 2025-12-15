/**
 * 列操作 API 模块
 * 提供各种列操作功能的封装
 */

/**
 * 执行删除列操作
 * @param {string} fileId - 文件ID
 * @param {Array} columnsToDelete - 要删除的列数组
 * @returns {Promise<Object>} 删除结果
 */
export async function executeDeleteColumns(fileId, columnsToDelete) {
  if (!fileId) {
    throw new Error('请先选择一个文件');
  }

  if (columnsToDelete.length === 0) {
    throw new Error('请选择要删除的列');
  }

  const response = await fetch(`/user/${fileId}/delete_columns`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      columns_to_delete: columnsToDelete
    }),
    credentials: 'include'
  });

  const result = await response.json();
  
  if (!result.success) {
    throw new Error(result.error || '删除列失败');
  }

  return result;
}

/**
 * 执行插值法处理缺失值
 * @param {string} fileId - 文件ID
 * @param {Array} selectedColumns - 选中的列
 * @param {Object} interpolationConfig - 插值配置
 * @returns {Promise<Object>} 插值处理结果
 */
export async function executeMissingValueInterpolation(fileId, selectedColumns, interpolationConfig) {
  if (!fileId) {
    throw new Error('请先选择一个文件');
  }

  const response = await fetch(`/user/${fileId}/handle_missing_values`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      specified_columns: interpolationConfig.interpolationMethod !== 'knn' ? selectedColumns : undefined,
      interpolation_method: interpolationConfig.interpolationMethod,
      fill_value: interpolationConfig.fillValue || undefined,
      knn_neighbors: interpolationConfig.knnNeighbors
    }),
    credentials: 'include'
  });

  const result = await response.json();
  
  if (!result.success) {
    throw new Error(result.error || '插值处理失败');
  }

  return result;
}

/**
 * 执行无效样本处理
 * @param {string} fileId - 文件ID
 * @param {Object} invalidSamplesConfig - 无效样本处理配置
 * @returns {Promise<Object>} 无效样本处理结果
 */
export async function executeInvalidSamples(fileId, invalidSamplesConfig) {
  if (!fileId) {
    throw new Error('请先选择一个文件');
  }

  const response = await fetch(`/user/${fileId}/remove_invalid_samples`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      remove_duplicates: invalidSamplesConfig.removeDuplicates,
      remove_duplicate_cols: invalidSamplesConfig.removeDuplicateCols,
      remove_constant_cols: invalidSamplesConfig.removeConstantCols,
      row_missing_threshold: invalidSamplesConfig.rowMissingThreshold,
      col_missing_threshold: invalidSamplesConfig.columnMissingThreshold
    }),
    credentials: 'include'
  });

  const result = await response.json();
  
  if (!result.success) {
    throw new Error(result.error || '处理无效样本失败');
  }

  return result;
}