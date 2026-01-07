from typing import List, Dict, Any
from .check_and_read import check_and_read
import pandas as pd

def statistical_summary(file_path: str, columns: List[str], session_id: str = None) -> Dict[str, Any]:
    """
    统计摘要 - 计算并返回指定列的统计摘要信息

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        session_id (str): 会话ID

    Returns:
        Dict[str, Any]: 包含统计摘要信息的字典，格式适合 echarts 绘制表格
    """

    df, numeric_columns = check_and_read(file_path, columns, session_id, True)

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
