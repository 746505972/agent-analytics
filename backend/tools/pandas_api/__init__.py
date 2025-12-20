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


# 注册统计摘要工具
@tool
def statistical_summary_tool(
    file_path: str, session_id: str = None,
    columns: List[str] = None
) -> dict:
    """
    统计摘要 - 计算并返回指定列的统计摘要信息
    返回包括样本量、平均值、中位数、方差、标准差、最小值、最大值、四分位数、峰度、偏度等在内的全面统计信息
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        columns (List[str]): 需要处理的列名列表
    """
    from utils.pandas_tool import statistical_summary
    return statistical_summary(file_path, columns, session_id)

# 注册文本转换工具
@tool
def text_to_numeric_or_datetime_tool(
    file_path: str,
    columns: List[str],
    convert_to: str = "numeric",
    session_id: str = None,
    datetime_format: str = None
) -> dict:
    """
    文本转数值/时间 - 将包含千位分隔符、单位缩写（K,M等）的文本列转换为数值列，或将时间戳转换为时间列

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        convert_to (str): 转换目标类型 "numeric" 或 "datetime"
        session_id (str): 会话ID
        datetime_format (str): 时间格式(可选)，如转换为时间时可指定格式，例如 "%Y-%m-%d %H:%M:%S"
    """
    from utils.pandas_tool import text_to_numeric_or_datetime
    return text_to_numeric_or_datetime(file_path, columns, convert_to, session_id, datetime_format)


# 注册相关性分析工具
@tool
def correlation_analysis_tool(
    file_path: str, session_id: str = None,
    columns: List[str] = None,
    method: str = "pearson"
) -> dict:
    """
    相关性分析 - 计算并返回指定列之间的相关系数和p值
    返回每对变量之间的相关系数以及对应的p值，用于评估变量间的相关性强弱和统计显著性
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        columns (List[str]): 需要分析的列名列表
        method (str): 相关性计算方法 ("pearson", "spearman", "kendall")
    """
    from utils.pandas_tool import correlation_analysis
    return correlation_analysis(file_path, columns, method, session_id)

# 注册正态性检验工具
@tool
def normality_test_tool(file_path: str, columns: List[str], session_id: str = None,
        method: str = "shapiro", alpha: float = 0.05) -> dict:
    """
    正态性检验（自带常值检验）

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要检验的列名列表
        session_id (str): session_id
        method (str): 正态性检验方法 ("shapiro", "normaltest")
        alpha (float): 显著性水平 (默认0.05)
    """
    from utils.pandas_tool import normality_test
    return normality_test(file_path, columns, session_id, method, alpha)

# 注册T检验工具
@tool
def t_test_tool(file_path: str, columns: List[str], test_type: str = "one_sample",
        session_id: str = None, **kwargs) -> dict:
    """
    T检验 - 对数据执行不同类型的T检验，自带正态性检验

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要分析的列名列表
        test_type (str): T检验类型
            - "one_sample": 单样本T检验
            - "independent": 独立样本T检验
            - "paired": 配对样本T检验
        session_id (str): 会话ID
        **kwargs: 其他参数，用于特定检验的配置
            - popmean: 单样本t检验中的总体均值 (用于"one_sample"类型)
            - equal_var: 独立样本t检验中是否假设方差相等 (用于"independent"类型)
            - group_col: 分组列名，用于独立样本t检验 (用于"independent"类型)
            - normality_method: 正态性检验方法 ("shapiro", "normaltest")
            - alpha: 显著性水平 (默认0.05)

    Returns:
        Dict[str, Any]: 包含T检验结果和正态性检验结果的字典
    """
    from utils.pandas_tool import t_test
    return t_test(file_path, columns, test_type, session_id, **kwargs)

# 将模块中的函数注册为工具
def register_pandas_tools(agent):
    """
    将pandas工具注册到agent
    
    Args:
        agent: DataAnalysisAgent实例
    """
    agent.tools.append(remove_invalid_samples_tool)
    agent.tools.append(handle_missing_values_tool)
    agent.tools.append(dimensionless_processing_tool)
    agent.tools.append(scientific_calculation_tool)
    agent.tools.append(one_hot_encoding_tool)
    agent.tools.append(statistical_summary_tool)
    agent.tools.append(correlation_analysis_tool)
    agent.tools.append(text_to_numeric_or_datetime_tool)
    agent.tools.append(normality_test_tool)
    agent.tools.append(t_test_tool)