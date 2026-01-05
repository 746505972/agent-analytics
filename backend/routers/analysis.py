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
from typing import List, Optional, Tuple, Dict, Any

from routers.data import load_csv_file
from utils.pandas_tool import statistical_summary, correlation_analysis, \
    normality_test, t_test, f_test, chi_square_test, non_parametric_test,linear_regression
from utils.file_manager import get_file_path
import pandas as pd

router = APIRouter(prefix="/data", tags=["analysis"])

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StatisticalSummaryRequest(BaseModel):
    columns: Optional[List[str]] = None


class CorrelationAnalysisRequest(BaseModel):
    columns: Optional[List[str]] = None
    method: str = "pearson"


class NormalityTestRequest(BaseModel):
    columns: Optional[List[str]] = None
    method: str = "shapiro"
    alpha: float = 0.05
    group_by: Optional[str] = None


class TTestRequest(BaseModel):
    columns: Optional[List[str]] = None
    test_type: str = "one_sample"
    params: Optional[Dict[str, Any]] = None


class FTestRequest(BaseModel):
    columns: Optional[List[str]] = None
    group_by: Optional[str] = None
    alpha: float = 0.05


class ChiSquareTestRequest(BaseModel):
    columns: Optional[List[str]] = None
    group_by: Optional[str] = None
    alpha: float = 0.05


class NonParametricTestRequest(BaseModel):
    columns: Optional[List[str]] = None
    test_type: str = "mannwhitney"
    group_by: Optional[str] = None
    alpha: float = 0.05
    params: Optional[Dict[str, Any]] = None


def validate_request_data(request: Request, data_id: str, body_columns: Optional[List[str]] = None) -> Tuple[str, str, pd.DataFrame, List[str], JSONResponse]:
    """
    验证请求数据并准备处理参数
    
    Args:
        request: FastAPI请求对象
        data_id: 数据ID
        body_columns: 请求体中的列列表
        
    Returns:
        Tuple[session_id, file_path, df, columns_to_process, error_response]
    """
    # 获取session_id
    session_id = request.state.session_id

    # 获取文件路径
    file_path = get_file_path(data_id, session_id)
    
    if not os.path.exists(file_path):
        return "", "", None, [], JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": f"文件不存在: {file_path}"
            }
        )

    # 加载CSV文件
    success, result, status_code = load_csv_file(data_id, session_id)
    if not success:
        return "", "", None, [], JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": result
            }
        )

    df = result

    # 检查DataFrame是否为空
    if df.empty:
        return "", "", None, [], JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "数据文件为空"
            }
        )

    # 确定要处理的列
    if body_columns:
        # 使用请求中指定的列
        columns_to_process = [col for col in body_columns if col in df.columns]
        missing_columns = set(body_columns) - set(columns_to_process)
        if missing_columns:
            logger.warning(f"以下列在数据中不存在: {missing_columns}")
    else:
        # 默认处理所有数值型列
        columns_to_process = df.select_dtypes(include=['number']).columns.tolist()
    
    if not columns_to_process:
        return "", "", None, [], JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "没有可处理的列"
            }
        )

    return session_id, file_path, df, columns_to_process, None


@router.post("/{data_id}/statistical_summary")
async def get_statistical_summary(request: Request, data_id: str, body: StatisticalSummaryRequest):
    """
    获取数据文件的统计摘要信息接口，用于"统计摘要"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

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
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        # 调用工具函数处理相关性分析
        correlation_result = correlation_analysis(file_path, columns_to_process, body.method, session_id)
        
        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "method": body.method,
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
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/normality_test")
async def get_normality_test(request: Request, data_id: str, body: NormalityTestRequest):
    """
    获取数据文件的正态性检验结果接口，用于"正态性检验"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        # 调用工具函数处理正态性检验
        normality_result = normality_test(file_path, columns_to_process, session_id, body.method, body.alpha, body.group_by)
        
        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": columns_to_process,
            "alpha": body.alpha,
            "method": body.method,
        }
        
        # 根据是否分组返回不同的结果格式
        if "grouped_results" in normality_result:
            result_data["grouped_results"] = normality_result["grouped_results"]
            result_data["group_by"] = normality_result["group_by"]
        else:
            result_data["normality_results"] = normality_result["normality_results"]
            result_data["constant_columns"] = normality_result.get("constant_columns", [])

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取正态性检验结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/t_test")
async def get_t_test(request: Request, data_id: str, body: TTestRequest):
    """
    获取数据文件的T检验结果接口，用于"T检验"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        # 准备参数
        kwargs = body.params if body.params else {}

        # 调用工具函数处理T检验
        t_test_result = t_test(file_path, columns_to_process, body.test_type, session_id, **kwargs)

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": t_test_result["columns"],
            "test_type": t_test_result["test_type"],
            "normality_test": t_test_result["normality_test"],
            "t_test": t_test_result["t_test"]
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取T检验结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/f_test")
async def get_f_test(request: Request, data_id: str, body: FTestRequest):
    """
    获取数据文件的F检验结果接口，用于"F检验"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        # 调用工具函数处理F检验
        f_test_result = f_test(file_path, columns_to_process, session_id, body.group_by, body.alpha)

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": f_test_result["columns"],
            "f_test": f_test_result["f_test"],
            "alpha": f_test_result["alpha"]
        }

        # 如果有分组信息，也返回
        if "group_by" in f_test_result:
            result_data["group_by"] = f_test_result["group_by"]

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取F检验结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/chi_square_test")
async def get_chi_square_test(request: Request, data_id: str, body: ChiSquareTestRequest):
    """
    获取数据文件的卡方检验结果接口，用于"卡方检验"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        # 调用工具函数处理卡方检验
        chi_square_result = chi_square_test(file_path, columns_to_process, session_id, body.alpha, body.group_by)

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": chi_square_result["columns"],
            "chi_square_test": chi_square_result["chi_square_test"],
            "alpha": chi_square_result["alpha"]
        }

        # 如果有分组信息，也返回
        if "group_by" in chi_square_result:
            result_data["group_by"] = chi_square_result["group_by"]

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取卡方检验结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/non_parametric_test")
async def get_non_parametric_test(request: Request, data_id: str, body: NonParametricTestRequest):
    """
    获取数据文件的非参数检验结果接口，用于"非参数检验"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        # 准备参数
        kwargs = body.params if body.params else {}

        # 调用工具函数处理非参数检验
        non_parametric_result = non_parametric_test(
            file_path, columns_to_process, body.test_type, session_id, body.group_by, body.alpha, **kwargs)

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "columns": non_parametric_result["columns"],
            "test_type": non_parametric_result["test_type"],
            "non_parametric_test": non_parametric_result["non_parametric_test"],
            "alpha": non_parametric_result["alpha"]
        }

        # 如果有分组信息，也返回
        if "group_by" in non_parametric_result:
            result_data["group_by"] = non_parametric_result["group_by"]

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取非参数检验结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


class LinearRegressionRequest(BaseModel):
    x_columns: List[str]  # 自变量列
    y_column: str         # 因变量列
    method: str = "ols"   # 回归方法
    alpha: float = 1.0    # 正则化强度
    l1_ratio: float = 0.5 # ElasticNet中L1正则化的比例
    params: Optional[Dict[str, Any]] = None  # 其他参数


@router.post("/{data_id}/linear_regression")
async def get_linear_regression(request: Request, data_id: str, body: LinearRegressionRequest):
    """
    获取数据文件的线性回归分析结果接口，用于"线性回归"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        # 准备参数
        kwargs = body.params if body.params else {}

        # 调用工具函数处理线性回归
        regression_result = linear_regression(
            file_path, columns_to_process, body.y_column, body.method, session_id, body.alpha, body.l1_ratio, **kwargs)

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "method": regression_result["method"],
            "x_columns": regression_result["x_columns"],
            "y_column": regression_result["y_column"],
            "coefficients": regression_result["coefficients"],
            "intercept": regression_result["intercept"],
            "evaluation_metrics": regression_result["evaluation_metrics"],
            "sample_size": regression_result["sample_size"],
            "alpha": regression_result["alpha"],
            "l1_ratio": regression_result["l1_ratio"]
        }

        # 如果有正则化参数，也返回
        if "regularization_params" in regression_result:
            result_data["regularization_params"] = regression_result["regularization_params"]

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取线性回归结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


class LogisticRegressionRequest(BaseModel):
    x_columns: List[str]  # 自变量列
    y_column: str         # 因变量列
    method: str = "logistic"   # 回归方法
    solver: str = "lbfgs" # 优化算法
    params: Optional[Dict[str, Any]] = None  # 其他参数


@router.post("/{data_id}/logistic_regression")
async def get_logistic_regression(request: Request, data_id: str, body: LogisticRegressionRequest):
    """
    获取数据文件的逻辑回归分析结果接口，用于"逻辑回归"方法
    """
    try:
        # 验证请求数据
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        # 准备参数
        kwargs = body.params if body.params else {}

        # 调用工具函数处理逻辑回归
        from utils.ml_tool import logistic_regression
        regression_result = logistic_regression(
            file_path, columns_to_process, body.y_column, body.method, session_id, 
            body.solver, **kwargs)

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "method": regression_result["method"],
            "x_columns": regression_result["x_columns"],
            "y_column": regression_result["y_column"],
            "coefficients": regression_result["coefficients"],
            "intercept": regression_result["intercept"],
            "evaluation_metrics": regression_result["evaluation_metrics"],
            "sample_size": regression_result["sample_size"],
            "n_classes": regression_result["n_classes"],
            "class_labels": regression_result["class_labels"],
            "confusion_matrix": regression_result["confusion_matrix"],
            "model_params": regression_result["model_params"],
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取逻辑回归结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )
