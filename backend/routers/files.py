from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
import os
import pandas as pd
import numpy as np
import logging
from pydantic import BaseModel
from typing import Any, List, Dict, Optional, Union
from backend.routers.data import load_csv_file

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from utils.file_manager import get_file_path, delete_file, delete_columns

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/files")
async def get_user_files(request: Request):
    """
    获取用户上传的文件列表
    """
    # 获取session_id
    session_id = request.state.session_id
    try:
        # 构建用户目录路径
        user_dir = os.path.join("data", session_id)
        
        # 检查目录是否存在
        if not os.path.exists(user_dir):
            return JSONResponse(content={
                "success": True,
                "data": [],
                "session_id": session_id
            })
        
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
                        
                        # 确保所有值都可以被JSON序列化
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
        
        return JSONResponse(content={
            "success": True,
            "data": files,
            "session_id": session_id
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
        )

class DeleteColumnsRequest(BaseModel):
    columns_to_delete: List[str]

@router.post("/{data_id}/delete_columns")
async def delete_columns_endpoint(request: Request, data_id: str, body: DeleteColumnsRequest):
    """
    删除指定列接口

    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (DeleteColumnsRequest): 请求体，包含要删除的列名列表

    Returns:
        JSONResponse: 处理结果，只包含data_id和保存路径
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

        # 调用删除列的函数
        result = delete_columns(file_path, body.columns_to_delete, session_id)

        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"删除列时出错: {str(e)}")
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

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )

        # 导入并调用添加标题行的函数
        from utils.file_manager import add_header_to_file

        result = add_header_to_file(get_file_path(data_id, session_id), body.column_names, session_id, mode=body.mode)

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


class RemoveInvalidSamplesRequest(BaseModel):
    remove_duplicates: bool = False
    remove_duplicate_cols: bool = False
    remove_constant_cols: bool = False
    row_missing_threshold: float = 1.0
    col_missing_threshold: float = 1.0


@router.post("/{data_id}/remove_invalid_samples")
async def remove_invalid_samples(request: Request, data_id: str, body: RemoveInvalidSamplesRequest):
    """
    去除无效样本接口

    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (RemoveInvalidSamplesRequest): 请求体，包含处理参数

    Returns:
        JSONResponse: 处理结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )
        # 导入并调用去除无效样本的函数
        from utils.file_manager import remove_invalid_samples

        result = remove_invalid_samples(get_file_path(data_id, session_id), session_id,
                                        body.remove_duplicates, body.remove_duplicate_cols, body.remove_constant_cols,
                                        body.row_missing_threshold, body.col_missing_threshold)

        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"去除无效样本时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


class HandleMissingValuesRequest(BaseModel):
    specified_columns: List[str] = None
    interpolation_method: str = "linear"
    fill_value: Any = None
    knn_neighbors: int = 5


@router.post("/{data_id}/handle_missing_values")
async def handle_missing_values_endpoint(request: Request, data_id: str, body: HandleMissingValuesRequest):
    """
    处理缺失值接口

    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (HandleMissingValuesRequest): 请求体，包含处理参数

    Returns:
        JSONResponse: 处理结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )
        # 导入并调用处理缺失值的函数
        from utils.file_manager import handle_missing_values

        result = handle_missing_values(get_file_path(data_id, session_id), session_id, body.specified_columns,
                                       body.interpolation_method, body.fill_value,
                                       body.knn_neighbors)

        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"处理缺失值时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


# 数据转换相关模型和端点
class DimensionlessProcessingRequest(BaseModel):
    columns: List[str]
    method: str = "standard"
    params: Optional[Dict[str, Any]] = None


@router.post("/{data_id}/dimensionless_processing")
async def dimensionless_processing_endpoint(request: Request, data_id: str, body: DimensionlessProcessingRequest):
    """
    量纲处理接口

    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (DimensionlessProcessingRequest): 请求体，包含处理参数

    Returns:
        JSONResponse: 处理结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )
            
        # 导入并调用量纲处理函数
        from utils.pandas_tool import dimensionless_processing

        # 准备额外参数
        kwargs = {}
        if body.params:
            kwargs.update(body.params)
            
        result = dimensionless_processing(
            get_file_path(data_id, session_id), 
            body.columns, 
            body.method, 
            session_id,
            **kwargs
        )

        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"量纲处理时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


class ScientificCalculationRequest(BaseModel):
    columns: List[str]
    operation: str
    params: Optional[Dict[str, Any]] = None


@router.post("/{data_id}/scientific_calculation")
async def scientific_calculation_endpoint(request: Request, data_id: str, body: ScientificCalculationRequest):
    """
    科学计算接口

    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (ScientificCalculationRequest): 请求体，包含处理参数

    Returns:
        JSONResponse: 处理结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )
            
        # 导入并调用科学计算函数
        from utils.pandas_tool import scientific_calculation

        result = scientific_calculation(
            get_file_path(data_id, session_id), 
            body.columns, 
            body.operation, 
            body.params, 
            session_id
        )

        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"科学计算时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


class OneHotEncodingRequest(BaseModel):
    columns: List[str]
    drop_first: bool = False


@router.post("/{data_id}/one_hot_encoding")
async def one_hot_encoding_endpoint(request: Request, data_id: str, body: OneHotEncodingRequest):
    """
    独热编码接口

    Args:
        request (Request): FastAPI请求对象
        data_id (str): 数据文件ID
        body (OneHotEncodingRequest): 请求体，包含处理参数

    Returns:
        JSONResponse: 处理结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )
            
        # 导入并调用独热编码函数
        from utils.pandas_tool import one_hot_encoding

        result = one_hot_encoding(
            get_file_path(data_id, session_id), 
            body.columns, 
            session_id,
            body.drop_first
        )

        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"独热编码时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )