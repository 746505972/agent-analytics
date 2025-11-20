import sys
import os
import urllib.parse

# 添加项目根目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
import logging

try:
    from utils.file_manager import get_file_path, delete_file, sanitize_filename
except ImportError:
    # 最后尝试直接添加到路径并导入
    sys.path.insert(0, os.path.join(parent_dir, "utils"))
    from utils.file_manager import get_file_path, delete_file, sanitize_filename

router = APIRouter(prefix="/data", tags=["data"])

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user_files_list(session_id: str) -> list:
    """
    获取用户上传的文件列表
    
    Args:
        session_id (str): 用户会话ID
        
    Returns:
        list: 文件信息列表
    """
    # 构建用户目录路径
    user_dir = os.path.join("data", session_id)
    
    # 检查目录是否存在
    if not os.path.exists(user_dir):
        return []
    
    # 获取目录中的所有CSV文件
    files = []
    for filename in os.listdir(user_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(user_dir, filename)
            if os.path.isfile(file_path):
                try:
                    # 获取文件信息
                    stat = os.stat(file_path)
                    df = pd.read_csv(file_path, encoding="utf-8-sig")
                    # 处理NaN值，将其替换为None以便JSON序列化
                    df = df.replace({pd.NA: None, pd.NaT: None, np.nan: None})
                    
                    files.append({
                        "data_id": os.path.splitext(filename)[0],
                        "filename": filename,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "size": stat.st_size,
                        "modified": stat.st_mtime
                    })
                except Exception as e:
                    # 如果某个文件读取出错，跳过该文件
                    logger.error(f"读取文件 {filename} 时出错: {str(e)}")
                    continue
    
    return files


@router.get("/user/files")
async def get_user_files(request: Request):
    """
    获取用户上传的文件列表
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        files = get_user_files_list(session_id)
        
        return JSONResponse(content={
            "success": True,
            "data": files
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@router.get("/{data_id}")
async def get_data_preview(request: Request, data_id: str, page: int = 1, page_size: int = 10):
    """
    获取数据预览接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建文件路径
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 读取CSV文件
        try:
            df = pd.read_csv(file_path, encoding="utf-8-sig")
        except Exception as e:
            logger.error(f"读取文件 {file_path} 失败: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"读取文件失败: {str(e)}"
                }
            )
        
        # 检查DataFrame是否为空
        if df.empty:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "数据文件为空"
                }
            )
        
        # 计算分页信息
        total_rows = len(df)
        total_pages = (total_rows + page_size - 1) // page_size
        
        # 获取当前页数据
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = df.iloc[start_idx:end_idx]
        
        # 处理NaN值，将其替换为None以便JSON序列化
        page_data = page_data.replace({pd.NA: None, pd.NaT: None, np.nan: None})
        
        # 将numpy数据类型转换为Python原生数据类型
        for col in page_data.columns:
            def convert_value(x):
                if pd.isna(x) or x is None:
                    return None
                if hasattr(x, 'item'):
                    try:
                        return x.item()
                    except (ValueError, OverflowError):
                        return str(x)
                return x
            page_data[col] = page_data[col].apply(convert_value)
        
        # 再次处理可能遗漏的NaN值
        page_data = page_data.replace({pd.NA: None, pd.NaT: None, np.nan: None})
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "data_id": data_id,
                "columns": list(df.columns),
                "rows": total_rows,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "data": page_data.to_dict('records')
            }
        })
    except Exception as e:
        logger.error(f"获取数据预览时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@router.get("/{data_id}/info")
async def get_data_info(request: Request, data_id: str):
    """
    获取数据文件信息接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建文件路径
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 读取CSV文件
        try:
            df = pd.read_csv(file_path, encoding="utf-8-sig")
        except Exception as e:
            logger.error(f"读取文件 {file_path} 失败: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": f"读取文件失败: {str(e)}"
                }
            )
        
        # 检查DataFrame是否为空
        if df.empty:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "数据文件为空"
                }
            )
        
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
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "data_id": data_id,
                "filename": f"{data_id}.csv",
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
        })
    except Exception as e:
        logger.error(f"获取数据信息时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@router.delete("/{data_id}")
async def delete_data(request: Request, data_id: str):
    """
    删除数据文件接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        logger.info(f"尝试删除数据文件: {data_id}, session_id: {session_id}")
        
        # 删除文件时检查session_id
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            logger.warning(f"尝试删除不存在的文件: {file_path}")
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 删除文件
        delete_file(data_id, session_id)
        logger.info(f"数据文件删除成功: {data_id}")
        
        return JSONResponse(content={
            "success": True,
            "message": "数据文件删除成功"
        })
    except Exception as e:
        logger.error(f"删除数据文件时出错: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@router.get("/{data_id}/download")
async def download_data(request: Request, data_id: str):
    """
    下载数据文件接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 首先尝试使用原始data_id查找文件
        file_path = get_file_path(data_id, session_id)
        logger.info(f"尝试使用原始data_id查找文件: {file_path}")
        
        # 如果文件不存在，尝试使用清理后的data_id
        if not os.path.exists(file_path):
            # 解码URL编码的data_id
            decoded_data_id = urllib.parse.unquote(data_id)
            logger.info(f"原始文件未找到，尝试解码后的data_id: {decoded_data_id}")
            
            # 再次尝试使用解码后的data_id
            file_path = get_file_path(decoded_data_id, session_id)
            if not os.path.exists(file_path):
                # 如果仍然不存在，尝试清理后的文件名
                sanitized_data_id = sanitize_filename(decoded_data_id)
                logger.info(f"解码后的文件未找到，尝试清理后的data_id: {sanitized_data_id}")
                file_path = get_file_path(sanitized_data_id, session_id)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": f"数据文件不存在: {file_path}"
                }
            )
        
        # 从文件路径中提取实际的data_id（文件名不带扩展名）
        actual_data_id = os.path.splitext(os.path.basename(file_path))[0]
        logger.info(f"找到文件，实际data_id为: {actual_data_id}")
        
        # 返回文件下载响应
        return FileResponse(
            path=file_path,
            filename=f"{actual_data_id}.csv",
            media_type='text/csv'
        )
    except Exception as e:
        logger.error(f"下载数据文件时出错: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@router.get("/{data_id}/details")
async def get_data_details(request: Request, data_id: str):
    """
    获取数据文件详细信息接口（包括前5行、每列类型、数据范围、缺失值等统计信息）
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建文件路径
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 读取CSV文件
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        # 处理NaN值，将其替换为None以便JSON序列化
        df = df.replace({pd.NA: None, pd.NaT: None, np.nan: None})
        
        # 获取前5行数据
        head_data = df.head(5).to_dict('records')
        
        # 获取每列的数据类型
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # 获取数值列的统计信息
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        numeric_stats = {}
        for col in numeric_columns:
            min_val = df[col].min()
            max_val = df[col].max()
            mean_val = df[col].mean()
            std_val = df[col].std()
            
            # 处理可能的NaN值和无穷大值
            def safe_float_convert(val):
                if pd.isna(val) or val is None:
                    return None
                try:
                    # 检查是否为无穷大
                    if np.isinf(val):
                        return None
                    return float(val)
                except (ValueError, OverflowError):
                    return None
            
            numeric_stats[col] = {
                "min": safe_float_convert(min_val),
                "max": safe_float_convert(max_val),
                "mean": safe_float_convert(mean_val),
                "std": safe_float_convert(std_val),
            }
        
        # 获取分类列的统计信息
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        categorical_stats = {}
        for col in categorical_columns:
            value_counts = df[col].value_counts()
            # 处理可能的NaN值
            value_counts = value_counts.replace({pd.NA: None, pd.NaT: None, np.nan: None})
            top_values = value_counts.head(5).to_dict()
            
            # 确保所有值都可以被JSON序列化
            safe_top_values = {}
            for k, v in top_values.items():
                if pd.isna(k):
                    safe_key = None
                else:
                    safe_key = str(k) if not isinstance(k, (str, int, float, bool)) else k
                
                safe_top_values[safe_key] = v
            
            categorical_stats[col] = {
                "unique_count": int(df[col].nunique()),
                "top_values": safe_top_values,
            }
        
        # 缺失值统计
        missing_values = {col: int(df[col].isnull().sum()) for col in df.columns}
        
        # 总体统计
        total_missing = int(df.isnull().sum().sum())
        total_cells = int(df.size)
        
        # 再次处理可能遗漏的NaN值
        df = df.replace({pd.NA: None, pd.NaT: None, np.nan: None})
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "data_id": data_id,
                "filename": f"{data_id}.csv",
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "head": head_data,
                "dtypes": dtypes,
                "numeric_stats": numeric_stats,
                "categorical_stats": categorical_stats,
                "missing_values": missing_values,
                "total_missing": total_missing,
                "total_cells": total_cells,
                "completeness": (total_cells - total_missing) / total_cells if total_cells > 0 else 0
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


class AddHeaderRequest(BaseModel):
    column_names: list
    mode: str = "add"  # "add" for adding header, "modify" for modifying existing header


@router.post("/{data_id}/add_header")
async def add_header(request: Request, data_id: str, body: AddHeaderRequest):
    """
    为文件添加标题行
    
    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (AddHeaderRequest): 请求体，包含列名列表和模式
        
    Returns:
        JSONResponse: 新文件的信息
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建文件路径
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 导入并调用添加标题行的函数
        try:
            from utils.file_manager import add_header_to_file
        except ImportError:
            # 最后尝试直接添加到路径并导入
            sys.path.insert(0, os.path.join(parent_dir, "utils"))
            from utils.file_manager import add_header_to_file
                
        result = add_header_to_file(file_path, body.column_names, session_id, mode=body.mode)
        
        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"添加标题行时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )
