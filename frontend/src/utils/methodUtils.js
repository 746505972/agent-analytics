// methodUtils.js
// 存放与方法相关的工具函数

/**
 * 获取方法的中文名称
 * @param {string} methodId - 方法ID
 * @returns {string} 方法的中文名称
 */
export function getMethodName(methodId) {
  const methods = {
    'basic_info': '基本信息',
    'statistical_summary': '统计摘要',
    'correlation_analysis': '相关性分析',
    't_test': 'T检验',
    'f_test': 'F检验',
    'chi_square_test': '卡方检验',
    'linear_regression': '线性回归',
    'normality_test': '正态性检验',
    'non_parametric_test': '非参数检验',
    'line_chart': '折线图',
    'scatter_plot': '散点图',
    'bar_chart': '柱状图',
    'histogram': '直方图',
    'pie_chart': '饼图',
    'box_plot': '箱线图',
    'clustering': '聚类分析',
    'classification': '分类分析',
    'logistic_regression': '逻辑回归',
    'decision_tree': '决策树',
    'random_forest': '随机森林',
    'knn': 'KNN',
    'naive_bayes': '朴素贝叶斯',
    'svm': '支持向量机',
    'neural_network': '神经网络',
    'xgboost': 'XGBoost',
    'text_analysis': '文本分析',
    'sentiment_analysis': '情感分析',
    'invalid_samples': '无效样本',
    'data_transformation': '数据转换',
    'add_header': '添加/修改标题行',
    'delete_columns': '删除列',
    'data_visualization': '数据可视化',
  };
  return methods[methodId] || '未知分析';
}