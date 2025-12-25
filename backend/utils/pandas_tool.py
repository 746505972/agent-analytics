"""
Pandas 数据转换工具模块
提供数据转换功能，包括量纲处理、科学计算、独热编码等功能
"""

import os
# 添加项目根目录到sys.path
import sys
from typing import List, Dict, Any

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder, QuantileTransformer, \
    PowerTransformer, Normalizer
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, shapiro, normaltest, \
    levene, bartlett,f_oneway, chi2_contingency, mannwhitneyu, wilcoxon, kruskal, ks_2samp, kstest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.file_manager import read_any_file, ensure_session_dir, generate_new_file_path

def check_and_read(file_path: str, columns: List[str], session_id: str = None) -> tuple:
    """
    检查文件和列的有效性，并读取数据

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        session_id (str): 会话ID

    Returns:
        tuple: (df, numeric_columns) 数据框和有效的数值列列表

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 列不存在或没有有效的数值型列
    """
    # 确保数据目录存在
    os.makedirs("data", exist_ok=True)

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

    if not numeric_columns:
        raise ValueError("没有有效的数值型列可供处理")

    return df, numeric_columns


def dimensionless_processing(file_path: str,columns: List[str],method: str = "standard",
    session_id: str = None,**kwargs) -> Dict[str, Any]:
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
    df, numeric_columns = check_and_read(file_path, columns, session_id)
        
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


def scientific_calculation(file_path: str,columns: List[str],operation: str,
    params: Dict[str, Any] = None,session_id: str = None) -> Dict[str, Any]:
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
    df, numeric_columns = check_and_read(file_path, columns, session_id)
        
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


def one_hot_encoding(file_path: str,columns: List[str],session_id: str = None,
    drop_first: bool = False) -> Dict[str, Any]:
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
    df, _ = check_and_read(file_path, columns, session_id)
        
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


def statistical_summary(file_path: str,columns: List[str],session_id: str = None) -> Dict[str, Any]:
    """
    统计摘要 - 计算并返回指定列的统计摘要信息
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        session_id (str): 会话ID
        
    Returns:
        Dict[str, Any]: 包含统计摘要信息的字典，格式适合 echarts 绘制表格
    """

    df, numeric_columns = check_and_read(file_path, columns, session_id)
    
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

def normality_test(file_path: str,columns: List[str],session_id: str = None,
    method: str = "shapiro",alpha: float = 0.05, group_by: str = None) -> Dict[str, Any]:
    """
    正态性检验

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要检验的列名列表
        method (str): 正态性检验方法 ("shapiro", "normaltest")
        alpha (float): 显著性水平 (默认0.05)
        group_by (str): 分组列名，如果提供则按组进行正态性检验
    """
    df, numeric_columns = check_and_read(file_path, columns, session_id)
    
    if group_by:
        # 按分组列进行正态性检验
        if group_by not in df.columns:
            raise ValueError(f"分组列 '{group_by}' 不存在于数据集中")
        
        # 获取唯一分组
        unique_groups = df[group_by].dropna().unique()
        grouped_results = {}
        
        for group in unique_groups:
            # 筛选当前组的数据
            group_data = df[df[group_by] == group]
            grouped_results[group] = _normality_test_with_constants(group_data, numeric_columns, method, alpha)
        
        return {
            "grouped_results": grouped_results,
            "group_by": group_by,
        }
    else:
        # 原始的正态性检验逻辑
        return _normality_test_with_constants(df, numeric_columns, method, alpha)

def _safe_float(value):
    """安全地将值转换为float，处理inf和nan值"""
    if value is None:
        return None
    try:
        f = float(value)
        if np.isinf(f) or np.isnan(f):
            return None
        return f
    except (ValueError, OverflowError):
        return None

def _normality_test_with_constants(df: pd.DataFrame,columns: List[str],
    method: str = "shapiro",alpha: float = 0.05) -> Dict[str, Any]:
    """
    正态性检验（包括常量列检测）

    Args:
        df (pd.DataFrame): 数据框
        columns (List[str]): 需要检验的列名列表
        method (str): 正态性检验方法 ("shapiro", "normaltest")
        alpha (float): 显著性水平 (默认0.05)

    Returns:
        Dict[str, Any]: 包含正态性检验结果和常量列信息的字典
    """
    # 检查是否有常量列（方差为0的列）
    constant_columns = []
    normality_results = {}

    # 对选定的数值列进行正态性检验
    for col in columns:
        col_data = df[col].dropna()

        # 数据量检查
        if len(col_data) < 3:
            raise ValueError(f"列 '{col}' 的有效数据少于3个，无法进行正态性检验")

        # 检查是否为常量列（方差为0）
        if col_data.var() == 0:
            constant_columns.append(col)
            normality_results[col] = {
                "method": method,
                "statistic": 0.0,
                "p_value": 1.0,
                "is_normal": True,  # 常量可以视为正态分布
                "sample_size": len(col_data),
                "is_constant": True
            }
            continue

        # 根据数据量选择合适的正态性检验方法
        try:
            if method == "shapiro" and len(col_data) <= 5000:  # Shapiro-Wilk适用于小样本
                stat, p_value = shapiro(col_data)
            else:  # D'Agostino's normality test适用于大样本
                stat, p_value = normaltest(col_data)
                method = "normaltest"

            normality_results[col] = {
                "method": method,
                "statistic": _safe_float(stat),
                "p_value": _safe_float(p_value),
                "is_normal": bool(p_value > alpha) if _safe_float(p_value) is not None else True,
                "sample_size": len(col_data)
            }
        except Exception as e:
            normality_results[col] = {
                "method": method,
                "error": str(e),
                "is_normal": False
            }

    return {
        "normality_results": normality_results,
        "constant_columns": constant_columns
    }


def t_test(file_path: str,columns: List[str],test_type: str = "one_sample",
    session_id: str = None,**kwargs) -> Dict[str, Any]:
    """
    T检验 - 对数据执行不同类型的T检验，并先进行正态性检验
    
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

    df, numeric_columns = check_and_read(file_path, columns, session_id)
    
    # 获取参数
    normality_method = kwargs.get("normality_method", "shapiro")
    alpha = kwargs.get("alpha", 0.05)
    
    # 执行正态性检验（包括常量列检测）
    normality_test_result = _normality_test_with_constants(df, numeric_columns, normality_method, alpha)
    normality_results = normality_test_result["normality_results"]
    
    # 执行T检验
    t_test_results = {}
    
    if test_type == "one_sample":
        # 单样本T检验
        popmean = kwargs.get("popmean", 0)  # 默认总体均值为0
        
        for col in numeric_columns:
            col_data = df[col].dropna()
            
            try:
                # 执行单样本T检验
                t_stat, p_value = ttest_1samp(col_data, popmean)
                
                t_test_results[col] = {
                    "test_type": "one_sample",
                    "statistic": _safe_float(t_stat),
                    "p_value": _safe_float(p_value),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                    "popmean": _safe_float(popmean),
                    "sample_mean": _safe_float(col_data.mean()),
                    "sample_std": _safe_float(col_data.std()),
                    "sample_size": len(col_data)
                }
            except Exception as e:
                t_test_results[col] = {
                    "test_type": "one_sample",
                    "error": str(e)
                }
                
    elif test_type == "independent":
        # 独立样本T检验
        group_col = kwargs.get("group_col")
        equal_var = kwargs.get("equal_var", True)
        
        if not group_col:
            raise ValueError("独立样本T检验需要指定分组列 (group_col)")
            
        if group_col not in df.columns:
            raise ValueError(f"分组列 '{group_col}' 不存在于数据集中")
            
        # 检查分组列是否为分类变量
        if pd.api.types.is_numeric_dtype(df[group_col]):
            print(f"警告: 分组列 '{group_col}' 是数值型，建议确认是否为正确的分组变量")
            
        # 获取唯一分组
        unique_groups = df[group_col].dropna().unique()
        if len(unique_groups) != 2:
            raise ValueError(f"独立样本T检验要求分组列恰好有2个不同的组，当前有 {len(unique_groups)} 个组")
            
        # 提取两组数据
        group1_name, group2_name = unique_groups[0], unique_groups[1]
        group1_data = df[df[group_col] == group1_name][numeric_columns].dropna()
        group2_data = df[df[group_col] == group2_name][numeric_columns].dropna()
        
        # 方差齐性检验
        variance_results = {}
        for col in numeric_columns:
            try:
                # Levene检验对方差齐性进行检验
                lev_stat, lev_p = levene(group1_data[col], group2_data[col])
                
                # Bartlett检验（要求数据正态分布）
                try:
                    bartlett_stat, bartlett_p = bartlett(group1_data[col], group2_data[col])
                except:
                    bartlett_stat, bartlett_p = None, None
                    
                variance_results[col] = {
                    "levene": {
                        "statistic": _safe_float(lev_stat),
                        "p_value": _safe_float(lev_p),
                        "equal_variance": bool(lev_p > alpha) if _safe_float(lev_p) is not None else False
                    },
                    "bartlett": {
                        "statistic": _safe_float(bartlett_stat) if bartlett_stat is not None else None,
                        "p_value": _safe_float(bartlett_p) if bartlett_p is not None else None,
                        "equal_variance": bool(bartlett_p > alpha) if bartlett_p is not None and _safe_float(bartlett_p) is not None else None
                    } if bartlett_stat is not None else None
                }
            except Exception as e:
                variance_results[col] = {
                    "error": str(e)
                }
        
        # 对每个数值列执行独立样本T检验
        for col in numeric_columns:
            try:
                # 执行独立样本T检验
                t_stat, p_value = ttest_ind(group1_data[col], group2_data[col], equal_var=equal_var)
                
                t_test_results[col] = {
                    "test_type": "independent",
                    "statistic": _safe_float(t_stat),
                    "p_value": _safe_float(p_value),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                    "equal_var": equal_var,
                    "group1": {
                        "name": str(group1_name),
                        "mean": _safe_float(group1_data[col].mean()),
                        "std": _safe_float(group1_data[col].std()),
                        "size": len(group1_data[col])
                    },
                    "group2": {
                        "name": str(group2_name),
                        "mean": _safe_float(group2_data[col].mean()),
                        "std": _safe_float(group2_data[col].std()),
                        "size": len(group2_data[col])
                    }
                }
            except Exception as e:
                t_test_results[col] = {
                    "test_type": "independent",
                    "error": str(e)
                }
                
        # 将方差齐性检验结果添加到返回结果中
        t_test_results["variance_test"] = variance_results
        
    elif test_type == "paired":
        # 配对样本T检验
        if len(numeric_columns) != 2:
            raise ValueError("配对样本T检验需要恰好2个数值列")
            
        col1, col2 = numeric_columns[0], numeric_columns[1]
        
        # 提取成对的数据（去除任一列的缺失值）
        paired_data = df[[col1, col2]].dropna()
        
        if len(paired_data) < 2:
            raise ValueError("配对样本T检验需要至少2对有效数据")
            
        try:
            # 执行配对样本T检验
            t_stat, p_value = ttest_rel(paired_data[col1], paired_data[col2])
            
            # 计算差异
            differences = paired_data[col1] - paired_data[col2]
            
            t_test_results["paired_test"] = {
                "test_type": "paired",
                "statistic": _safe_float(t_stat),
                "p_value": _safe_float(p_value),
                "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                "column1": col1,
                "column2": col2,
                "mean_difference": _safe_float(differences.mean()),
                "std_difference": _safe_float(differences.std()),
                "sample_size": len(differences)
            }
        except Exception as e:
            t_test_results["paired_test"] = {
                "test_type": "paired",
                "error": str(e)
            }
    else:
        raise ValueError(f"不支持的T检验类型: {test_type}")
    
    # 准备返回结果
    result = {
        "columns": numeric_columns,
        "test_type": test_type,
        "normality_test": normality_results,
        "t_test": t_test_results
    }
    
    return result


def text_to_numeric_or_datetime(file_path: str,columns: List[str],convert_to: str = "numeric",
    session_id: str = None,datetime_format: str = None) -> Dict[str, Any]:
    """
    文本转数值/时间 - 将包含千位分隔符、单位缩写（K,M等）的文本列转换为数值列，或将时间戳转换为时间列
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        convert_to (str): 转换目标类型 "numeric" 或 "datetime"
        datetime_format (str): 时间格式，如转换为时间时可指定格式，例如 "%Y-%m-%d %H:%M:%S"
        session_id (str): 会话ID
        
    Returns:
        Dict[str, Any]: 处理结果信息
    """
    df, _ = check_and_read(file_path, columns, session_id)
        
    # 处理列
    processed_columns = []
    
    if convert_to == "numeric":
        # 转换为数值
        for col in columns:
            # 处理带有 K, M, B 等单位的数值
            def convert_text_to_number(text):
                if pd.isna(text) or text == '':
                    return text
                    
                # 转换为字符串处理
                text = str(text).strip().lower()
                
                # 去除千位分隔符
                text = text.replace(',', '')
                
                # 定义单位映射
                units = {
                    'k': 10**3,
                    'm': 10**6,
                    'b': 10**9,
                    't': 10**12
                }
                
                # 检查是否以单位结尾
                if text[-1] in units:
                    try:
                        number = float(text[:-1])
                        return number * units[text[-1]]
                    except ValueError:
                        pass
                
                # 尝试直接转换为浮点数
                try:
                    return float(text)
                except ValueError:
                    # 如果转换失败，返回原始值
                    return text
            
            df[col] = df[col].apply(convert_text_to_number)
            processed_columns.append(col)
            
    elif convert_to == "datetime":
        # 转换为时间
        for col in columns:
            try:
                if datetime_format:
                    df[col] = pd.to_datetime(df[col], format=datetime_format)
                else:
                    df[col] = pd.to_datetime(df[col])
                processed_columns.append(col)
            except Exception as e:
                raise ValueError(f"列 {col} 转换为时间失败: {e}")
    else:
        raise ValueError(f"不支持的转换类型: {convert_to}，仅支持 'numeric' 或 'datetime'")
        
    # 保存处理后的数据
    new_filename, new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "saved_path": new_file_path,
        "processed_columns": processed_columns,
        "convert_to": convert_to
    }


def correlation_analysis(file_path: str,columns: List[str],method: str = "pearson",session_id: str = None) -> Dict[str, Any]:
    """
    相关性分析 - 计算并返回指定列之间的相关系数和p值
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要分析的列名列表
        method (str): 相关性计算方法 ("pearson", "spearman", "kendall")
        session_id (str): 会话ID
        
    Returns:
        Dict[str, Any]: 包含相关性分析结果的字典
    """
    df, numeric_columns = check_and_read(file_path, columns, session_id)
    
    from scipy.stats import pearsonr, spearmanr, kendalltau
    import warnings
    
    # 检查是否有常量列（方差为0的列）
    constant_columns = []
    for col in numeric_columns:
        col_data = df[col].dropna()
        if len(col_data) > 0 and col_data.var() == 0:
            constant_columns.append(col)
    
    if constant_columns:
        raise ValueError(f"以下列为常量列（所有值相同），无法计算相关性: {constant_columns}")
    
    # 计算相关系数和p值
    correlation_data = []
    n = len(numeric_columns)
    
    # 初始化相关性矩阵和p值矩阵
    corr_matrix = np.zeros((n, n))
    p_value_matrix = np.zeros((n, n))
    
    # 填充对角线（自相关性为1，p值为0）
    np.fill_diagonal(corr_matrix, 1.0)
    
    # 计算每对列之间的相关性
    for i in range(n):
        for j in range(i+1, n):
            col1 = numeric_columns[i]
            col2 = numeric_columns[j]
            
            # 删除任意一列有缺失值的行
            clean_data = df[[col1, col2]].dropna()
            
            if len(clean_data) < 2:
                # 数据不足，无法计算相关性
                corr = 0.0
                p_value = 1.0
            else:
                x = clean_data[col1]
                y = clean_data[col2]
                
                # 检查是否为常量列（在clean_data中）
                if x.var() == 0 or y.var() == 0:
                    # 常量列，相关性未定义
                    raise ValueError(f"列 '{col1}' 或 '{col2}' 在有效数据中为常量，无法计算相关性")
                
                try:
                    # 忽略ConstantInputWarning警告，我们已经进行了检查
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        if method == "pearson":
                            corr, p_value = pearsonr(x, y)
                        elif method == "spearman":
                            corr, p_value = spearmanr(x, y)
                        elif method == "kendall":
                            corr, p_value = kendalltau(x, y)
                        else:
                            raise ValueError(f"不支持的相关性计算方法: {method}")
                except Exception as e:
                    # 计算过程中出现异常，返回默认值
                    raise ValueError(f"计算相关性时出现异常: {e}")
            
            # 保存到相关性数据列表
            correlation_data.append({
                "column_x": col1,
                "column_y": col2,
                "correlation": round(float(corr), 6) if not pd.isna(corr) else 0.0,
                "p_value": round(float(p_value), 6) if not pd.isna(p_value) else 1.0
            })
            
            # 保存到矩阵中
            corr_matrix[i, j] = corr_matrix[j, i] = corr
            p_value_matrix[i, j] = p_value_matrix[j, i] = p_value
    
    # 构造相关性矩阵和p值矩阵的表格形式
    correlation_matrix = {
        "columns": numeric_columns,
        "correlations": corr_matrix.tolist(),
        "p_values": p_value_matrix.tolist()
    }
    
    # 准备返回结果
    result = {
        "method":method,
        "columns": numeric_columns,
        "correlation_data": correlation_data,
        "correlation_matrix": correlation_matrix
    }
    
    return result


def f_test(file_path: str, columns: List[str], session_id: str = None, group_by: str = None, alpha: float = 0.05) -> Dict[str, Any]:
    """
    F检验 - 用于检验多个样本的方差是否相等或进行方差分析(ANOVA)
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要分析的列名列表
        session_id (str): 会话ID
        group_by (str): 分组列名，用于进行组间方差分析
        alpha (float): 显著性水平 (默认0.05)

    Returns:
        Dict[str, Any]: 包含F检验结果的字典

    """
    df, numeric_columns = check_and_read(file_path, columns, session_id)
    
    # 检查是否有足够的数值列进行F检验
    if len(numeric_columns) < 2 and group_by is None:
        raise ValueError("F检验至少需要2个数值列")
    
    f_test_results = {}
    
    if group_by:
        # 按组进行方差分析(ANOVA)
        if group_by not in df.columns:
            raise ValueError(f"分组列 '{group_by}' 不存在于数据集中")
        
        # 获取唯一分组
        unique_groups = df[group_by].dropna().unique()
        
        if len(unique_groups) < 2:
            raise ValueError("分组数必须大于等于2才能进行方差分析")
        
        # 对每个数值列进行组间方差分析
        for col in numeric_columns:
            # 按组提取数据
            groups_data = []
            group_names = []
            group_stats = []  # 存储每组的统计信息
            
            for group in unique_groups:
                group_data = df[df[group_by] == group][col].dropna()
                if len(group_data) > 0:  # 只有当组内有数据时才添加
                    groups_data.append(group_data)
                    group_names.append(str(group))
                    # 计算每组的平均值和标准差
                    group_stats.append({
                        "name": str(group),
                        "mean": _safe_float(group_data.mean()),
                        "std": _safe_float(group_data.std()),
                        "size": len(group_data)
                    })
            
            if len(groups_data) < 2:
                f_test_results[col] = {
                    "error": "有效分组数少于2组，无法进行方差分析"
                }
                continue
            
            try:
                # 执行单因素方差分析
                f_stat, p_value = f_oneway(*groups_data)
                
                f_test_results[col] = {
                    "test_type": "anova",
                    "statistic": _safe_float(f_stat),
                    "p_value": _safe_float(p_value),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                    "groups": len(groups_data),
                    "group_names": group_names,
                    "sample_sizes": [len(group) for group in groups_data],
                    "group_stats": group_stats  # 添加组统计信息
                }
            except Exception as e:
                f_test_results[col] = {
                    "test_type": "anova",
                    "error": str(e)
                }
    else:
        # 方差齐性检验（Levene检验）
        # 对所有数值列进行方差齐性检验
        try:
            # 准备数据，确保每列都有相同数量的非空值
            cleaned_data = [df[col].dropna() for col in numeric_columns]
            
            # 使用Levene检验进行方差齐性检验
            f_stat, p_value = levene(*cleaned_data)
            
            f_test_results["variance_homogeneity"] = {
                "test_type": "levene",
                "statistic": _safe_float(f_stat),
                "p_value": _safe_float(p_value),
                "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                "equal_variance": bool(p_value > alpha) if _safe_float(p_value) is not None else True,
                "columns": numeric_columns,
                "sample_sizes": [len(data) for data in cleaned_data]
            }
        except Exception as e:
            f_test_results["variance_homogeneity"] = {
                "test_type": "levene",
                "error": str(e)
            }
    
    # 准备返回结果
    result = {
        "columns": numeric_columns,
        "f_test": f_test_results,
        "alpha": alpha
    }
    
    if group_by:
        result["group_by"] = group_by
    
    return result


def chi_square_test(file_path: str, columns: List[str], session_id: str = None, 
                   alpha: float = 0.05, group_by: str = None) -> Dict[str, Any]:
    """
    卡方检验 - 用于检验分类变量之间的独立性或拟合优度
    
    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要分析的列名列表（需要是分类变量列）
        session_id (str): 会话ID
        alpha (float): 显著性水平 (默认0.05)
        group_by (str): 分组列名，用于进行独立性检验（可选）
        
    Returns:
        Dict[str, Any]: 包含卡方检验结果的字典
    """
    
    df, _ = check_and_read(file_path, columns, session_id)
    
    # 检查列是否都是分类变量
    categorical_columns = []
    for col in columns:
        # 如果是数值型但唯一值较少，也可以当作分类变量处理
        if pd.api.types.is_numeric_dtype(df[col]):
            unique_count = df[col].nunique()
            if unique_count <= min(20, len(df[col]) * 0.1):  # 如果唯一值不超过20或者不超过总数的10%
                categorical_columns.append(col)
            else:
                raise ValueError(f"列 '{col}' 是数值型且唯一值过多，请先进行离散化处理")
        else:
            categorical_columns.append(col)
    
    if not categorical_columns:
        raise ValueError("没有有效的分类变量列可供处理")
    
    chi_square_results = {}
    
    if group_by:
        # 独立性检验：检验group_by列与其他列是否独立
        if group_by not in df.columns:
            raise ValueError(f"分组列 '{group_by}' 不存在于数据集中")
            
        # 检查group_by是否为分类变量

        if pd.api.types.is_numeric_dtype(df[group_by]):
            unique_count = df[group_by].nunique()
            if unique_count > min(20, len(df[group_by]) * 0.1):
                raise ValueError(f"分组列 '{group_by}' 是数值型且唯一值过多，请先进行离散化处理")

        # 对每个分类变量列与group_by列进行独立性检验
        for col in categorical_columns:
            if col == group_by:
                continue
                
            # 构建列联表
            contingency_table = pd.crosstab(df[group_by], df[col])
            
            # 检查列联表是否有效
            if contingency_table.size == 0:
                chi_square_results[col] = {
                    "error": "无法构建有效的列联表"
                }
                continue
                
            # 检查期望频数，确保至少80%的单元格期望频数大于5
            try:
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                # 计算期望频数小于5的单元格比例
                low_expected_ratio = (expected < 5).sum() / expected.size
                
                chi_square_results[col] = {
                    "test_type": "independence",
                    "contingency_table": contingency_table.values.tolist(),
                    "contingency_table_index": contingency_table.index.tolist(),
                    "contingency_table_columns": contingency_table.columns.tolist(),
                    "statistic": _safe_float(chi2),
                    "p_value": _safe_float(p_value),
                    "degrees_of_freedom": int(dof),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                    "low_expected_ratio": float(low_expected_ratio),  # 期望频数小于5的单元格比例
                    "warning": "期望频数过少" if low_expected_ratio > 0.2 else None
                }
            except Exception as e:
                chi_square_results[col] = {
                    "test_type": "independence",
                    "error": str(e)
                }
    else:
        # 拟合优度检验：检验各列的分布是否均匀
        for col in categorical_columns:
            # 计算观察频数
            observed_freq = df[col].value_counts()
            
            # 如果类别过多，合并低频类别
            if len(observed_freq) > 10:
                # 保留前9个最常见的类别，其余合并为"其他"
                top_categories = observed_freq.head(9)
                other_count = observed_freq.iloc[9:].sum()
                if other_count > 0:
                    observed_freq = pd.concat([top_categories, pd.Series([other_count], index=["其他"])])
            
            # 计算期望频数（均匀分布）
            expected_freq = np.full(len(observed_freq), observed_freq.sum() / len(observed_freq))
            
            # 执行卡方拟合优度检验
            try:
                from scipy.stats import chisquare
                chi2, p_value = chisquare(observed_freq.values, expected_freq)
                
                chi_square_results[col] = {
                    "test_type": "goodness_of_fit",
                    "categories": observed_freq.index.tolist(),
                    "observed_frequencies": observed_freq.values.tolist(),
                    "expected_frequencies": expected_freq.tolist(),
                    "statistic": _safe_float(chi2),
                    "p_value": _safe_float(p_value),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False
                }
            except Exception as e:
                chi_square_results[col] = {
                    "test_type": "goodness_of_fit",
                    "error": str(e)
                }
    
    # 准备返回结果
    result = {
        "columns": categorical_columns,
        "chi_square_test": chi_square_results,
        "alpha": alpha
    }
    
    if group_by:
        result["group_by"] = group_by
    
    return result


def non_parametric_test(file_path: str, columns: List[str], test_type: str = "mannwhitney",
                       session_id: str = None, group_by: str = None, alpha: float = 0.05, **kwargs) -> Dict[str, Any]:
    """
    非参数检验 - 提供多种非参数检验方法

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要分析的列名列表
        test_type (str): 非参数检验类型
            - "mannwhitney": Mann-Whitney U检验（两个独立样本）
            - "wilcoxon": Wilcoxon符号秩检验（两个相关样本）
            - "kruskal": Kruskal-Wallis检验（多个独立样本）
            - "kolmogorov_smirnov": Kolmogorov-Smirnov检验（单样本或两样本）
        session_id (str): 会话ID
        group_by (str): 分组列名，用于进行分组检验
        alpha (float): 显著性水平 (默认0.05)
        **kwargs: 其他参数
            - alternative: 检验方向 ("two-sided", "less", "greater")
            - distribution: 单样本K-S检验的理论分布 ("norm", "uniform", "expon", "logistic")

    Returns:
        Dict[str, Any]: 包含非参数检验结果的字典
    """

    df, numeric_columns = check_and_read(file_path, columns, session_id)

    # 获取参数
    alternative = kwargs.get("alternative", "two-sided")
    distribution = kwargs.get("distribution", "norm")

    non_parametric_results = {}

    if test_type == "mannwhitney":
        # Mann-Whitney U检验：用于比较两个独立样本的分布
        if not group_by:
            raise ValueError("Mann-Whitney U检验需要指定分组列 (group_by)")

        if group_by not in df.columns:
            raise ValueError(f"分组列 '{group_by}' 不存在于数据集中")

        # 检查分组列是否为分类变量
        if pd.api.types.is_numeric_dtype(df[group_by]):
            print(f"警告: 分组列 '{group_by}' 是数值型，建议确认是否为正确的分组变量")

        # 获取唯一分组
        unique_groups = df[group_by].dropna().unique()
        if len(unique_groups) != 2:
            raise ValueError(f"Mann-Whitney U检验要求分组列恰好有2个不同的组，当前有 {len(unique_groups)} 个组")

        # 提取两组数据
        group1_name, group2_name = unique_groups[0], unique_groups[1]
        group1_data = df[df[group_by] == group1_name][numeric_columns].dropna()
        group2_data = df[df[group_by] == group2_name][numeric_columns].dropna()

        # 对每个数值列执行Mann-Whitney U检验
        for col in numeric_columns:
            try:
                # 获取两组数据
                x = group1_data[col].values
                y = group2_data[col].values

                # 检查数据是否有效
                if len(x) == 0 or len(y) == 0:
                    non_parametric_results[col] = {
                        "test_type": "mannwhitney",
                        "error": f"组 '{group1_name}' 或 '{group2_name}' 中列 '{col}' 没有有效数据"
                    }
                    continue

                if len(x) < 3 or len(y) < 3:
                    non_parametric_results[col] = {
                        "test_type": "mannwhitney",
                        "error": f"组 '{group1_name}' 或 '{group2_name}' 中列 '{col}' 的样本量过小（<3）"
                    }
                    continue

                # 执行Mann-Whitney U检验
                stat, p_value = mannwhitneyu(x, y, alternative=alternative)

                non_parametric_results[col] = {
                    "test_type": "mannwhitney",
                    "statistic": _safe_float(stat),
                    "p_value": _safe_float(p_value),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                    "alternative": alternative,
                    "group1": {
                        "name": str(group1_name),
                        "median": _safe_float(np.median(x)),
                        "size": len(x)
                    },
                    "group2": {
                        "name": str(group2_name),
                        "median": _safe_float(np.median(y)),
                        "size": len(y)
                    }
                }
            except Exception as e:
                non_parametric_results[col] = {
                    "test_type": "mannwhitney",
                    "error": str(e)
                }

    elif test_type == "wilcoxon":
        # Wilcoxon符号秩检验：用于比较两个相关样本的分布
        if len(numeric_columns) != 2:
            raise ValueError("Wilcoxon符号秩检验需要恰好2个数值列")

        col1, col2 = numeric_columns[0], numeric_columns[1]

        # 提取成对的数据（去除任一列的缺失值）
        paired_data = df[[col1, col2]].dropna()

        if len(paired_data) < 3:
            raise ValueError("Wilcoxon符号秩检验需要至少3对有效数据")

        try:
            # 执行Wilcoxon符号秩检验
            stat, p_value = wilcoxon(paired_data[col1], paired_data[col2])

            # 计算差异
            differences = paired_data[col1] - paired_data[col2]

            non_parametric_results["paired_test"] = {
                "test_type": "wilcoxon",
                "statistic": _safe_float(stat),
                "p_value": _safe_float(p_value),
                "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                "alternative": alternative,
                "column1": col1,
                "column2": col2,
                "median_difference": _safe_float(np.median(differences)),
                "mean_difference": _safe_float(differences.mean()),
                "sample_size": len(differences)
            }
        except Exception as e:
            non_parametric_results["paired_test"] = {
                "test_type": "wilcoxon",
                "error": str(e)
            }

    elif test_type == "kruskal":
        # Kruskal-Wallis检验：用于比较多个独立样本的分布
        if group_by:
            # 按组进行Kruskal-Wallis检验
            if group_by not in df.columns:
                raise ValueError(f"分组列 '{group_by}' 不存在于数据集中")

            # 获取唯一分组
            unique_groups = df[group_by].dropna().unique()

            if len(unique_groups) < 2:
                raise ValueError("分组数必须大于等于2才能进行Kruskal-Wallis检验")

            # 对每个数值列进行Kruskal-Wallis检验
            for col in numeric_columns:
                # 按组提取数据
                groups_data = []
                group_names = []

                for group in unique_groups:
                    group_data = df[df[group_by] == group][col].dropna()
                    if len(group_data) > 0:  # 只有当组内有数据时才添加
                        groups_data.append(group_data.values)
                        group_names.append(str(group))

                if len(groups_data) < 2:
                    non_parametric_results[col] = {
                        "error": "有效分组数少于2组，无法进行Kruskal-Wallis检验"
                    }
                    continue

                if any(len(group_data) < 3 for group_data in groups_data):
                    non_parametric_results[col] = {
                        "error": "至少一个组的样本量过小（<3）"
                    }
                    continue

                try:
                    # 执行Kruskal-Wallis检验
                    stat, p_value = kruskal(*groups_data)

                    # 计算每组的中位数
                    group_stats = []
                    for i, group in enumerate(unique_groups):
                        group_data = df[df[group_by] == group][col].dropna()
                        group_stats.append({
                            "name": str(group),
                            "median": _safe_float(np.median(group_data)),
                            "size": len(group_data)
                        })

                    non_parametric_results[col] = {
                        "test_type": "kruskal",
                        "statistic": _safe_float(stat),
                        "p_value": _safe_float(p_value),
                        "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                        "groups": len(groups_data),
                        "group_names": group_names,
                        "group_stats": group_stats
                    }
                except Exception as e:
                    non_parametric_results[col] = {
                        "test_type": "kruskal",
                        "error": str(e)
                    }
        else:
            # 如果没有分组列，则需要提供多个数值列进行检验
            if len(numeric_columns) < 2:
                raise ValueError("Kruskal-Wallis检验至少需要2个数值列或指定分组列")

            # 准备数据
            data_to_test = [df[col].dropna().values for col in numeric_columns]

            # 检查数据量
            if any(len(data) < 3 for data in data_to_test):
                raise ValueError("Kruskal-Wallis检验中至少一个列的样本量过小（<3）")

            try:
                # 执行Kruskal-Wallis检验
                stat, p_value = kruskal(*data_to_test)

                non_parametric_results["kruskal_test"] = {
                    "test_type": "kruskal",
                    "statistic": _safe_float(stat),
                    "p_value": _safe_float(p_value),
                    "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                    "columns": numeric_columns,
                    "sample_sizes": [len(data) for data in data_to_test]
                }
            except Exception as e:
                non_parametric_results["kruskal_test"] = {
                    "test_type": "kruskal",
                    "error": str(e)
                }

    elif test_type == "kolmogorov_smirnov":
        # Kolmogorov-Smirnov检验：用于检验样本分布与理论分布的差异或两个样本的分布差异
        if group_by:
            # 两样本K-S检验：比较group_by列的两个组之间的数值列分布
            if group_by not in df.columns:
                raise ValueError(f"分组列 '{group_by}' 不存在于数据集中")

            # 获取唯一分组
            unique_groups = df[group_by].dropna().unique()
            if len(unique_groups) != 2:
                raise ValueError(f"Kolmogorov-Smirnov检验要求分组列恰好有2个不同的组，当前有 {len(unique_groups)} 个组")

            # 提取两组数据
            group1_name, group2_name = unique_groups[0], unique_groups[1]
            group1_data = df[df[group_by] == group1_name][numeric_columns].dropna()
            group2_data = df[df[group_by] == group2_name][numeric_columns].dropna()

            # 对每个数值列执行两样本K-S检验
            for col in numeric_columns:
                try:
                    # 获取两组数据
                    x = group1_data[col].values
                    y = group2_data[col].values

                    # 检查数据是否有效
                    if len(x) == 0 or len(y) == 0:
                        non_parametric_results[col] = {
                            "test_type": "kolmogorov_smirnov",
                            "error": f"组 '{group1_name}' 或 '{group2_name}' 中列 '{col}' 没有有效数据"
                        }
                        continue

                    if len(x) < 3 or len(y) < 3:
                        non_parametric_results[col] = {
                            "test_type": "kolmogorov_smirnov",
                            "error": f"组 '{group1_name}' 或 '{group2_name}' 中列 '{col}' 的样本量过小（<3）"
                        }
                        continue

                    # 执行两样本K-S检验
                    stat, p_value = ks_2samp(x, y)

                    non_parametric_results[col] = {
                        "test_type": "kolmogorov_smirnov",
                        "statistic": _safe_float(stat),
                        "p_value": _safe_float(p_value),
                        "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                        "group1": {
                            "name": str(group1_name),
                            "size": len(x)
                        },
                        "group2": {
                            "name": str(group2_name),
                            "size": len(y)
                        }
                    }
                except Exception as e:
                    non_parametric_results[col] = {
                        "test_type": "kolmogorov_smirnov",
                        "error": str(e)
                    }
        else:
            # 单样本K-S检验：检验数值列是否符合某种理论分布
            for col in numeric_columns:
                col_data = df[col].dropna().values

                if len(col_data) < 3:
                    non_parametric_results[col] = {
                        "test_type": "kolmogorov_smirnov",
                        "error": f"列 '{col}' 的样本量过小（<3）"
                    }
                    continue

                try:
                    # 执行单样本K-S检验，检验数据是否符合指定的理论分布
                    if distribution == "norm":
                        stat, p_value = kstest(col_data, 'norm',
                                              args=(np.mean(col_data), np.std(col_data, ddof=1)))
                    elif distribution == "uniform":
                        stat, p_value = kstest(col_data, 'uniform',
                                              args=(np.min(col_data), np.max(col_data)-np.min(col_data)))
                    elif distribution == "expon":
                        stat, p_value = kstest(col_data, 'expon',
                                              args=(0, np.mean(col_data)))
                    elif distribution == "logistic":
                        from scipy.stats import logistic
                        stat, p_value = kstest(col_data, 'logistic',
                                              args=(np.mean(col_data), np.std(col_data, ddof=1)/np.sqrt(3.0)))
                    else:
                        # 默认使用正态分布
                        stat, p_value = kstest(col_data, 'norm',
                                              args=(np.mean(col_data), np.std(col_data, ddof=1)))

                    non_parametric_results[col] = {
                        "test_type": "kolmogorov_smirnov",
                        "statistic": _safe_float(stat),
                        "p_value": _safe_float(p_value),
                        "significant": bool(p_value < alpha) if _safe_float(p_value) is not None else False,
                        "distribution": distribution,
                        "sample_size": len(col_data)
                    }
                except Exception as e:
                    non_parametric_results[col] = {
                        "test_type": "kolmogorov_smirnov",
                        "error": str(e)
                    }

    else:
        raise ValueError(f"不支持的非参数检验类型: {test_type}，支持的类型: 'mannwhitney', 'wilcoxon', 'kruskal', 'kolmogorov_smirnov'")

    # 准备返回结果
    result = {
        "columns": numeric_columns,
        "test_type": test_type,
        "non_parametric_test": non_parametric_results,
        "alpha": alpha
    }

    if group_by:
        result["group_by"] = group_by

    return result
