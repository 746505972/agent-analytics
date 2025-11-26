import os
import uuid
from typing import Any, List

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

DATA_DIR = "data"


def ensure_data_dir():
    """确保 data 目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def ensure_session_dir(session_id: str):
    """确保用户session目录存在"""
    session_dir = os.path.join(DATA_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


def read_any_file(file_path: str) -> pd.DataFrame:
    """
    自动识别 CSV / Excel 文件并读取。
    CSV 使用 utf-8-sig 防止 BOM 和乱码。
    项目实际运行时会把用户上传的文件转成csv因此用不到，该方法主要用于单元测试
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".csv", ".txt"]:
        return pd.read_csv(file_path, encoding="utf-8-sig")

    elif ext in [".xlsx", ".xls"]:
        # 读取Excel文件的第一个工作表
        return pd.read_excel(file_path, sheet_name=0)

    else:
        raise ValueError(f"不支持的文件格式：{ext}")


def get_file_path(data_id: str, session_id: str = None) -> str:
    """
    获取文件路径，支持session隔离
    """
    if session_id:
        return os.path.join(DATA_DIR, session_id, f"{data_id}.csv")
    else:
        return os.path.join(DATA_DIR, f"{data_id}.csv")


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全的字符
    """
    # 移除或替换不安全的字符
    unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # 移除开头和结尾的空格和点
    filename = filename.strip('. ')
    
    # 如果文件名为空，生成一个默认名称
    if not filename:
        filename = "untitled"
    
    return filename


def upload_file(file_path: str, original_filename: str = None, session_id: str = None) -> dict:
    """
    上传 CSV/Excel 文件：
    1. 自动识别格式
    2. 读入 DataFrame
    3. 保存为 data/<session_id>/<original_filename>.csv（统一转换为 UTF-8 CSV）
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    # 如果有session_id，确保session目录存在
    if session_id:
        ensure_session_dir(session_id)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    df = read_any_file(file_path)

    # 检查DataFrame是否为空
    if df.empty:
        raise ValueError("上传的文件为空或无法读取有效数据")

    # 使用原始文件名作为data_id（清理不安全字符）
    if original_filename:
        # 移除扩展名并清理文件名
        data_id = os.path.splitext(original_filename)[0]
        data_id = sanitize_filename(data_id)
    else:
        # 如果没有原始文件名，生成一个随机ID
        data_id = str(uuid.uuid4())[:8]
    
    # 构建目标路径
    if session_id:
        target_path = os.path.join(DATA_DIR, session_id, f"{data_id}.csv")
    else:
        target_path = os.path.join(DATA_DIR, f"{data_id}.csv")

    # 如果文件已存在，添加序号
    counter = 1
    while os.path.exists(target_path):
        name_part = data_id
        if counter > 1:
            name_part = f"{data_id}_{counter}"
        
        if session_id:
            target_path = os.path.join(DATA_DIR, session_id, f"{name_part}.csv")
        else:
            target_path = os.path.join(DATA_DIR, f"{name_part}.csv")
        counter += 1

    # 保存成 UTF-8 CSV
    df.to_csv(target_path, index=False, encoding="utf-8-sig")

    # 从最终路径中提取实际使用的data_id
    actual_data_id = os.path.splitext(os.path.basename(target_path))[0]

    return {
        "data_id": actual_data_id,
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
        "saved_path": target_path
    }


def delete_file(data_id: str, session_id: str = None):
    """
    删除指定的数据文件
    """
    file_path = get_file_path(data_id, session_id)
    if os.path.exists(file_path):
        os.remove(file_path)

def generate_new_file_path(file_path , session_id):
    original_filename = os.path.splitext(os.path.basename(file_path))[0]

    # 根据文件名决定新文件名
    if original_filename.endswith('_edit'):
        # 如果已经是编辑过的文件，则在原文件基础上修改
        new_filename = original_filename
    else:
        # 第一次编辑，添加 _edit 后缀
        new_filename = f"{original_filename}_edit"

    return new_filename,get_file_path(new_filename, session_id)


def add_header_to_file(file_path: str, column_names: list, session_id: str = None, mode: str = "add") -> dict:
    """
    为没有标题行的CSV文件添加标题行，创建新文件而不覆盖原文件
    
    Args:
        file_path (str): 原始文件路径
        column_names (list): 列名列表(当mode="remove"时可以为空)
        session_id (str, optional): 用户会话ID
        mode (str): 操作模式，"add"表示添加标题行，"modify"表示修改现有标题行，"remove"表示删除第一行
        
    Returns:
        dict: 包含新文件信息的字典
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    if mode == "add":
        # 添加模式：读取没有标题行的文件
        df = pd.read_csv(file_path, header=None, encoding="utf-8-sig")
    elif mode == "remove":
        # 删除模式：读取文件并删除第一行
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    else:
        # 修改模式：读取已有标题行的文件
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    
    # 检查列数是否匹配（仅适用于add和modify模式）
    if mode != "remove" and len(column_names) != len(df.columns):
        raise ValueError(f"提供的列名数量({len(column_names)})与文件列数({len(df.columns)})不匹配")
    
    # 设置列名（仅适用于add和modify模式）
    if mode != "remove":
        df.columns = column_names
    else:
        df.columns = df.iloc[0]
        df = df[1:]

    new_filename,new_file_path = generate_new_file_path(file_path, session_id)
    
    # 保存新文件
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "saved_path": new_file_path
    }


def remove_invalid_samples(file_path: str, session_id: str = None,
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

    Returns:
        dict: 处理结果和统计信息
    """
    # 确保数据目录存在
    ensure_data_dir()

    if session_id:
        ensure_session_dir(session_id)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    df = read_any_file(file_path)

    # 记录处理统计信息
    cleaning_stats = {
        'duplicates_removed': 0,
        'duplicate_cols_removed': 0,
        'constant_cols_removed': 0,
        'rows_removed': 0,
        'columns_removed': 0,
    }

    # 1. 去除重复行（如果启用）
    if remove_duplicates:
        before_dup = len(df)
        df = df.drop_duplicates()
        cleaning_stats['duplicates_removed'] = before_dup - len(df)

    # 2. 删除重复列（如果启用）
    if remove_duplicate_cols:
        before_cols = len(df.columns)
        df = df.T.drop_duplicates().T
        cleaning_stats['duplicate_cols_removed'] = before_cols - len(df.columns)

    # 3. 删除所有数据都相同的列（如果启用）
    if remove_constant_cols:
        before_cols = len(df.columns)
        constant_cols = []
        for col in df.columns:
            if df[col].nunique() <= 1:  # 只有一个唯一值或全部为NaN
                constant_cols.append(col)
        df = df.drop(columns=constant_cols)
        cleaning_stats['constant_cols_removed'] = before_cols - len(df.columns)

    # 4. 处理缺失值超过阈值的行
    if row_missing_threshold < 1:
        row_missing_ratio = df.isnull().sum(axis=1) / df.shape[1]
        rows_before = len(df)
        df = df[row_missing_ratio <= row_missing_threshold]
        cleaning_stats['rows_removed'] = rows_before - len(df)

    # 5. 处理缺失值超过阈值的列
    if col_missing_threshold < 1:
        col_missing_ratio = df.isnull().sum() / df.shape[0]
        cols_before = len(df.columns)
        df = df.loc[:, col_missing_ratio <= col_missing_threshold]
        cleaning_stats['columns_removed'] = cols_before - len(df.columns)

    new_filename,new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")

    return {
        "data_id": new_filename,
        "saved_path": new_file_path,
        "cleaning_stats": cleaning_stats,
    }


def handle_missing_values(file_path: str, session_id: str = None,
                          row_handling: str = "interpolate",
                          col_handling: str = "interpolate",
                          interpolation_method: str = "linear",
                          fill_value: Any = None,
                          knn_neighbors: int = 5,
                          specified_columns: List[str] = None,
                          temporal_columns: List[str] = None) -> dict:
    """
    处理缺失值 - 对行列缺失值进行插值或填充

    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        # TODO: 检查"constant"和"fill"是否重复
        row_handling (str): 行处理方式 ("interpolate", "fill")
        col_handling (str): 列处理方式 ("interpolate", "fill")
        interpolation_method (str): 插值方法 ("linear", "ffill", "bfill", "mean", "median", "mode", "knn", "constant")
        fill_value (Any): 当使用constant方法时的填充值
        knn_neighbors (int): KNN插值的邻居数量
        specified_columns (List[str]): 指定要处理的列名列表，如果为None则处理所有列
        temporal_columns (List[str]): 时间序列列名列表

    Returns:
        dict: 处理结果和统计信息
    """
    # 确保数据目录存在
    ensure_data_dir()

    if session_id:
        ensure_session_dir(session_id)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    df = read_any_file(file_path)

    # 确定要处理的列
    if specified_columns is None:
        # 未指定列，处理所有列
        columns_to_process = df.columns.tolist()
    else:
        # 过滤出数据集中存在的列
        columns_to_process = [col for col in specified_columns if col in df.columns]
        missing_columns = set(specified_columns) - set(columns_to_process)
        if missing_columns:
            print(f"警告: 以下列不存在于数据集中: {missing_columns}")

    # 记录处理统计信息
    filling_stats = {
        'missing_filled': 0,
        'columns_processed': columns_to_process,
        'methods_used': {}
    }

    # 处理缺失值
    if row_handling == "interpolate" or col_handling == "interpolate":
        # 插值处理
        df, stats = _interpolate_missing_values(df, columns_to_process, interpolation_method,
                                                fill_value, knn_neighbors, temporal_columns)
    else:
        # 填充处理
        df, stats = _fill_missing_values(df, columns_to_process, interpolation_method,
                                         fill_value, temporal_columns)

    filling_stats['missing_filled'] = stats['missing_filled']
    filling_stats['methods_used'] = stats['methods_used']
    filling_stats['total_missing_after'] = df.isnull().sum().sum()

    # 保存处理后的数据
    new_filename,new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")

    return {
        "processed_rows": df.shape[0],
        "processed_cols": df.shape[1],
        "remaining_missing_count": int(filling_stats['total_missing_after']),
        "missing_filled_count": int(filling_stats['missing_filled']),
        "data_id": new_filename,
        "saved_path": new_file_path,
    }


def _interpolate_missing_values(df: pd.DataFrame, columns: List[str], method: str,
                                fill_value: Any, knn_neighbors: int, temporal_columns: List[str]) -> tuple:
    """插值处理缺失值"""
    df_copy = df.copy()
    total_filled = 0
    methods_used = {}

    # 如果使用KNN方法，需要特殊处理
    if method == "knn":
        numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(df_copy[col])]
        if numeric_cols:
            knn_imputer = KNNImputer(n_neighbors=knn_neighbors)
            df_copy[numeric_cols] = knn_imputer.fit_transform(df_copy[numeric_cols])
            filled_count = df_copy[numeric_cols].isnull().sum().sum()
            total_filled += filled_count
            methods_used['knn'] = {'columns': numeric_cols, 'filled': filled_count}

    # 处理其他列
    for column in columns:
        if method == "knn" and pd.api.types.is_numeric_dtype(df_copy[column]):
            continue  # 已经在KNN中处理过了

        if df_copy[column].isnull().sum() == 0:
            continue

        original_null_count = df_copy[column].isnull().sum()

        if pd.api.types.is_numeric_dtype(df_copy[column]):
            # 数值型数据
            if method in ["linear", "ffill", "bfill"]:
                df_copy[column] = df_copy[column].interpolate(method=method, limit_direction='both')
            elif method == "mean":
                df_copy[column] = df_copy[column].interpolate(method='linear').fillna(df_copy[column].mean())
            elif method == "median":
                df_copy[column] = df_copy[column].interpolate(method='linear').fillna(df_copy[column].median())
            else:
                df_copy[column] = df_copy[column].interpolate()

        elif pd.api.types.is_datetime64_any_dtype(df_copy[column]):
            # 时间型数据
            if method in ["linear", "ffill", "bfill"]:
                df_copy[column] = df_copy[column].interpolate(method=method, limit_direction='both')
            else:
                df_copy[column] = df_copy[column].interpolate(method='linear')

        else:
            # 分类型数据 - 使用填充方法
            if method == "ffill":
                df_copy[column] = df_copy[column].fillna(method='ffill')
            elif method == "bfill":
                df_copy[column] = df_copy[column].fillna(method='bfill')
            else:
                df_copy[column] = df_copy[column].fillna("Missing")

        filled_count = original_null_count - df_copy[column].isnull().sum()
        total_filled += filled_count
        methods_used[column] = {'method': method, 'filled': filled_count}

    return df_copy, {'missing_filled': total_filled, 'methods_used': methods_used}


def _fill_missing_values(df: pd.DataFrame, columns: List[str], method: str,
                         fill_value: Any, temporal_columns: List[str]) -> tuple:
    """填充处理缺失值"""
    df_copy = df.copy()
    total_filled = 0
    methods_used = {}

    for column in columns:
        if df_copy[column].isnull().sum() == 0:
            continue

        original_null_count = df_copy[column].isnull().sum()

        if pd.api.types.is_numeric_dtype(df_copy[column]):
            # 数值型数据
            if method == "mean":
                df_copy[column] = df_copy[column].fillna(df_copy[column].mean())
            elif method == "median":
                df_copy[column] = df_copy[column].fillna(df_copy[column].median())
            elif method == "constant":
                fill_val = fill_value if fill_value is not None else 0
                df_copy[column] = df_copy[column].fillna(fill_val)
            else:
                df_copy[column] = df_copy[column].fillna(df_copy[column].mean())

        elif pd.api.types.is_datetime64_any_dtype(df_copy[column]):
            # 时间型数据
            if method == "constant":
                fill_val = fill_value if fill_value is not None else pd.Timestamp.now()
                df_copy[column] = df_copy[column].fillna(fill_val)
            elif method == "ffill":
                df_copy[column] = df_copy[column].fillna(method='ffill')
            elif method == "bfill":
                df_copy[column] = df_copy[column].fillna(method='bfill')
            else:
                df_copy[column] = df_copy[column].fillna(method='ffill')

        else:
            # 分类型数据
            if method == "mode":
                mode_value = df_copy[column].mode()
                fill_val = mode_value[0] if len(mode_value) > 0 else "Unknown"
                df_copy[column] = df_copy[column].fillna(fill_val)
            elif method == "constant":
                fill_val = fill_value if fill_value is not None else "Unknown"
                df_copy[column] = df_copy[column].fillna(fill_val)
            elif method == "ffill":
                df_copy[column] = df_copy[column].fillna(method='ffill')
            elif method == "bfill":
                df_copy[column] = df_copy[column].fillna(method='bfill')
            else:
                df_copy[column] = df_copy[column].fillna("Missing")

        filled_count = original_null_count - df_copy[column].isnull().sum()
        total_filled += filled_count
        methods_used[column] = {'method': method, 'filled': filled_count}

    return df_copy, {'missing_filled': total_filled, 'methods_used': methods_used}


def _convert_to_serializable(x):
    """将值转换为可JSON序列化的格式"""
    if pd.isna(x) or x is None:
        return None
    if hasattr(x, 'item'):
        try:
            return x.item()
        except (ValueError, OverflowError):
            return str(x)
    if hasattr(x, 'strftime'):
        return x.strftime('%Y-%m-%d %H:%M:%S')
    return x



def edit_file_data(file_path: str, edit_func, session_id: str = None, *args, **kwargs) -> dict:
    """
    通用文件编辑函数，在文件上应用自定义编辑操作
    
    Args:
        file_path (str): 要编辑的文件路径
        edit_func (callable): 执行实际数据编辑的函数，应该接受DataFrame作为第一个参数
        session_id (str, optional): 用户会话ID
        *args, **kwargs: 传递给edit_func的额外参数
        
    Returns:
        dict: 包含新文件信息的字典
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    df = read_any_file(file_path)
    # 应用编辑函数
    df = edit_func(df, *args, **kwargs)
    
    new_filename,new_file_path = generate_new_file_path(file_path, session_id)
    
    # 保存编辑后的数据
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    # 处理NaN值，将其替换为None以便JSON序列化
    df = df.replace({pd.NA: None, pd.NaT: None, np.nan: None})
    
    # 再次确保所有值都可以被JSON序列化
    for col in df.columns:
        def convert_value(x):
            if pd.isna(x) or x is None:
                return None
            if hasattr(x, 'item'):
                try:
                    return x.item()
                except (ValueError, OverflowError):
                    return str(x)
            return x
        df[col] = df[col].apply(convert_value)
    
    return {
        "data_id": new_filename,
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
        "saved_path": new_file_path,
    }

def test():
    file_path = f"data/100/asd.xlsx"
    result=handle_missing_values(file_path, session_id = "100",
                              row_handling = "interpolate",
                              col_handling = "interpolate",
                              interpolation_method= "linear",
                              fill_value= None,
                              specified_columns= None,
                              temporal_columns= None)

    print(json.dumps(result, indent=4, ensure_ascii=False))

def test2():
    file_path = f"data/100/asd.xlsx"
    result = remove_invalid_samples(file_path,"100",True, True, True,
                                    0.5,0.5)
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    import json
    test2()