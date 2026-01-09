from typing import List, Dict, Any

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

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


def logistic_regression(file_path: str, x_columns: List[str], y_column: str,
                        method: str = "logistic", session_id: str = None,
                        solver: str = 'lbfgs',**kwargs) -> Dict[str, Any]:
    """
    逻辑回归 - 使用逻辑回归进行分类任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列，分类标签）
        method (str): 回归方法 (默认 "logistic")
        session_id (str): 会话ID

        solver (str): 优化算法
            - "lbfgs": 拟牛顿法 (默认，适用于小数据集)
            - "liblinear": 坐标下降法 (适用于小数据集)
            - "newton-cg": 牛顿共轭梯度法 (适用于大数据集)
            - "sag": 随机平均梯度下降 (适用于大数据集)
            - "saga": 随机平均梯度下降加速版 (适用于大数据集)
        **kwargs: 其他参数，用于特定回归方法的配置
            - C (float): 正则化强度的倒数，值越小正则化越强 (默认1.0)
            - max_iter (int): 最大迭代次数 (默认1000)
            - tol: 收敛容差 (默认1e-4)
            - fit_intercept: 是否拟合截距 (默认True)
            - class_weight: 类别权重 ("balanced" 或 None)

    Returns:
        Dict[str, Any]: 包含逻辑回归结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_x_columns = check_and_read(file_path, x_columns, session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 准备数据
    X = df[numeric_x_columns].dropna()
    y_df = df[y_column].loc[X.index]  # 只保留X中对应行的y值

    # 对y列进行标签编码（转换分类标签为数值）
    label_encoder = LabelEncoder()
    y_raw = y_df.dropna()
    y = label_encoder.fit_transform(y_raw)
    
    # 同时过滤X以匹配y的索引
    valid_indices = y_raw.index
    X = X.loc[valid_indices]

    # 确保X和y的行数一致
    if len(X) != len(y):
        raise ValueError("X和y的数据行数不一致")

    if len(X) == 0:
        raise ValueError("没有有效的数据可用于逻辑回归分析")

    # 检查y是否为二分类或多分类
    unique_labels = np.unique(y)
    n_classes = len(unique_labels)
    if n_classes < 2:
        raise ValueError("目标列必须至少包含2个不同的类别")
    
    # 获取参数
    C = kwargs.get("C", 1.0)
    max_iter = kwargs.get("max_iter", 1000)
    tol = kwargs.get("tol", 1e-4)
    fit_intercept = kwargs.get("fit_intercept", True)
    class_weight = kwargs.get("class_weight", None)

    # 多分类设置
    if n_classes > 2:
        # 对于多分类问题，确保solver支持
        if solver not in ['newton-cg', 'sag', 'saga', 'lbfgs']:
            solver = 'lbfgs'  # 默认使用支持多分类的算法

    # 创建逻辑回归模型
    model = LogisticRegression(
        C=C,
        max_iter=max_iter,
        solver=solver,
        tol=tol,
        fit_intercept=fit_intercept,
        class_weight=class_weight,
        random_state=42  # 为了结果可重现
    )

    # 拟合模型
    try:
        model.fit(X, y)
    except Exception as e:
        raise ValueError(f"模型拟合失败: {e}")

    # 预测
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)

    # 计算评估指标
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    from sklearn.preprocessing import label_binarize

    accuracy = accuracy_score(y, y_pred)
    
    # 对于多分类问题，计算宏平均和微平均
    if n_classes > 2:
        precision = precision_score(y, y_pred, average='macro', zero_division=0)
        recall = recall_score(y, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y, y_pred, average='macro', zero_division=0)
        
        # 对于微平均
        precision_micro = precision_score(y, y_pred, average='micro', zero_division=0)
        recall_micro = recall_score(y, y_pred, average='micro', zero_division=0)
        f1_micro = f1_score(y, y_pred, average='micro', zero_division=0)
    else:  # 二分类
        precision = precision_score(y, y_pred, zero_division=0)
        recall = recall_score(y, y_pred, zero_division=0)
        f1 = f1_score(y, y_pred, zero_division=0)
        precision_micro = recall_micro = f1_micro = None

    # 获取混淆矩阵
    cm = confusion_matrix(y, y_pred)

    # 获取模型系数
    coefficients = {}
    if len(model.coef_.shape) == 1:  # 二分类
        coefficients = dict(zip(numeric_x_columns, model.coef_))
        intercept = float(model.intercept_) if hasattr(model, 'intercept_') else None
    else:  # 多分类
        # 对于多分类，每个类别有一组系数
        for i, class_coef in enumerate(model.coef_):
            class_name = label_encoder.inverse_transform([i])[0]
            coefficients[f"class_{class_name}"] = dict(zip(numeric_x_columns, class_coef))
        intercept = [float(i) for i in model.intercept_] if hasattr(model, 'intercept_') else None

    # 准备返回结果
    result = {"method": method, "x_columns": numeric_x_columns, "y_column": y_column, "coefficients": coefficients,
              "intercept": intercept,
              "evaluation_metrics": {
                "accuracy": _safe_float(accuracy),
                "precision": _safe_float(precision),
                "recall": _safe_float(recall),
                "f1_score": _safe_float(f1),
                "precision_micro": _safe_float(precision_micro),
                "recall_micro": _safe_float(recall_micro),
                "f1_micro": _safe_float(f1_micro)
              },
              "sample_size": len(X), "n_classes": n_classes, "class_labels": label_encoder.classes_.tolist(),
              "confusion_matrix": cm.tolist(),
              "model_params": {
                "C": C,
                "max_iter": max_iter,
                "solver": solver,
                "tol": tol,
                "fit_intercept": fit_intercept,
                "class_weight": class_weight
        }}

    return result