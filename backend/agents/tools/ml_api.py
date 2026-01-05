"""
机器学习 API 模块
提供基于 PyTorch 的机器学习算法，包括深度学习、SVM、随机森林等
"""

from typing import List, Dict, Any
from langchain_core.tools import tool
from .tool_error_handler import tool_error_handler

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
    from utils.ml_tool import logistic_regression
    return logistic_regression(file_path, x_columns, y_column, method, session_id, solver, **kwargs)


# 将模块中的函数注册为工具
def register_ml_tools(agent):
    """
    将机器学习工具注册到agent

    Args:
        agent: DataAnalysisAgent实例
    """
    agent.tools.append(logistic_regression_tool)
