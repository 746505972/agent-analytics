# file_manager.py
import os
import shutil
import uuid
import pandas as pd

DATA_DIR = "data"


def ensure_data_dir():
    """确保 data 目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)


def read_any_file(file_path: str) -> pd.DataFrame:
    """
    自动识别 CSV / Excel 文件并读取。
    CSV 使用 utf-8-sig 防止 BOM 和乱码。
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".csv", ".txt"]:
        return pd.read_csv(file_path, encoding="utf-8-sig")

    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)

    else:
        raise ValueError(f"不支持的文件格式：{ext}")


def upload_file(file_path: str) -> dict:
    """
    上传 CSV/Excel 文件：
    1. 自动识别格式
    2. 读入 DataFrame
    3. 保存为 data/<uuid>.csv（统一转换为 UTF-8 CSV）
    """
    ensure_data_dir()

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 读取文件
    df = read_any_file(file_path)

    # 生成短 data_id
    data_id = str(uuid.uuid4())[:8]
    target_path = os.path.join(DATA_DIR, f"{data_id}.csv")

    # 保存成 UTF-8 CSV
    df.to_csv(target_path, index=False, encoding="utf-8-sig")

    return {
        "data_id": data_id,
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
        "saved_path": target_path
    }
