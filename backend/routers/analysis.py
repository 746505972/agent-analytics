import sys
import os

# 添加项目根目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel
from typing import List, Optional

from routers.data import load_csv_file
from utils.pandas_tool import statistical_summary, correlation_analysis
from utils.file_manager import get_file_path

router = APIRouter(prefix="/data", tags=["analysis"])

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StatisticalSummaryRequest(BaseModel):
    columns: Optional[List[str]] = None


class CorrelationAnalysisRequest(BaseModel):
    columns: Optional[List[str]] = None
    method: str = "pearson"


@router.post("/{data_id}/statistical_summary")
async def get_statistical_summary(request: Request, data_id: str, body: StatisticalSummaryRequest):
    """
    获取数据文件的统计摘要信息接口，用于"统计摘要"方法
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 获取文件路径
        file_path = get_file_path(data_id, session_id)
        
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": f"文件不存在: {file_path}"
                }
            )

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

        df = result

        # 检查DataFrame是否为空
        if df.empty:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "数据文件为空"
                }
            )

        # 确定要处理的列
        if body.columns:
            # 使用请求中指定的列
            columns_to_process = [col for col in body.columns if col in df.columns]
            missing_columns = set(body.columns) - set(columns_to_process)
            if missing_columns:
                logger.warning(f"以下列在数据中不存在: {missing_columns}")
        else:
            # 默认处理所有数值型列
            columns_to_process = df.select_dtypes(include=['number']).columns.tolist()
        
        if not columns_to_process:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "没有可处理的列"
                }
            )

        # 调用工具函数处理统计摘要
        summary_result = statistical_summary(file_path, columns_to_process, session_id)
        
        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": summary_result["columns"],
            "summary": summary_result["summary"]
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取统计摘要信息时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.post("/{data_id}/correlation_analysis")
async def get_correlation_analysis(request: Request, data_id: str, body: CorrelationAnalysisRequest):
    """
    获取数据文件的相关性分析结果接口，用于"相关性分析"方法
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 获取文件路径
        file_path = get_file_path(data_id, session_id)
        
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": f"文件不存在: {file_path}"
                }
            )

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

        df = result

        # 检查DataFrame是否为空
        if df.empty:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "数据文件为空"
                }
            )

        # 确定要处理的列
        if body.columns:
            # 使用请求中指定的列
            columns_to_process = [col for col in body.columns if col in df.columns]
            missing_columns = set(body.columns) - set(columns_to_process)
            if missing_columns:
                logger.warning(f"以下列在数据中不存在: {missing_columns}")
        else:
            # 默认处理所有数值型列
            columns_to_process = df.select_dtypes(include=['number']).columns.tolist()
        
        if not columns_to_process:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "没有可处理的列"
                }
            )

        # 调用工具函数处理相关性分析
        correlation_result = correlation_analysis(file_path, columns_to_process, body.method, session_id)
        
        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": correlation_result["columns"],
            "correlation_data": correlation_result["correlation_data"],
            "correlation_matrix": correlation_result["correlation_matrix"]
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取相关性分析结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )