import os
import shutil
import uuid
import pandas as pd
import numpy as np


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
    
    # 获取原始文件名（不含扩展名）
    original_filename = os.path.splitext(os.path.basename(file_path))[0]
    
    # 根据文件名决定新文件名
    if original_filename.endswith('_edit'):
        # 如果已经是编辑过的文件，则在原文件基础上修改
        new_filename = original_filename
    else:
        # 第一次编辑，添加 _edit 后缀
        new_filename = f"{original_filename}_edit"
    
    new_file_path = get_file_path(new_filename, session_id)
    
    # 保存新文件
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "saved_path": new_file_path
    }


def clean_data_file(file_path: str, session_id: str = None, remove_duplicates: bool = False,
                   row_missing_threshold: float = 1, col_missing_threshold: float = 1,
                   row_handling: str = "delete", col_handling: str = "delete") -> dict:
    """
    清洗数据文件
    
    Args:
        file_path (str): 文件路径
        session_id (str): session_id
        remove_duplicates (bool): 是否去除重复行
        row_missing_threshold (float): 行缺失值阈值
        col_missing_threshold (float): 列缺失值阈值
        row_handling (str): 行处理方式 ("delete" or "interpolate")
        col_handling (str): 列处理方式 ("delete" or "interpolate")
    """
    # 确保数据目录存在
    ensure_data_dir()
    
    if session_id:
        ensure_session_dir(session_id)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    
    # 记录清洗前的信息
    original_shape = df.shape
    original_rows = original_shape[0]
    original_cols = original_shape[1]
    
    # 1. 去除重复行（如果启用）
    if remove_duplicates:
        df = df.drop_duplicates()
    
    # 2. 处理缺失值 - 行处理
    if row_handling == "delete":
        # 删除缺失值比例超过阈值的行
        row_missing_ratio = df.isnull().sum(axis=1) / df.shape[1]
        df = df[row_missing_ratio <= row_missing_threshold]
    elif row_handling == "interpolate":
        # 对数值列进行插值处理
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].interpolate()
    
    # 3. 处理缺失值 - 列处理
    if col_handling == "delete":
        # 删除缺失值比例超过阈值的列
        col_missing_ratio = df.isnull().sum() / df.shape[0]
        df = df.loc[:, col_missing_ratio <= col_missing_threshold]
    elif col_handling == "interpolate":
        # 对数值列进行插值处理
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].interpolate()
    
    # 获取原始文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 根据文件名决定新文件名
    if base_name.endswith('_edit'):
        # 如果已经是编辑过的文件，则在原文件基础上修改
        new_filename = base_name
    else:
        # 第一次编辑，添加 _edit 后缀
        new_filename = f"{base_name}_edit"
    
    new_file_path = get_file_path(new_filename, session_id)
    
    # 保存清洗后的数据
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
        "original_rows": original_rows,
        "original_cols": original_cols,
        "cleaned_rows": df.shape[0],
        "cleaned_cols": df.shape[1],
        "removed_rows": original_rows - df.shape[0],
        "removed_cols": original_cols - df.shape[1],
        "data_id": new_filename,
        "saved_path": new_file_path,
    }


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
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    
    # 应用编辑函数
    df = edit_func(df, *args, **kwargs)
    
    # 获取原始文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 根据文件名决定新文件名
    if base_name.endswith('_edit'):
        # 如果已经是编辑过的文件，则在原文件基础上修改
        new_filename = base_name
    else:
        # 第一次编辑，添加 _edit 后缀
        new_filename = f"{base_name}_edit"
    
    new_file_path = get_file_path(new_filename, session_id)
    
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
