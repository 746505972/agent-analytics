import os
import pandas as pd
from utils.file_manager import ensure_session_dir, read_any_file
from typing import List

def check_and_read(file_path: str, columns: List[str], session_id: str = None, select_all_cols: bool = False) -> tuple:
    """
    检查文件和列的有效性，并读取数据

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        session_id (str): 会话ID
        select_all_cols (bool): 默认选全部列

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

    if not columns:
        raise ValueError("没有指定列")

    if select_all_cols:
        columns = df.columns

    # 只选择数值型列进行处理
    numeric_columns = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]

    if not numeric_columns:
        raise ValueError("没有有效的数值型列可供处理")

    return df, numeric_columns
