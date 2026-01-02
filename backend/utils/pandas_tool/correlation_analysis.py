from typing import List, Dict, Any
from .check_and_read import check_and_read
from scipy.stats import pearsonr, spearmanr, kendalltau
import warnings
import numpy as np
import pandas as pd

def correlation_analysis(file_path: str, columns: List[str], method: str = "pearson", session_id: str = None) -> Dict[
    str, Any]:
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
        for j in range(i + 1, n):
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
        "method": method,
        "columns": numeric_columns,
        "correlation_data": correlation_data,
        "correlation_matrix": correlation_matrix
    }

    return result

