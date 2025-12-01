/**
 * 反馈处理模块
 * 用于生成和处理各种操作的反馈信息
 */

/**
 * 生成数据转换操作的反馈信息
 * @param {Object} result - 操作结果
 * @returns {string} 格式化的反馈信息
 */
export function generateDataTransformationFeedback(result) {
  let statsMessage = '数据转换处理完成：\n';
  statsMessage += `已自动选择新文件\n\n`;
  statsMessage += '处理统计信息：\n';
  
  if (result.data.processed_columns) {
    statsMessage += `处理列: ${result.data.processed_columns.join(', ')}\n`;
  }
  
  if (result.data.method) {
    statsMessage += `处理方法: ${result.data.method}\n`;
  }
  
  if (result.data.operation) {
    statsMessage += `操作类型: ${result.data.operation}\n`;
  }
  
  return statsMessage;
}

/**
 * 生成删除列操作的反馈信息
 * @param {Object} result - 操作结果
 * @returns {string} 格式化的反馈信息
 */
export function generateDeleteColumnsFeedback(result) {
  return '列删除成功，已自动选择新文件';
}

/**
 * 生成插值法处理的反馈信息
 * @param {Object} result - 操作结果
 * @returns {string} 格式化的反馈信息
 */
export function generateMissingValueInterpolationFeedback(result) {
  const stats = result.data;
  let statsMessage = '插值处理完成：\n';
  statsMessage += `已自动选择新文件\n\n`;
  statsMessage += '处理统计信息：\n';
  statsMessage += `处理行数: ${stats.processed_rows}\n`;
  statsMessage += `处理列数: ${stats.processed_cols}\n`;
  statsMessage += `剩余缺失值: ${stats.remaining_missing_count}\n`;
  statsMessage += `填充缺失值: ${stats.missing_filled_count}\n\n`;
  
  if (Object.keys(stats.cols_filled).length > 0) {
    statsMessage += '各列填充详情:\n';
    for (const [col, count] of Object.entries(stats.cols_filled)) {
      statsMessage += `${col}: ${count}个缺失值\n`;
    }
  }
  
  return statsMessage;
}

/**
 * 生成无效样本处理的反馈信息
 * @param {Object} result - 操作结果
 * @returns {string} 格式化的反馈信息
 */
export function generateInvalidSamplesFeedback(result) {
  const stats = result.data.cleaning_stats;
  let statsMessage = '无效样本处理完成：\n';
  statsMessage += `已自动选择新文件\n\n`;
  statsMessage += '处理统计信息：\n';
  statsMessage += `删除重复行: ${stats.duplicates_removed}\n`;
  statsMessage += `删除重复列: ${stats.duplicate_cols_removed}\n`;
  statsMessage += `删除常量列: ${stats.constant_cols_removed}\n`;
  statsMessage += `删除行数: ${stats.rows_removed}\n`;
  statsMessage += `删除列数: ${stats.columns_removed}`;
  
  return statsMessage;
}