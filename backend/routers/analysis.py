import sys
import os
import traceback

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
from utils.ml_tool import clustering_analysis,logistic_regression, xgboost_analysis, svm_analysis, \
    decision_tree_analysis, neural_network_analysis, neural_network_classification, neural_network_regression
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


class ClusteringRequest(BaseModel):
    columns: Optional[List[str]] = None
    method: str = "kmeans"
    n_clusters: int = 3
    params: Optional[Dict[str, Any]] = None  # 其他参数


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

        correlation_result = correlation_analysis(file_path, columns_to_process, body.method, session_id)

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

        kwargs = body.params if body.params else {}

        t_test_result = t_test(file_path, columns_to_process, body.test_type, session_id, **kwargs)

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

        f_test_result = f_test(file_path, columns_to_process, session_id, body.group_by, body.alpha)

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
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        chi_square_result = chi_square_test(file_path, columns_to_process, session_id, body.alpha, body.group_by)

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
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}

        non_parametric_result = non_parametric_test(
            file_path, columns_to_process, body.test_type, session_id, body.group_by, body.alpha, **kwargs)

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
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}

        regression_result = linear_regression(
            file_path, columns_to_process, body.y_column, body.method, session_id, body.alpha, body.l1_ratio, **kwargs)

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
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}

        regression_result = logistic_regression(
            file_path, columns_to_process, body.y_column, body.method, session_id, 
            body.solver, **kwargs)

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


@router.post("/{data_id}/clustering_analysis")
async def get_clustering_analysis(request: Request, data_id: str, body: ClusteringRequest):
    """
    获取数据文件的聚类分析结果接口，用于"聚类分析"方法
    """
    try:
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}
        
        clustering_result = clustering_analysis(
            file_path, columns_to_process, body.method, body.n_clusters, session_id, **kwargs)

        result_data = {
            "data_id": data_id,
            "method": clustering_result["method"],
            "columns": clustering_result["columns"],
            "n_clusters": clustering_result["n_clusters"],
            "cluster_labels": clustering_result["cluster_labels"],
            "original_indices": clustering_result["original_indices"],
            "cluster_stats": clustering_result["cluster_stats"],
            "evaluation_metrics": clustering_result["evaluation_metrics"],
            "sample_size": clustering_result["sample_size"],
            "result_file_path": clustering_result["result_file_path"],  # 添加结果文件路径
            "model_params": clustering_result["model_params"]
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取聚类分析结果时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


class XGBoostRequest(BaseModel):
    x_columns: List[str]  # 自变量列
    y_column: str         # 因变量列
    task_type: str = "auto"  # 任务类型
    objective: Optional[str] = None  # 目标函数
    n_estimators: int = 100  # 树的数量
    max_depth: int = 6       # 树的最大深度
    learning_rate: float = 0.3  # 学习率
    subsample: float = 1.0      # 子样本比例
    colsample_bytree: float = 1.0  # 每棵树使用的特征比例
    random_state: int = 42        # 随机种子
    params: Optional[Dict[str, Any]] = None  # 其他参数


class SVMRequest(BaseModel):
    x_columns: List[str]  # 自变量列
    y_column: str         # 因变量列
    task_type: str = "classification"  # 任务类型
    kernel: str = "rbf"  # 核函数类型
    C: float = 1.0  # 正则化参数
    gamma: str = "scale"  # 核函数系数
    degree: int = 3  # 多项式核的度数
    coef0: float = 0.0  # 核函数中的独立项
    shrinking: bool = True  # 是否使用启发式收缩
    probability: bool = True  # 是否启用概率预测
    tol: float = 1e-3  # 停止准则的容忍度
    max_iter: int = -1  # 最大迭代次数
    params: Optional[Dict[str, Any]] = None  # 其他参数


@router.post("/{data_id}/xgboost_analysis")
async def get_xgboost_analysis(request: Request, data_id: str, body: XGBoostRequest):
    """
    获取数据文件的XGBoost分析结果接口，用于"XGBoost"方法
    """
    try:
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}
        if body.objective:
            kwargs['objective'] = body.objective
        
        kwargs.update({
            'n_estimators': body.n_estimators,
            'max_depth': body.max_depth,
            'learning_rate': body.learning_rate,
            'subsample': body.subsample,
            'colsample_bytree': body.colsample_bytree,
            'random_state': body.random_state
        })

        xgboost_result = xgboost_analysis(
            file_path, columns_to_process, body.y_column, body.task_type, session_id, **kwargs)

        result_data = {
            "data_id": data_id,
            "method": xgboost_result["method"],
            "x_columns": xgboost_result["x_columns"],
            "y_column": xgboost_result["y_column"],
            "objective": xgboost_result.get("objective"),
            "feature_importance": xgboost_result["feature_importance"],
            "evaluation_metrics": xgboost_result["evaluation_metrics"],
            "sample_size": xgboost_result["sample_size"],
            "train_size": xgboost_result.get("train_size"),
            "test_size": xgboost_result.get("test_size"),
            "model_params": xgboost_result["model_params"]
        }

        # 如果是分类任务，添加分类相关信息
        if "n_classes" in xgboost_result:
            result_data["n_classes"] = xgboost_result["n_classes"]
            result_data["class_labels"] = xgboost_result["class_labels"]
            result_data["confusion_matrix"] = xgboost_result.get("confusion_matrix")

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取XGBoost分析结果时出错: {str(e)},{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/svm_analysis")
async def get_svm_analysis(request: Request, data_id: str, body: SVMRequest):
    """
    获取数据文件的支持向量机(SVM)分析结果接口，用于"SVM"方法
    """
    try:
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}
        
        kwargs.update({
            'kernel': body.kernel,
            'C': body.C,
            'gamma': body.gamma,
            'degree': body.degree,
            'coef0': body.coef0,
            'shrinking': body.shrinking,
            'probability': body.probability,
            'tol': body.tol,
            'max_iter': body.max_iter
        })

        svm_result = svm_analysis(
            file_path, columns_to_process, body.y_column, body.task_type, session_id, **kwargs)

        result_data = {
            "data_id": data_id,
            "method": svm_result["method"],
            "task_type": svm_result["task_type"],
            "x_columns": svm_result["x_columns"],
            "y_column": svm_result["y_column"],
            "evaluation_metrics": svm_result["evaluation_metrics"],
            "sample_size": svm_result["sample_size"],
            "model_params": svm_result["model_params"]
        }

        # 根据任务类型添加特定信息
        if svm_result.get("task_type", "").endswith("classification"):
            result_data["n_classes"] = svm_result["n_classes"]
            result_data["class_labels"] = svm_result["class_labels"]
            result_data["support_vectors_count"] = svm_result["support_vectors_count"]
            result_data["n_support_vectors_per_class"] = svm_result["n_support_vectors_per_class"]
            result_data["predicted_labels"] = svm_result["predicted_labels"]  # 添加预测标签
        else:
            result_data["support_vectors_count"] = svm_result["support_vectors_count"]
            result_data["predicted_values"] = svm_result["predicted_values"]  # 添加预测值

        # 添加结果文件路径
        if "result_file_path" in svm_result:
            result_data["result_file_path"] = svm_result["result_file_path"]

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取SVM分析结果时出错: {str(e)},{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


class DecisionTreeRequest(BaseModel):
    x_columns: List[str]  # 自变量列
    y_column: str         # 因变量列
    task_type: str = "auto"  # 任务类型
    criterion: Optional[str] = None  # 分割标准
    max_depth: Optional[int] = None  # 树的最大深度
    min_samples_split: int = 2       # 内部节点分裂所需的最小样本数
    min_samples_leaf: int = 1        # 叶节点所需的最小样本数
    max_features: Optional[str] = None  # 寻找最佳分割时考虑的特征数量
    random_state: int = 42           # 随机种子
    params: Optional[Dict[str, Any]] = None  # 其他参数


class NeuralNetworkRequest(BaseModel):
    x_columns: List[str]  # 自变量列
    y_column: str         # 因变量列
    task_type: str = "auto"  # 任务类型
    hidden_layer_sizes: Tuple[int, ...] = (100,)  # 隐藏层节点数元组
    activation: str = "relu"  # 激活函数
    solver: str = "adam"  # 求解器
    alpha: float = 0.0001  # L2正则化参数
    batch_size: str = "auto"  # 批大小
    learning_rate: str = "constant"  # 学习率调整策略
    learning_rate_init: float = 0.001  # 初始学习率
    max_iter: int = 200  # 最大迭代次数
    shuffle: bool = True  # 是否在每次迭代前打乱样本
    random_state: int = 42  # 随机种子
    tol: float = 1e-4  # 停止容差
    verbose: bool = False  # 是否输出训练过程信息
    warm_start: bool = False  # 是否使用上次训练结果继续训练
    momentum: float = 0.9  # 动量参数
    nesterovs_momentum: bool = True  # 是否使用Nesterov动量
    early_stopping: bool = False  # 是否启用早停
    validation_fraction: float = 0.1  # 验证集比例
    beta_1: float = 0.9  # Adam优化器参数
    beta_2: float = 0.999  # Adam优化器参数
    epsilon: float = 1e-8  # 数值稳定性参数
    n_iter_no_change: int = 10  # 早停判断的不改善迭代次数
    params: Optional[Dict[str, Any]] = None  # 其他参数


@router.post("/{data_id}/decision_tree_analysis")
async def get_decision_tree_analysis(request: Request, data_id: str, body: DecisionTreeRequest):
    """
    获取数据文件的决策树分析结果接口，用于"决策树"方法
    """
    try:
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}
        
        kwargs.update({
            'criterion': body.criterion,
            'max_depth': body.max_depth,
            'min_samples_split': body.min_samples_split,
            'min_samples_leaf': body.min_samples_leaf,
            'max_features': body.max_features,
            'random_state': body.random_state
        })

        dt_result = decision_tree_analysis(
            file_path, columns_to_process, body.y_column, body.task_type, session_id, **kwargs)

        result_data = {
            "data_id": data_id,
            "method": dt_result["method"],
            "x_columns": dt_result["x_columns"],
            "y_column": dt_result["y_column"],
            "criterion": dt_result.get("criterion"),
            "feature_importance": dt_result["feature_importance"],
            "evaluation_metrics": dt_result["evaluation_metrics"],
            "sample_size": dt_result["sample_size"],
            "train_size": dt_result.get("train_size"),
            "test_size": dt_result.get("test_size"),
            "model_params": dt_result["model_params"]
        }

        # 如果是分类任务，添加分类相关信息
        if "n_classes" in dt_result:
            result_data["n_classes"] = dt_result["n_classes"]
            result_data["class_labels"] = dt_result["class_labels"]
            result_data["confusion_matrix"] = dt_result.get("confusion_matrix")

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取决策树分析结果时出错: {str(e)},{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )


@router.post("/{data_id}/neural_network_analysis")
async def get_neural_network_analysis(request: Request, data_id: str, body: NeuralNetworkRequest):
    """
    获取数据文件的神经网络分析结果接口，用于"神经网络"方法
    """
    try:
        session_id, file_path, df, columns_to_process, error_response = validate_request_data(
            request, data_id, body.x_columns)
        if error_response:
            return error_response

        kwargs = body.params if body.params else {}
        
        kwargs.update({
            'hidden_layer_sizes': body.hidden_layer_sizes,
            'activation': body.activation,
            'solver': body.solver,
            'alpha': body.alpha,
            'batch_size': body.batch_size,
            'learning_rate': body.learning_rate,
            'learning_rate_init': body.learning_rate_init,
            'max_iter': body.max_iter,
            'shuffle': body.shuffle,
            'random_state': body.random_state,
            'tol': body.tol,
            'verbose': body.verbose,
            'warm_start': body.warm_start,
            'momentum': body.momentum,
            'nesterovs_momentum': body.nesterovs_momentum,
            'early_stopping': body.early_stopping,
            'validation_fraction': body.validation_fraction,
            'beta_1': body.beta_1,
            'beta_2': body.beta_2,
            'epsilon': body.epsilon,
            'n_iter_no_change': body.n_iter_no_change
        })

        nn_result = neural_network_analysis(
            file_path, columns_to_process, body.y_column, body.task_type, session_id, **kwargs)

        result_data = {
            "data_id": data_id,
            "method": nn_result["method"],
            "x_columns": nn_result["x_columns"],
            "y_column": nn_result["y_column"],
            "evaluation_metrics": nn_result["evaluation_metrics"],
            "sample_size": nn_result["sample_size"],
            "train_size": nn_result.get("train_size"),
            "test_size": nn_result.get("test_size"),
            "model_params": nn_result["model_params"],
            "model_info": nn_result["model_info"]
        }

        # 根据任务类型添加特定信息
        if nn_result.get("method", "").endswith("classification"):
            result_data["n_classes"] = nn_result["n_classes"]
            result_data["class_labels"] = nn_result["class_labels"]
            result_data["confusion_matrix"] = nn_result.get("confusion_matrix")

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"获取神经网络分析结果时出错: {str(e)},{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"{str(e)}"
            }
        )

