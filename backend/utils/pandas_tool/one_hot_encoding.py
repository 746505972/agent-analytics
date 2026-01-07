from typing import List, Dict, Any
from .check_and_read import check_and_read
from ..file_manager import generate_new_file_path


def one_hot_encoding(file_path: str, columns: List[str], session_id: str = None,
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
