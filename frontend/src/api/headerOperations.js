/**
 * 标题行操作 API 模块
 * 提供标题行相关功能的封装
 */

/**
 * 应用自定义标题行
 * @param {string} fileId - 文件ID
 * @param {Array} columnNames - 列名数组
 * @param {string} mode - 操作模式 ('add', 'modify', 'remove')
 * @returns {Promise<Object>} 操作结果
 */
export async function applyHeaderNames(fileId, columnNames, mode = "add") {
  if (!fileId) {
    throw new Error('请先选择一个文件');
  }

  // 检查是否所有列都已命名（仅在非删除模式下）
  if (mode !== 'remove') {
    const emptyNames = columnNames.filter(name => !name.trim()).length;
    if (emptyNames > 0) {
      throw new Error(`还有 ${emptyNames} 个列未命名，请为所有列提供名称。`);
    }
  }

  let modeParam = "add";
  if (mode === 'modify') {
    modeParam = "modify";
  } else if (mode === 'remove') {
    modeParam = "remove";
  }

  const response = await fetch(`/user/${fileId}/add_header`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      column_names: columnNames,
      mode: modeParam
    }),
    credentials: 'include'
  });

  if (!response.ok) {
    throw new Error(`添加标题行请求失败，状态码: ${response.status}`);
  }

  const result = await response.json();

  if (!result.success) {
    throw new Error(result.error || '添加标题行失败');
  }

  return result;
}