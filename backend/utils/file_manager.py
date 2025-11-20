import os
import shutil
import uuid
import pandas as pd

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
    original_target_path = target_path
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
        column_names (list): 列名列表
        session_id (str, optional): 用户会话ID
        mode (str): 操作模式，"add"表示添加标题行，"modify"表示修改现有标题行
        
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
    else:
        # 修改模式：读取已有标题行的文件
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    
    # 检查列数是否匹配
    if len(column_names) != len(df.columns):
        raise ValueError(f"提供的列名数量({len(column_names)})与文件列数({len(df.columns)})不匹配")
    
    # 设置列名
    df.columns = column_names
    
    # 获取原始文件名（不含扩展名）
    original_filename = os.path.splitext(os.path.basename(file_path))[0]
    
    # 生成新文件名，格式为"原文件名_add_header_N" 或 "原文件名_modify_header_N"
    counter = 1
    while True:
        if mode == "add":
            new_filename = f"{original_filename}_add_header_{counter}"
        else:
            new_filename = f"{original_filename}_modify_header_{counter}"
        new_file_path = get_file_path(new_filename, session_id)
        if not os.path.exists(new_file_path):
            break
        counter += 1
    
    # 保存新文件
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")
    
    return {
        "data_id": new_filename,
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
        "saved_path": new_file_path
    }
