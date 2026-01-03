from typing import List, Dict, Any
import pandas as pd
from . import check_and_read
from ..file_manager import generate_new_file_path


def text_to_numeric_or_datetime(file_path: str, columns: List[str], convert_to: str = "numeric",
                                session_id: str = None, datetime_format: str = None) -> Dict[str, Any]:
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
                    'k': 10 ** 3,
                    'm': 10 ** 6,
                    'b': 10 ** 9,
                    't': 10 ** 12
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
