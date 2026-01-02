from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from .check_and_read import check_and_read

def _safe_float(value):
    """安全地将值转换为float，处理inf和nan值"""
    if value is None:
        return None
    try:
        f = float(value)
        if np.isinf(f) or np.isnan(f):
            return None
        return f
    except (ValueError, OverflowError):
        return None


def linear_regression(file_path: str, x_columns: List[str], y_column: str,
                      method: str = "ols", session_id: str = None,
                      alpha: float = 1.0, l1_ratio: float = 0.5, **kwargs) -> Dict[str, Any]:
    """
    线性回归 - 使用普通最小二乘法或带正则化的线性回归方法

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        method (str): 回归方法
            - "ols": 普通最小二乘法 (默认)
            - "lasso": L1正则化 (Lasso)
            - "ridge": L2正则化 (Ridge)
            - "elastic_net": 弹性网络 (ElasticNet)
        session_id (str): 会话ID
        alpha (float): 正则化强度 (默认1.0)
        l1_ratio (float): ElasticNet中L1正则化的比例 (0到1之间，仅用于elastic_net)
        **kwargs: 其他参数，用于特定回归方法的配置
            - max_iter: 最大迭代次数 (默认1000)
            - tol: 收敛容差 (默认1e-4)
            - fit_intercept: 是否拟合截距 (默认True)

    Returns:
        Dict[str, Any]: 包含线性回归结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_x_columns = check_and_read(file_path, x_columns, session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查目标列是否为数值型
    if not pd.api.types.is_numeric_dtype(df[y_column]):
        raise ValueError(f"目标列 '{y_column}' 必须是数值型")

    # 确保X列都是数值型
    if not numeric_x_columns:
        raise ValueError("所有自变量列都必须是数值型")

    # 准备数据
    X = df[numeric_x_columns].dropna()
    y = df[y_column].loc[X.index]  # 只保留X中对应行的y值

    # 确保X和y的行数一致
    if len(X) != len(y):
        raise ValueError("X和y的数据行数不一致")

    if len(X) == 0:
        raise ValueError("没有有效的数据可用于回归分析")

    # 获取参数
    max_iter = kwargs.get("max_iter", 1000)
    tol = kwargs.get("tol", 1e-4)
    fit_intercept = kwargs.get("fit_intercept", True)

    # 选择回归模型
    if method == "ols":
        model = LinearRegression(fit_intercept=fit_intercept)
    elif method == "lasso":
        model = Lasso(alpha=alpha, fit_intercept=fit_intercept,
                      max_iter=max_iter, tol=tol)
    elif method == "ridge":
        model = Ridge(alpha=alpha, fit_intercept=fit_intercept,
                      max_iter=max_iter, tol=tol, solver='auto')
    elif method == "elastic_net":
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio,
                           fit_intercept=fit_intercept, max_iter=max_iter,
                           tol=tol)
    else:
        raise ValueError(f"不支持的回归方法: {method}")

    # 拟合模型
    try:
        model.fit(X, y)
    except Exception as e:
        raise ValueError(f"模型拟合失败: {e}")

    # 预测
    y_pred = model.predict(X)

    # 计算评估指标
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)

    # 获取模型系数
    coefficients = dict(zip(numeric_x_columns, model.coef_))
    intercept = float(model.intercept_) if hasattr(model, 'intercept_') else None

    # 准备返回结果
    result = {
        "method": method,
        "x_columns": numeric_x_columns,
        "y_column": y_column,
        "coefficients": coefficients,
        "intercept": intercept,
        "evaluation_metrics": {
            "mse": _safe_float(mse),
            "rmse": _safe_float(rmse),
            "r2_score": _safe_float(r2),
            "mae": _safe_float(mae)
        },
        "sample_size": len(X),
        "alpha": alpha if method != "ols" else None,
        "l1_ratio": l1_ratio if method == "elastic_net" else None
    }

    # 如果是正则化方法，添加额外参数
    if method in ["lasso", "ridge", "elastic_net"]:
        result["regularization_params"] = {
            "alpha": alpha,
            "max_iter": max_iter,
            "tol": tol,
            "fit_intercept": fit_intercept
        }
        if method == "elastic_net":
            result["regularization_params"]["l1_ratio"] = l1_ratio

    return result
