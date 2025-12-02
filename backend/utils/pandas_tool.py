"""
Pandas 数据转换工具模块
提供数据转换功能，包括量纲处理、科学计算、独热编码等功能
"""

import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder, QuantileTransformer, PowerTransformer, Normalizer

# 添加项目根目录到sys.path
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.file_manager import read_any_file, ensure_data_dir, ensure_session_dir, generate_new_file_path


def dimensionless_processing(
    file_path: str,
    columns: List[str],
    method: str = "standard",
    session_id: str = None,
    **kwargs
) -> Dict[str, Any]:
    """
    量纲处理 - 对数据进行标准化、归一化等处理
    
    Args:
        file_path (str): 文件路径
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
        
    Returns:
        Dict[str, Any]: 处理结果信息
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)
        
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
        
    # 读取文件
    df = read_any_file(file_path)
    
    # 检查列是否存在
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"以下列不存在于数据集中: {missing_columns}")
        
    # 只选择数值型列进行处理
    numeric_columns = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]
    non_numeric_columns = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
    
    if non_numeric_columns:
        print(f"警告: 以下列为非数值型，将跳过处理: {non_numeric_columns}")
        
    if not numeric_columns:
        raise ValueError("没有有效的数值型列可供处理")
        
    # 根据方法选择对应的处理器
    if method == "standard":
        scaler = StandardScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        
    elif method == "minmax":
        scaler = MinMaxScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        
    elif method == "robust":
        scaler = RobustScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        
    elif method in ["unit", "l2"]:
        # L2范数标准化
        df[numeric_columns] = df[numeric_columns].div(
            np.linalg.norm(df[numeric_columns], axis=0), axis=1
        )
        
    elif method == "l1":
        # L1范数标准化
        df[numeric_columns] = df[numeric_columns].div(
            np.linalg.norm(df[numeric_columns], ord=1, axis=0), axis=1
        )
        
    elif method == "max":
        # 最大值标准化
        df[numeric_columns] = df[numeric_columns].div(
            df[numeric_columns].abs().max(), axis=1
        )
        
    elif method == "quantile":
        # 分位数变换
        n_quantiles = kwargs.get('n_quantiles', min(100, len(df)))
        output_distribution = kwargs.get('output_distribution', 'uniform')
        scaler = QuantileTransformer(n_quantiles=n_quantiles, 
                                   output_distribution=output_distribution,
                                   random_state=0)
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        
    elif method == "yeo-johnson":
        # Yeo-Johnson变换
        standardize = kwargs.get('standardize', True)
        scaler = PowerTransformer(method='yeo-johnson', standardize=standardize)
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        
    elif method == "box-cox":
        # Box-Cox变换 (仅适用于正值)
        # 检查是否有非正值
        if (df[numeric_columns] <= 0).any().any():
            # 对非正值添加常数使其变为正值
            min_val = df[numeric_columns].min().min()
            if min_val <= 0:
                df[numeric_columns] = df[numeric_columns] + abs(min_val) + 1
                
        standardize = kwargs.get('standardize', True)
        scaler = PowerTransformer(method='box-cox', standardize=standardize)
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
        
    else:
        raise ValueError(f"不支持的量纲处理方法: {method}")
        
    # 保存处理后的数据
    new_filename, new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "saved_path": new_file_path,
        "processed_columns": numeric_columns,
        "method": method
    }


def scientific_calculation(
    file_path: str,
    columns: List[str],
    operation: str,
    params: Dict[str, Any] = None,
    session_id: str = None
) -> Dict[str, Any]:
    """
    科学计算 - 对数据执行数学运算
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        operation (str): 运算类型
            - "log": 对数变换
            - "exp": 指数变换
            - "power": 幂变换
            - "sqrt": 平方根变换
            - "poly": 多项式特征
        params (Dict[str, Any]): 运算参数
            - power: 幂指数 (用于"power"操作)
            - degree: 多项式度数 (用于"poly"操作)
        session_id (str): 会话ID
        
    Returns:
        Dict[str, Any]: 处理结果信息
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)
        
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
        
    # 读取文件
    df = read_any_file(file_path)
    
    # 检查列是否存在
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"以下列不存在于数据集中: {missing_columns}")
        
    # 只选择数值型列进行处理
    numeric_columns = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]
    non_numeric_columns = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
    
    if non_numeric_columns:
        print(f"警告: 以下列为非数值型，将跳过处理: {non_numeric_columns}")
        
    if not numeric_columns:
        raise ValueError("没有有效的数值型列可供处理")
        
    # 根据操作类型执行相应计算
    if operation == "log":
        # 对数变换
        for col in numeric_columns:
            # 处理负数和零值
            min_val = df[col].min()
            if min_val <= 0:
                df[col] = df[col] + abs(min_val) + 1
            df[col] = np.log(df[col])
            
    elif operation == "exp":
        # 指数变换
        for col in numeric_columns:
            df[col] = np.exp(df[col])
            
    elif operation == "power":
        # 幂变换
        power = params.get("power", 2) if params else 2
        for col in numeric_columns:
            df[col] = np.power(df[col], power)
            
    elif operation == "sqrt":
        # 平方根变换
        for col in numeric_columns:
            # 处理负数
            df[col] = np.where(df[col] < 0, np.sqrt(np.abs(df[col])), np.sqrt(df[col]))
            
    elif operation == "poly":
        # 多项式特征
        degree = params.get("degree", 2) if params else 2
        for col in numeric_columns:
            for d in range(2, degree + 1):
                new_col_name = f"{col}^{d}"
                df[new_col_name] = np.power(df[col], d)
                
    else:
        raise ValueError(f"不支持的科学计算操作: {operation}")
        
    # 保存处理后的数据
    new_filename, new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "saved_path": new_file_path,
        "processed_columns": numeric_columns,
        "operation": operation
    }


def one_hot_encoding(
    file_path: str,
    columns: List[str],
    session_id: str = None,
    drop_first: bool = False
) -> Dict[str, Any]:
    """
    独热编码 - 对分类变量进行独热编码处理
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        session_id (str): 会话ID
        drop_first (bool): 是否删除第一个虚拟变量以避免多重共线性
        
    Returns:
        Dict[str, Any]: 处理结果信息
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)
        
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
        
    # 读取文件
    df = read_any_file(file_path)
    
    # 检查列是否存在
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"以下列不存在于数据集中: {missing_columns}")
        
    # 对指定列进行独热编码
    processed_columns = []
    
    for col in columns:
        # 获取该列的所有唯一值
        unique_values = df[col].dropna().unique()
        
        # 创建独热编码列
        for i, value in enumerate(unique_values):
            if drop_first and i == 0:
                continue  # 跳过第一个值以避免多重共线性
                
            new_col_name = f"{col}_{value}"
            df[new_col_name] = (df[col] == value).astype(int)
            
        processed_columns.append(col)
        
    # 删除原始分类列
    df = df.drop(columns=columns)
        
    # 保存处理后的数据
    new_filename, new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "saved_path": new_file_path,
        "processed_columns": processed_columns
    }


def statistical_summary(
    file_path: str,
    columns: List[str],
    session_id: str = None
) -> Dict[str, Any]:
    """
    统计摘要 - 计算并返回指定列的统计摘要信息
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        session_id (str): 会话ID
        
    Returns:
        Dict[str, Any]: 包含统计摘要信息的字典，格式适合 echarts 绘制表格
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)
        
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
        
    # 读取文件
    df = read_any_file(file_path)
    
    # 检查列是否存在
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"以下列不存在于数据集中: {missing_columns}")

    # 只选择数值型列进行处理
    numeric_columns = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]
    non_numeric_columns = [col for col in columns if not pd.api.types.is_numeric_dtype(df[col])]
    
    if non_numeric_columns:
        print(f"警告: 以下列为非数值型，将跳过处理: {non_numeric_columns}")
        
    if not numeric_columns:
        raise ValueError("没有有效的数值型列可供处理")
    
    # 计算统计摘要信息
    summary_data = []
    for col in numeric_columns:
        col_data = df[col].dropna()  # 排除空值
        
        # 计算各项统计指标
        count = len(col_data)
        mean = col_data.mean()
        median = col_data.median()
        variance = col_data.var()
        std_dev = col_data.std()
        min_val = col_data.min()
        max_val = col_data.max()
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        
        # 计算峰度和偏度
        kurtosis = col_data.kurtosis()
        skewness = col_data.skew()
        
        # 计算其他常用统计指标
        range_val = max_val - min_val
        iqr = q3 - q1  # 四分位距
        
        # 构造适合 echarts 表格的数据格式
        summary_data.append({
            "column": col,
            "count": count,
            "mean": round(float(mean), 6) if not pd.isna(mean) else None,
            "median": round(float(median), 6) if not pd.isna(median) else None,
            "variance": round(float(variance), 6) if not pd.isna(variance) else None,
            "std_dev": round(float(std_dev), 6) if not pd.isna(std_dev) else None,
            "min": round(float(min_val), 6) if not pd.isna(min_val) else None,
            "max": round(float(max_val), 6) if not pd.isna(max_val) else None,
            "q1": round(float(q1), 6) if not pd.isna(q1) else None,
            "q3": round(float(q3), 6) if not pd.isna(q3) else None,
            "kurtosis": round(float(kurtosis), 6) if not pd.isna(kurtosis) else None,
            "skewness": round(float(skewness), 6) if not pd.isna(skewness) else None,
            "range": round(float(range_val), 6) if not pd.isna(range_val) else None,
            "iqr": round(float(iqr), 6) if not pd.isna(iqr) else None
        })
    
    # 准备返回结果
    result = {
        "columns": numeric_columns,
        "summary": summary_data
    }
    
    return result
