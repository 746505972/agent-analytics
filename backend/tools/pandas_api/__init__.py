"""
Pandas API 模块
提供统计建模方法，包括数据清洗、聚类、假设检验、回归分析等功能
"""
import os
import sys
from typing import Any, List

# 添加项目根目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 添加绝对导入路径
sys.path.insert(0, os.path.join(parent_dir, '..'))

from langchain_core.tools import tool
from utils.file_manager import remove_invalid_samples, handle_missing_values
from utils.pandas_tool import dimensionless_processing, scientific_calculation, one_hot_encoding

# 注册去除无效样本工具
@tool
def remove_invalid_samples_tool(file_path: str, session_id: str = None,
                                remove_duplicates: bool = False,
                                remove_duplicate_cols: bool = False,
                                remove_constant_cols: bool = False,
                                row_missing_threshold: float = 1,
                                col_missing_threshold: float = 1) -> dict:
    """
    去除无效样本 - 处理重复数据和超出阈值的行列
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        remove_duplicates (bool): 是否去除重复行
        remove_duplicate_cols (bool): 是否删除重复列
        remove_constant_cols (bool): 是否删除所有数据都相同的列
        row_missing_threshold (float): 行缺失值阈值 (0-1之间)
        col_missing_threshold (float): 列缺失值阈值 (0-1之间)
    """
    return remove_invalid_samples(file_path, session_id, remove_duplicates,
                                  remove_duplicate_cols, remove_constant_cols,
                                  row_missing_threshold, col_missing_threshold)



# 注册处理缺失值工具
@tool
def handle_missing_values_tool(file_path: str, session_id: str = None,
                               specified_columns: List[str] = None,
                               interpolation_method: str = "linear",
                               fill_value: Any = None,
                               knn_neighbors: int = 5) -> dict:
    """
    对缺失数据进行插值
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        specified_columns (List[str]): 指定要处理的列名列表，如果为None则处理所有列
        interpolation_method (str): 插值方法 ("linear", "ffill", "bfill", "mean", "median", "mode", "knn", "constant")
        fill_value (Any): 当使用constant方法时的填充值
        knn_neighbors (int): KNN插值的邻居数量
    """
    return handle_missing_values(file_path, session_id, specified_columns, interpolation_method,
                                 fill_value, knn_neighbors)

# 注册量纲处理工具
@tool
def dimensionless_processing_tool(
    file_path: str, session_id: str = None,
    columns: List[str] = None,
    method: str = "standard",
    **kwargs
) -> dict:
    """
    量纲处理 - 对数据进行标准化、归一化等处理
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        columns (List[str]): 需要处理的列名列表
        method (str): 处理方法
            - "standard": Z-score标准化 (默认)
            - "minmax": 最小-最大归一化 [0,1]
            - "robust": 鲁棒缩放 (使用中位数和四分位数)
            - "unit": 单位向量化 (L2范数)
            - "quantile": 分位数变换
            - "yeo-johnson": Yeo-Johnson变换
            - "box-cox": Box-Cox变换
            - "l1": L1范数标准化
            - "l2": L2范数标准化 (与unit相同)
            - "max": 最大值标准化
        session_id (str): 会话ID
        **kwargs: 其他参数，用于特定方法的配置
            - n_quantiles: 分位数变换的分位数数量 (默认100)
            - output_distribution: 分位数变换的输出分布 ('uniform'或'normal')
            - standardize: 是否在power变换后标准化数据 (默认True)
    """
    return dimensionless_processing(file_path, columns, method, session_id, **kwargs)


# 注册科学计算工具
@tool
def scientific_calculation_tool(
    file_path: str, session_id: str = None,
    columns: List[str] = None,
    operation: str = None,
    params: dict = None
) -> dict:
    """
    科学计算 - 对数据执行数学运算
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        columns (List[str]): 需要处理的列名列表
        operation (str): 运算类型 ("log", "exp", "power", "sqrt", "poly")
        params (dict): 运算参数
    """
    return scientific_calculation(file_path, columns, operation, params, session_id)


# 注册独热编码工具
@tool
def one_hot_encoding_tool(
    file_path: str, session_id: str = None,
    columns: List[str] = None,
    drop_first: bool = False
) -> dict:
    """
    独热编码 - 对分类变量进行独热编码处理
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        columns (List[str]): 需要处理的列名列表
        drop_first (bool): 是否删除第一个虚拟变量以避免多重共线性
    """
    return one_hot_encoding(file_path, columns, session_id, drop_first)


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
    agent.tools.append(remove_invalid_samples_tool)
    agent.tools.append(handle_missing_values_tool)
    agent.tools.append(dimensionless_processing_tool)
    agent.tools.append(scientific_calculation_tool)
    agent.tools.append(one_hot_encoding_tool)
    agent.tools.append(cluster_analysis)
    agent.tools.append(regression_analysis)
    agent.tools.append(hypothesis_test)