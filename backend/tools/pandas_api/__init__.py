"""
Pandas API 模块
提供统计建模方法，包括数据清洗、聚类、假设检验、回归分析等功能
"""
import os
import sys

import pandas as pd
import numpy as np
from langchain_core.tools import tool
# 添加项目根目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)



# 数据清洗工具
@tool
def clean_data(
    file_path: str,
    session_id: str = None,
    remove_duplicates: bool = True,
    row_missing_threshold: float = 0.5,
    col_missing_threshold: float = 0.5,
    row_handling: str = "delete",
    col_handling: str = "delete"
) -> dict:
    """
    数据清洗功能
    
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        remove_duplicates (bool): 是否去除重复行，默认False
        row_missing_threshold (float): 行缺失值阈值(0-1)，默认1(不删除)
        col_missing_threshold (float): 列缺失值阈值(0-1)，默认1(不删除)
        row_handling (str): 行处理方式("delete" 或 "interpolate")，默认"delete"
        col_handling (str): 列处理方式("delete" 或 "interpolate")，默认"delete"
    """
    try:
        from utils.file_manager import clean_data_file
    except ImportError:
        # 最后尝试直接添加到路径并导入
        sys.path.insert(0, os.path.join(parent_dir, "utils"))
        from utils.file_manager import clean_data_file
    return clean_data_file(file_path, session_id,remove_duplicates, row_missing_threshold, col_missing_threshold, row_handling, col_handling)


# 聚类分析工具
@tool
def cluster_analysis(df: dict, method: str = 'kmeans', n_clusters: int = 3) -> dict:
    """
    执行聚类分析
    
    Args:
        df (dict): 输入数据（字典格式）
        method (str): 聚类方法 ('kmeans', 'hierarchical')
        n_clusters (int): 聚类数量
        
    Returns:
        dict: 聚类结果
    """
    # 占位函数，后续实现具体逻辑
    return {
        'method': method,
        'n_clusters': n_clusters,
        'status': 'placeholder'
    }

# 回归分析工具
@tool
def regression_analysis(df: dict, target_column: str, method: str = 'linear') -> dict:
    """
    执行回归分析
    
    Args:
        df (dict): 输入数据（字典格式）
        target_column (str): 目标变量列名
        method (str): 回归方法 ('linear', 'logistic', 'polynomial')
        
    Returns:
        dict: 回归分析结果
    """
    # 占位函数，后续实现具体逻辑
    return {
        'target': target_column,
        'method': method,
        'status': 'placeholder'
    }

# 假设检验工具
@tool
def hypothesis_test(df: dict, column1: str, column2: str = None, test_type: str = 'ttest') -> dict:
    """
    执行假设检验
    
    Args:
        df (dict): 输入数据（字典格式）
        column1 (str): 第一列数据
        column2 (str, optional): 第二列数据(两样本检验时需要)
        test_type (str): 棓验类型 ('ttest', 'ztest', 'chisquare')
        
    Returns:
        dict: 假设检验结果
    """
    # 占位函数，后续实现具体逻辑
    return {
        'column1': column1,
        'column2': column2,
        'test_type': test_type,
        'status': 'placeholder'
    }

# 将模块中的函数注册为工具
def register_pandas_tools(agent):
    """
    将pandas工具注册到agent
    
    Args:
        agent: DataAnalysisAgent实例
    """
    # 已经使用装饰器注册为工具，这里只需要将它们添加到agent中
    agent.tools.append(clean_data)
    agent.tools.append(cluster_analysis)
    agent.tools.append(regression_analysis)
    agent.tools.append(hypothesis_test)