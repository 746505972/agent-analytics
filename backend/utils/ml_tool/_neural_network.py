"""
神经网络算法模块
提供基于scikit-learn的多层感知机(MLP)分类和回归功能
支持自定义激活函数和隐藏层节点配置
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score
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


def neural_network_classification(file_path: str, x_columns: List[str], y_column: str,
                                 session_id: str = None, hidden_layer_sizes: tuple = (100,),
                                 activation: str = 'relu', solver: str = 'adam',
                                 alpha: float = 0.0001, batch_size: str = 'auto',
                                 learning_rate: str = 'constant', learning_rate_init: float = 0.001,
                                 max_iter: int = 200, shuffle: bool = True,
                                 random_state: int = 42, tol: float = 1e-4,
                                 verbose: bool = False, warm_start: bool = False,
                                 momentum: float = 0.9, nesterovs_momentum: bool = True,
                                 early_stopping: bool = False, validation_fraction: float = 0.1,
                                 beta_1: float = 0.9, beta_2: float = 0.999,
                                 epsilon: float = 1e-8, n_iter_no_change: int = 10,
                                 **kwargs) -> Dict[str, Any]:
    """
    神经网络分类 - 使用多层感知机(MLP)进行分类任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列，分类标签）
        session_id (str): 会话ID
        
        # 神经网络结构参数
        hidden_layer_sizes (tuple): 隐藏层节点数元组 (例如 (100,) 表示1个隐藏层含100个节点, (50, 25) 表示2个隐藏层分别含50和25个节点)
        activation (str): 激活函数
            - "identity": 恒等函数
            - "logistic": sigmoid函数
            - "tanh": 双曲正切函数
            - "relu": ReLU函数 (默认)
        
        # 优化器参数
        solver (str): 求解器
            - "lbfgs": 拟牛顿法 (适合小数据集)
            - "sgd": 随机梯度下降
            - "adam": Adam优化器 (默认)
        alpha (float): L2正则化参数 (默认0.0001)
        batch_size (str or int): 批大小 (默认'auto')
        learning_rate (str): 学习率调整策略
            - "constant": 恒定学习率 (默认)
            - "invscaling": 逆缩放
            - "adaptive": 自适应
        learning_rate_init (float): 初始学习率 (默认0.001)
        
        # 训练参数
        max_iter (int): 最大迭代次数 (默认200)
        shuffle (bool): 是否在每次迭代前打乱样本 (默认True)
        random_state (int): 随机种子 (默认42)
        tol (float): 停止容差 (默认1e-4)
        verbose (bool): 是否输出训练过程信息 (默认False)
        warm_start (bool): 是否使用上次训练结果继续训练 (默认False)
        
        # SGD优化器特有参数
        momentum (float): 动量参数 (默认0.9)
        nesterovs_momentum (bool): 是否使用Nesterov动量 (默认True)
        
        # 早停参数
        early_stopping (bool): 是否启用早停 (默认False)
        validation_fraction (float): 验证集比例 (默认0.1)
        
        # Adam优化器特有参数
        beta_1 (float): Adam优化器参数 (默认0.9)
        beta_2 (float): Adam优化器参数 (默认0.999)
        epsilon (float): 数值稳定性参数 (默认1e-8)
        
        n_iter_no_change (int): 早停判断的不改善迭代次数 (默认10)
        
        **kwargs: 其他MLPClassifier参数

    Returns:
        Dict[str, Any]: 包含神经网络分类结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, x_columns + [y_column], session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查是否有足够的特征列
    feature_columns = [col for col in x_columns if col in df.columns]
    if not feature_columns:
        raise ValueError("没有有效的特征列用于神经网络分类")

    # 提取特征和目标变量
    X = df[feature_columns].select_dtypes(include=[np.number])
    y = df[y_column]

    # 检查是否有足够的数值型特征
    if X.shape[1] == 0:
        raise ValueError("没有有效的数值型特征列用于神经网络分类")

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
        raise ValueError("没有有效的数据可用于神经网络分类")

    # 确定分类类型
    n_classes = len(np.unique(y_clean))
    if n_classes < 2:
        raise ValueError("目标列至少需要2个不同的类别")

    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clean)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_clean, test_size=0.2, random_state=random_state, stratify=y_clean
    )

    # 创建神经网络分类器
    clf = MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes,
        activation=activation,
        solver=solver,
        alpha=alpha,
        batch_size=batch_size,
        learning_rate=learning_rate,
        learning_rate_init=learning_rate_init,
        max_iter=max_iter,
        shuffle=shuffle,
        random_state=random_state,
        tol=tol,
        verbose=verbose,
        warm_start=warm_start,
        momentum=momentum,
        nesterovs_momentum=nesterovs_momentum,
        early_stopping=early_stopping,
        validation_fraction=validation_fraction,
        beta_1=beta_1,
        beta_2=beta_2,
        epsilon=epsilon,
        n_iter_no_change=n_iter_no_change,
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
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)

    # 获取模型信息
    n_layers = clf.n_layers_ - 1  # 减去输入层
    n_outputs = clf.n_outputs_
    loss = clf.loss_
    best_loss = clf.best_loss_
    n_iter = clf.n_iter_

    # 准备返回结果
    result = {
        "method": "neural_network_classification",
        "x_columns": feature_columns,
        "y_column": y_column,
        "n_classes": int(n_classes),
        "class_labels": label_encoder.classes_.tolist(),
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
            "hidden_layer_sizes": hidden_layer_sizes,
            "activation": activation,
            "solver": solver,
            "alpha": alpha,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "learning_rate_init": learning_rate_init,
            "max_iter": max_iter,
            "shuffle": shuffle,
            "random_state": random_state,
            "tol": tol,
            "verbose": verbose,
            "warm_start": warm_start,
            "momentum": momentum,
            "nesterovs_momentum": nesterovs_momentum,
            "early_stopping": early_stopping,
            "validation_fraction": validation_fraction,
            "beta_1": beta_1,
            "beta_2": beta_2,
            "epsilon": epsilon,
            "n_iter_no_change": n_iter_no_change
        },
        "model_info": {
            "n_layers": n_layers,
            "n_outputs": n_outputs,
            "loss": _safe_float(loss),
            "best_loss": _safe_float(best_loss),
            "n_iter": n_iter
        },
        "confusion_matrix": cm.tolist()
    }

    # 转换所有numpy类型为Python原生类型
    return _convert_numpy_types(result)


def neural_network_regression(file_path: str, x_columns: List[str], y_column: str,
                            session_id: str = None, hidden_layer_sizes: tuple = (100,),
                            activation: str = 'relu', solver: str = 'adam',
                            alpha: float = 0.0001, batch_size: str = 'auto',
                            learning_rate: str = 'constant', learning_rate_init: float = 0.001,
                            max_iter: int = 200, shuffle: bool = True,
                            random_state: int = 42, tol: float = 1e-4,
                            verbose: bool = False, warm_start: bool = False,
                            momentum: float = 0.9, nesterovs_momentum: bool = True,
                            early_stopping: bool = False, validation_fraction: float = 0.1,
                            beta_1: float = 0.9, beta_2: float = 0.999,
                            epsilon: float = 1e-8, n_iter_no_change: int = 10,
                            **kwargs) -> Dict[str, Any]:
    """
    神经网络回归 - 使用多层感知机(MLP)进行回归任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        session_id (str): 会话ID
        
        # 神经网络结构参数
        hidden_layer_sizes (tuple): 隐藏层节点数元组 (例如 (100,) 表示1个隐藏层含100个节点, (50, 25) 表示2个隐藏层分别含50和25个节点)
        activation (str): 激活函数
            - "identity": 恒等函数
            - "logistic": sigmoid函数
            - "tanh": 双曲正切函数
            - "relu": ReLU函数 (默认)
        
        # 优化器参数
        solver (str): 求解器
            - "lbfgs": 拟牛顿法 (适合小数据集)
            - "sgd": 随机梯度下降
            - "adam": Adam优化器 (默认)
        alpha (float): L2正则化参数 (默认0.0001)
        batch_size (str or int): 批大小 (默认'auto')
        learning_rate (str): 学习率调整策略
            - "constant": 恒定学习率 (默认)
            - "invscaling": 逆缩放
            - "adaptive": 自适应
        learning_rate_init (float): 初始学习率 (默认0.001)
        
        # 训练参数
        max_iter (int): 最大迭代次数 (默认200)
        shuffle (bool): 是否在每次迭代前打乱样本 (默认True)
        random_state (int): 随机种子 (默认42)
        tol (float): 停止容差 (默认1e-4)
        verbose (bool): 是否输出训练过程信息 (默认False)
        warm_start (bool): 是否使用上次训练结果继续训练 (默认False)
        
        # SGD优化器特有参数
        momentum (float): 动量参数 (默认0.9)
        nesterovs_momentum (bool): 是否使用Nesterov动量 (默认True)
        
        # 早停参数
        early_stopping (bool): 是否启用早停 (默认False)
        validation_fraction (float): 验证集比例 (默认0.1)
        
        # Adam优化器特有参数
        beta_1 (float): Adam优化器参数 (默认0.9)
        beta_2 (float): Adam优化器参数 (默认0.999)
        epsilon (float): 数值稳定性参数 (默认1e-8)
        
        n_iter_no_change (int): 早停判断的不改善迭代次数 (默认10)
        
        **kwargs: 其他MLPRegressor参数

    Returns:
        Dict[str, Any]: 包含神经网络回归结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, x_columns + [y_column], session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 检查是否有足够的特征列
    feature_columns = [col for col in x_columns if col in df.columns]
    if not feature_columns:
        raise ValueError("没有有效的特征列用于神经网络回归")

    # 提取特征和目标变量
    X = df[feature_columns].select_dtypes(include=[np.number])
    y = df[y_column]

    # 检查是否有足够的数值型特征
    if X.shape[1] == 0:
        raise ValueError("没有有效的数值型特征列用于神经网络回归")

    # 删除包含NaN的行
    mask = ~(X.isna().any(axis=1) | y.isna())
    X_clean = X[mask]
    y_clean = y[mask]

    if len(X_clean) == 0:
        raise ValueError("没有有效的数据可用于神经网络回归")

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

    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clean)
    y_scaled = y_clean  # 对于回归，我们通常不需要缩放目标变量

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_scaled, test_size=0.2, random_state=random_state
    )

    # 创建神经网络回归器
    reg = MLPRegressor(
        hidden_layer_sizes=hidden_layer_sizes,
        activation=activation,
        solver=solver,
        alpha=alpha,
        batch_size=batch_size,
        learning_rate=learning_rate,
        learning_rate_init=learning_rate_init,
        max_iter=max_iter,
        shuffle=shuffle,
        random_state=random_state,
        tol=tol,
        verbose=verbose,
        warm_start=warm_start,
        momentum=momentum,
        nesterovs_momentum=nesterovs_momentum,
        early_stopping=early_stopping,
        validation_fraction=validation_fraction,
        beta_1=beta_1,
        beta_2=beta_2,
        epsilon=epsilon,
        n_iter_no_change=n_iter_no_change,
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

    # 获取模型信息
    n_layers = reg.n_layers_ - 1  # 减去输入层
    n_outputs = reg.n_outputs_
    loss = reg.loss_
    best_loss = reg.best_loss_
    n_iter = reg.n_iter_

    # 准备返回结果
    result = {
        "method": "neural_network_regression",
        "x_columns": feature_columns,
        "y_column": y_column,
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
            "hidden_layer_sizes": hidden_layer_sizes,
            "activation": activation,
            "solver": solver,
            "alpha": alpha,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "learning_rate_init": learning_rate_init,
            "max_iter": max_iter,
            "shuffle": shuffle,
            "random_state": random_state,
            "tol": tol,
            "verbose": verbose,
            "warm_start": warm_start,
            "momentum": momentum,
            "nesterovs_momentum": nesterovs_momentum,
            "early_stopping": early_stopping,
            "validation_fraction": validation_fraction,
            "beta_1": beta_1,
            "beta_2": beta_2,
            "epsilon": epsilon,
            "n_iter_no_change": n_iter_no_change
        },
        "model_info": {
            "n_layers": n_layers,
            "n_outputs": n_outputs,
            "loss": _safe_float(loss),
            "best_loss": _safe_float(best_loss),
            "n_iter": n_iter
        }
    }

    # 转换所有numpy类型为Python原生类型
    return _convert_numpy_types(result)


def neural_network_analysis(file_path: str, x_columns: List[str], y_column: str,
                          task_type: str = "auto", session_id: str = None,
                          **kwargs) -> Dict[str, Any]:
    """
    神经网络分析 - 自动判断任务类型并执行相应的神经网络分析

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        task_type (str): 任务类型 ("classification", "regression", "auto")
        session_id (str): 会话ID
        **kwargs: 其他参数

    Returns:
        Dict[str, Any]: 包含神经网络分析结果的字典
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
        return neural_network_classification(file_path, x_columns, y_column, session_id=session_id, **kwargs)
    else:
        return neural_network_regression(file_path, x_columns, y_column, session_id=session_id, **kwargs)