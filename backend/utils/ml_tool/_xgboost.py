"""
XGBoost算法模块
提供XGBoost分类和回归功能
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score
)
from .check_and_read import check_and_read
import xgboost as xgb


def _safe_float(value):
    """安全地将值转换为float，处理inf和nan值"""
    if value is None:
        return None
    try:
        # 处理numpy数据类型
        if hasattr(value, 'dtype'):
            if np.isnan(value) or np.isinf(value):
                return None
            return float(value)
        f = float(value)
        if np.isinf(f) or np.isnan(f):
            return None
        return f
    except (ValueError, OverflowError):
        return None

def _safe_float_list(lst):
    """将列表中的numpy数据类型转换为Python原生类型，处理inf和nan值"""
    if lst is None:
        return None
    return [_safe_float(item) for item in lst]


def _convert_numpy_types(obj):
    """递归转换对象中的numpy数据类型为Python原生类型"""
    if isinstance(obj, np.ndarray):
        return [_safe_float(item) for item in obj.tolist()]
    elif isinstance(obj, np.floating):
        return _safe_float(float(obj))
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, list):
        return [_convert_numpy_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (tuple, set, frozenset)):
        return type(obj)(_convert_numpy_types(item) for item in obj)
    else:
        return obj


def xgboost_classification(file_path: str, x_columns: List[str], y_column: str,
                         session_id: str = None, objective: str = 'binary:logistic',
                         n_estimators: int = 100, max_depth: int = 6,
                         learning_rate: float = 0.3, subsample: float = 1.0,
                         colsample_bytree: float = 1.0, random_state: int = 42,
                         **kwargs) -> Dict[str, Any]:
    """
    XGBoost分类 - 使用XGBoost进行分类任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列，分类标签）
        session_id (str): 会话ID
        objective (str): 目标函数
            - "binary:logistic": 二分类（默认）
            - "multi:softmax": 多分类
            - "multi:softprob": 多分类概率输出
        n_estimators (int): 树的数量 (默认100)
        max_depth (int): 树的最大深度 (默认6)
        learning_rate (float): 学习率 (默认0.3)
        subsample (float): 子样本比例 (默认1.0)
        colsample_bytree (float): 每棵树使用的特征比例 (默认1.0)
        random_state (int): 随机种子 (默认42)
        **kwargs: 其他XGBoost参数

    Returns:
        Dict[str, Any]: 包含XGBoost分类结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, x_columns + [y_column], session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查是否有足够的特征列
    feature_columns = [col for col in x_columns if col in df.columns]
    if not feature_columns:
        raise ValueError("没有有效的特征列用于XGBoost分类")

    # 提取特征和目标变量
    X = df[feature_columns].select_dtypes(include=[np.number])
    y = df[y_column]

    # 检查是否有足够的数值型特征
    if X.shape[1] == 0:
        raise ValueError("没有有效的数值型特征列用于XGBoost分类")

    # 处理目标变量（分类标签）
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # 删除包含NaN的行
    # 将y_encoded转换为pandas Series以使用.isna()方法
    y_series = pd.Series(y_encoded)
    mask = ~(X.isna().any(axis=1) | y_series.isna())
    X_clean = X[mask]
    y_clean = y_encoded[mask]

    if len(X_clean) == 0:
        raise ValueError("没有有效的数据可用于XGBoost分类")

    # 确定分类类型
    n_classes = len(np.unique(y_clean))
    if n_classes < 2:
        raise ValueError("目标列至少需要2个不同的类别")

    # 设置目标函数
    if n_classes == 2 and objective == 'binary:logistic':
        objective = 'binary:logistic'
    elif n_classes > 2:
        objective = 'multi:softmax'
        kwargs['num_class'] = n_classes

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X_clean, y_clean, test_size=0.2, random_state=random_state, stratify=y_clean
    )

    # 创建XGBoost分类器
    clf = xgb.XGBClassifier(
        objective=objective,
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        **kwargs
    )

    # 训练模型
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)

    # 计算评估指标
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # 计算混淆矩阵
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)

    # 获取特征重要性
    feature_importance = {feature: _safe_float(importance) for feature, importance in zip(feature_columns, clf.feature_importances_)}

    # 准备返回结果
    result = {
        "method": "xgboost_classification",
        "x_columns": feature_columns,
        "y_column": y_column,
        "objective": objective,
        "n_classes": int(n_classes),
        "class_labels": label_encoder.classes_.tolist(),
        "feature_importance": feature_importance,
        "evaluation_metrics": {
            "accuracy": _safe_float(accuracy),
            "precision": _safe_float(precision),
            "recall": _safe_float(recall),
            "f1_score": _safe_float(f1)
        },
        "sample_size": len(X_clean),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "model_params": {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "random_state": random_state
        },
        "confusion_matrix": cm.tolist()
    }

    # 转换所有numpy类型为Python原生类型
    return _convert_numpy_types(result)


def xgboost_regression(file_path: str, x_columns: List[str], y_column: str,
                      session_id: str = None, objective: str = 'reg:squarederror',
                      n_estimators: int = 100, max_depth: int = 6,
                      learning_rate: float = 0.3, subsample: float = 1.0,
                      colsample_bytree: float = 1.0, random_state: int = 42,
                      **kwargs) -> Dict[str, Any]:
    """
    XGBoost回归 - 使用XGBoost进行回归任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        session_id (str): 会话ID
        objective (str): 目标函数
            - "reg:squarederror": 回归平方损失（默认）
            - "reg:squaredlogerror": 回归平方对数损失
            - "reg:pseudohubererror": Huber回归
        n_estimators (int): 树的数量 (默认100)
        max_depth (int): 树的最大深度 (默认6)
        learning_rate (float): 学习率 (默认0.3)
        subsample (float): 子样本比例 (默认1.0)
        colsample_bytree (float): 每棵树使用的特征比例 (默认1.0)
        random_state (int): 随机种子 (默认42)
        **kwargs: 其他XGBoost参数

    Returns:
        Dict[str, Any]: 包含XGBoost回归结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, x_columns + [y_column], session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查是否有足够的特征列
    feature_columns = [col for col in x_columns if col in df.columns]
    if not feature_columns:
        raise ValueError("没有有效的特征列用于XGBoost回归")

    # 提取特征和目标变量
    X = df[feature_columns].select_dtypes(include=[np.number])
    y = df[y_column]

    # 检查是否有足够的数值型特征
    if X.shape[1] == 0:
        raise ValueError("没有有效的数值型特征列用于XGBoost回归")

    # 删除包含NaN的行
    mask = ~(X.isna().any(axis=1) | y.isna())
    X_clean = X[mask]
    y_clean = y[mask]

    if len(X_clean) == 0:
        raise ValueError("没有有效的数据可用于XGBoost回归")

    # 确保目标变量是数值型
    if not pd.api.types.is_numeric_dtype(y_clean):
        # 尝试转换为数值型
        y_clean = pd.to_numeric(y_clean, errors='coerce')
        # 再次删除NaN值
        mask = ~y_clean.isna()
        X_clean = X_clean[mask]
        y_clean = y_clean[mask]

    if len(X_clean) == 0:
        raise ValueError("目标列无法转换为数值型")

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X_clean, y_clean, test_size=0.2, random_state=random_state
    )

    # 创建XGBoost回归器
    reg = xgb.XGBRegressor(
        objective=objective,
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        **kwargs
    )

    # 训练模型
    reg.fit(X_train, y_train)

    # 预测
    y_pred = reg.predict(X_test)

    # 计算评估指标
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 获取特征重要性
    feature_importance = {feature: _safe_float(importance) for feature, importance in zip(feature_columns, reg.feature_importances_)}

    # 准备返回结果
    result = {
        "method": "xgboost_regression",
        "x_columns": feature_columns,
        "y_column": y_column,
        "objective": objective,
        "feature_importance": feature_importance,
        "evaluation_metrics": {
            "mse": _safe_float(mse),
            "rmse": _safe_float(rmse),
            "mae": _safe_float(mae),
            "r2_score": _safe_float(r2)
        },
        "sample_size": len(X_clean),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "model_params": {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "random_state": random_state
        }
    }

    # 转换所有numpy类型为Python原生类型
    return _convert_numpy_types(result)


def xgboost_analysis(file_path: str, x_columns: List[str], y_column: str,
                     task_type: str = "auto", session_id: str = None,
                     **kwargs) -> Dict[str, Any]:
    """
    XGBoost分析 - 自动判断任务类型并执行相应的XGBoost分析

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        task_type (str): 任务类型 ("classification", "regression", "auto")
        session_id (str): 会话ID
        **kwargs: 其他参数

    Returns:
        Dict[str, Any]: 包含XGBoost分析结果的字典
    """
    # 检查目标列的数据类型以确定任务类型
    df, _ = check_and_read(file_path, x_columns + [y_column], session_id)
    
    if task_type == "auto":
        y_values = df[y_column].dropna()
        
        # 如果目标列是分类类型或唯一值较少（假设小于等于10个唯一值为分类任务）
        if pd.api.types.is_object_dtype(y_values) or pd.api.types.is_bool_dtype(y_values):
            task_type = "classification"
        elif pd.api.types.is_numeric_dtype(y_values):
            unique_values = y_values.nunique()
            if unique_values <= 10:  # 假设唯一值少于等于10为分类任务
                task_type = "classification"
            else:
                task_type = "regression"
        else:
            task_type = "classification"  # 默认分类任务
    
    if task_type == "classification":
        return xgboost_classification(file_path, x_columns, y_column, session_id=session_id, **kwargs)
    else:
        return xgboost_regression(file_path, x_columns, y_column, session_id=session_id, **kwargs)