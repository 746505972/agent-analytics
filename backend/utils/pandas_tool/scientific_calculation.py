from typing import List, Dict, Any
import numpy as np

from ..file_manager import generate_new_file_path
from .check_and_read import check_and_read

def scientific_calculation(file_path: str, columns: List[str], operation: str,
                           params: Dict[str, Any] = None, session_id: str = None) -> Dict[str, Any]:
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
