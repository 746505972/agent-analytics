"""
决策树算法模块
提供决策树分类和回归功能
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score, confusion_matrix
)
from .check_and_read import check_and_read


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


def _safe_int(value):
    """安全地将值转换为int，处理无效值"""
    if value is None:
        return None
    try:
        if np.isnan(value) or np.isinf(value):
            return None
        return int(value)
    except (ValueError, TypeError):
        return None


def _convert_numpy_types(obj):
    """递归转换对象中的numpy数据类型为Python原生类型"""
    if isinstance(obj, np.ndarray):
        return [_safe_float(item) if isinstance(item, (np.floating, float)) else _safe_int(item) if isinstance(item, (int, np.integer)) else item for item in obj.tolist()]
    elif isinstance(obj, np.floating):
        return _safe_float(float(obj))
    elif isinstance(obj, np.integer):
        return _safe_int(int(obj))
    elif isinstance(obj, list):
        return [_convert_numpy_types(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (tuple, set, frozenset)):
        return type(obj)(_convert_numpy_types(item) for item in obj)
    else:
        return obj


def decision_tree_classification(file_path: str, x_columns: List[str], y_column: str,
                               session_id: str = None, criterion: str = 'gini',
                               max_depth: int = None, min_samples_split: int = 2,
                               min_samples_leaf: int = 1, max_features: str = None,
                               random_state: int = 42, **kwargs) -> Dict[str, Any]:
    """
    决策树分类 - 使用决策树进行分类任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列，分类标签）
        session_id (str): 会话ID
        criterion (str): 分割标准
            - "gini": 基尼不纯度 (默认)
            - "entropy": 信息熵
        max_depth (int): 树的最大深度，None表示无限制 (默认None)
        min_samples_split (int): 内部节点分裂所需的最小样本数 (默认2)
        min_samples_leaf (int): 叶节点所需的最小样本数 (默认1)
        max_features (str or int): 寻找最佳分割时考虑的特征数量
            - None: 使用所有特征
            - "sqrt": 使用sqrt(n_features)个特征
            - "log2": 使用log2(n_features)个特征
            - int: 指定具体数量
        random_state (int): 随机种子 (默认42)
        **kwargs: 其他决策树参数

    Returns:
        Dict[str, Any]: 包含决策树分类结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, x_columns + [y_column], session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查是否有足够的特征列
    feature_columns = [col for col in x_columns if col in df.columns]
    if not feature_columns:
        raise ValueError("没有有效的特征列用于决策树分类")

    # 提取特征和目标变量
    X = df[feature_columns].select_dtypes(include=[np.number])
    y = df[y_column]

    # 检查是否有足够的数值型特征
    if X.shape[1] == 0:
        raise ValueError("没有有效的数值型特征列用于决策树分类")

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
        raise ValueError("没有有效的数据可用于决策树分类")

    # 确定分类类型
    n_classes = len(np.unique(y_clean))
    if n_classes < 2:
        raise ValueError("目标列至少需要2个不同的类别")

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X_clean, y_clean, test_size=0.2, random_state=random_state, stratify=y_clean
    )

    # 创建决策树分类器
    clf = DecisionTreeClassifier(
        criterion=criterion,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        random_state=random_state,
        **kwargs
    )

    # 训练模型
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)

    # 计算评估指标
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    # 计算混淆矩阵
    cm = confusion_matrix(y_test, y_pred)

    # 获取特征重要性
    feature_importance = {feature: _safe_float(importance) for feature, importance in zip(feature_columns, clf.feature_importances_)}

    # 获取决策树参数
    tree_params = clf.get_params()

    # 准备返回结果
    result = {
        "method": "decision_tree_classification",
        "x_columns": feature_columns,
        "y_column": y_column,
        "criterion": criterion,
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
            "criterion": criterion,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "min_samples_leaf": min_samples_leaf,
            "max_features": max_features,
            "random_state": random_state
        },
        "tree_params": {k: v for k, v in tree_params.items() if k not in ['random_state', 'criterion', 'max_depth', 'min_samples_split', 'min_samples_leaf', 'max_features']},
        "confusion_matrix": cm.tolist()
    }

    # 转换所有numpy类型为Python原生类型
    return _convert_numpy_types(result)


def decision_tree_regression(file_path: str, x_columns: List[str], y_column: str,
                           session_id: str = None, criterion: str = 'squared_error',
                           max_depth: int = None, min_samples_split: int = 2,
                           min_samples_leaf: int = 1, max_features: str = None,
                           random_state: int = 42, **kwargs) -> Dict[str, Any]:
    """
    决策树回归 - 使用决策树进行回归任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        session_id (str): 会话ID
        criterion (str): 分割标准
            - "squared_error": 平方误差 (默认，sklearn 1.0+版本)
            - "friedman_mse": Friedman均方误差
            - "absolute_error": 绝对误差
            - "poisson": 泊松偏差
        max_depth (int): 树的最大深度，None表示无限制 (默认None)
        min_samples_split (int): 内部节点分裂所需的最小样本数 (默认2)
        min_samples_leaf (int): 叶节点所需的最小样本数 (默认1)
        max_features (str or int): 寻找最佳分割时考虑的特征数量
            - None: 使用所有特征
            - "sqrt": 使用sqrt(n_features)个特征
            - "log2": 使用log2(n_features)个特征
            - int: 指定具体数量
        random_state (int): 随机种子 (默认42)
        **kwargs: 其他决策树参数

    Returns:
        Dict[str, Any]: 包含决策树回归结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, x_columns + [y_column], session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查是否有足够的特征列
    feature_columns = [col for col in x_columns if col in df.columns]
    if not feature_columns:
        raise ValueError("没有有效的特征列用于决策树回归")

    # 提取特征和目标变量
    X = df[feature_columns].select_dtypes(include=[np.number])
    y = df[y_column]

    # 检查是否有足够的数值型特征
    if X.shape[1] == 0:
        raise ValueError("没有有效的数值型特征列用于决策树回归")

    # 删除包含NaN的行
    mask = ~(X.isna().any(axis=1) | y.isna())
    X_clean = X[mask]
    y_clean = y[mask]

    if len(X_clean) == 0:
        raise ValueError("没有有效的数据可用于决策树回归")

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

    # 创建决策树回归器
    # 根据sklearn版本支持不同的criterion参数
    reg = DecisionTreeRegressor(
        criterion=criterion,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
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

    # 获取决策树参数
    tree_params = reg.get_params()

    # 准备返回结果
    result = {
        "method": "decision_tree_regression",
        "x_columns": feature_columns,
        "y_column": y_column,
        "criterion": criterion,
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
            "criterion": criterion,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "min_samples_leaf": min_samples_leaf,
            "max_features": max_features,
            "random_state": random_state
        },
        "tree_params": {k: v for k, v in tree_params.items() if k not in ['random_state', 'criterion', 'max_depth', 'min_samples_split', 'min_samples_leaf', 'max_features']}
    }

    # 转换所有numpy类型为Python原生类型
    return _convert_numpy_types(result)


def decision_tree_analysis(file_path: str, x_columns: List[str], y_column: str,
                         task_type: str = "auto", session_id: str = None,
                         criterion: str = None, max_depth: int = None, 
                         min_samples_split: int = 2, min_samples_leaf: int = 1, 
                         max_features: str = None, random_state: int = 42,
                         **kwargs) -> Dict[str, Any]:
    """
    决策树分析 - 自动判断任务类型并执行相应的决策树分析

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        task_type (str): 任务类型 ("classification", "regression", "auto")
        session_id (str): 会话ID
        criterion (str): 分割标准
        max_depth (int): 树的最大深度
        min_samples_split (int): 内部节点分裂所需的最小样本数
        min_samples_leaf (int): 叶节点所需的最小样本数
        max_features (str): 寻找最佳分割时考虑的特征数量
        random_state (int): 随机种子
        **kwargs: 其他参数

    Returns:
        Dict[str, Any]: 包含决策树分析结果的字典
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
    
    # 设置默认的分割标准
    if criterion is None:
        if task_type == "classification":
            criterion = "gini"
        else:
            # 根据sklearn版本，使用适当的回归准则
            criterion = "squared_error"  # sklearn 1.0+版本的默认值
    
    # 准备参数字典
    params = {
        'criterion': criterion,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'max_features': max_features,
        'random_state': random_state,
        **kwargs
    }
    
    if task_type == "classification":
        return decision_tree_classification(file_path, x_columns, y_column, session_id=session_id, **params)
    else:
        return decision_tree_regression(file_path, x_columns, y_column, session_id=session_id, **params)