"""
机器学习 API 模块
提供基于 sklearn、PyTorch 的机器学习算法，包括深度学习、SVM、随机森林等
"""

from typing import List, Dict, Any
from langchain_core.tools import tool
from .tool_error_handler import tool_error_handler
from utils.ml_tool import logistic_regression, clustering_analysis

# 注册逻辑回归工具
@tool
@tool_error_handler
def logistic_regression_tool(file_path: str, x_columns: List[str], y_column: str,
                          method: str = "logistic", session_id: str = None,
                          solver: str = 'lbfgs', **kwargs) -> Dict[str, Any]:
    """
    逻辑回归 - 使用逻辑回归进行分类任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列，分类标签）
        method (str): 回归方法 (默认 "logistic")
        session_id (str): 会话ID
        solver (str): 优化算法
            - "lbfgs": 拟牛顿法 (默认，适用于小数据集)
            - "liblinear": 坐标下降法 (适用于小数据集)
            - "newton-cg": 牛顿共轭梯度法 (适用于大数据集)
            - "sag": 随机平均梯度下降 (适用于大数据集)
            - "saga": 随机平均梯度下降加速版 (适用于大数据集)
        **kwargs: 其他参数，用于特定回归方法的配置
            - C (float): 正则化强度的倒数，值越小正则化越强 (默认1.0)
            - max_iter (int): 最大迭代次数 (默认1000)
            - tol: 收敛容差 (默认1e-4)
            - fit_intercept: 是否拟合截距 (默认True)
            - class_weight: 类别权重 ("balanced" 或 None)

    Returns:
        Dict[str, Any]: 包含逻辑回归结果的字典
    """
    return logistic_regression(file_path, x_columns, y_column, method, session_id, solver, **kwargs)


# 注册聚类分析工具
@tool
@tool_error_handler
def clustering_analysis_tool(file_path: str, columns: List[str],
                          method: str = "kmeans", n_clusters: int = 3, session_id: str = None,
                          **kwargs) -> Dict[str, Any]:
    """
    聚类分析 - 使用多种聚类算法对数据进行分组分析

    Args:
        file_path (str): 文件路径
        columns (List[str]): 用于聚类的列名列表
        method (str): 聚类方法
            - "kmeans": K-means聚类 (默认)
            - "hierarchical": 层次聚类
            - "dbscan": DBSCAN聚类
            - "gmm": 高斯混合模型
        n_clusters (int): 簇的数量 (对于K-means、层次聚类和GMM)
        session_id (str): 会话ID
        **kwargs: 其他参数，用于特定聚类方法的配置
            - standardize (bool): 是否标准化数据 (默认True)
            - init (str): K-means初始化方法 ("k-means++", "random") 
            - max_iter (int): K-means最大迭代次数 (默认300)
            - eps (float): DBSCAN的邻域半径 (默认0.5)
            - min_samples (int): DBSCAN的最小样本数 (默认5)
            - linkage (str): 层次聚类的链接方法 ("ward", "complete", "average", "single")
            - covariance_type (str): GMM协方差类型 ("full", "tied", "diag", "spherical")

    Returns:
        Dict[str, Any]: 包含聚类分析结果的字典
    """
    return clustering_analysis(file_path, columns, method, n_clusters, session_id, **kwargs)


# 将模块中的函数注册为工具
def register_ml_tools(agent):
    """
    将机器学习工具注册到agent

    Args:
        agent: DataAnalysisAgent实例
    """
    agent.tools.append(logistic_regression_tool)
    agent.tools.append(clustering_analysis_tool)
