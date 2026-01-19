"""
机器学习 API 模块
提供基于 sklearn、PyTorch 的机器学习算法，包括深度学习、SVM、随机森林等
"""

from typing import List, Dict, Any
from langchain_core.tools import tool
from .tool_error_handler import tool_error_handler
from utils.ml_tool import logistic_regression, clustering_analysis, xgboost_analysis,\
    xgboost_classification, xgboost_regression, svm_analysis, decision_tree_analysis,\
    decision_tree_classification, decision_tree_regression, neural_network_classification,\
    neural_network_regression, neural_network_analysis


# 注册逻辑回归工具
@tool
@tool_error_handler
def logistic_regression_tool(file_path: str, x_columns: List[str], y_column: str,
                          method: str = "logistic", session_id: str = None,
                          solver: str = 'lbfgs', **kwargs) -> Dict[str, Any]:
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
    return logistic_regression(file_path, x_columns, y_column, method, session_id, solver, **kwargs)


# 注册聚类分析工具
@tool
@tool_error_handler
def clustering_analysis_tool(file_path: str, columns: List[str],
                          method: str = "kmeans", n_clusters: int = 3, session_id: str = None,
                          **kwargs) -> Dict[str, Any]:
    """
    聚类分析 - 使用多种聚类算法对数据进行分组分析

    Args:
        file_path (str): 文件路径
        columns (List[str]): 用于聚类的列名列表
        method (str): 聚类方法
            - "kmeans": K-means聚类 (默认)
            - "hierarchical": 层次聚类
            - "dbscan": DBSCAN聚类
            - "gmm": 高斯混合模型
        n_clusters (int): 簇的数量 (对于K-means、层次聚类和GMM)
        session_id (str): 会话ID
        **kwargs: 其他参数，用于特定聚类方法的配置
            - standardize (bool): 是否标准化数据 (默认True)
            - init (str): K-means初始化方法 ("k-means++", "random") 
            - max_iter (int): K-means最大迭代次数 (默认300)
            - eps (float): DBSCAN的邻域半径 (默认0.5)
            - min_samples (int): DBSCAN的最小样本数 (默认5)
            - linkage (str): 层次聚类的链接方法 ("ward", "complete", "average", "single")
            - covariance_type (str): GMM协方差类型 ("full", "tied", "diag", "spherical")

    Returns:
        Dict[str, Any]: 包含聚类分析结果的字典
    """
    return clustering_analysis(file_path, columns, method, n_clusters, session_id, **kwargs)


# 注册XGBoost分类工具
@tool
@tool_error_handler
def xgboost_classification_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return xgboost_classification(file_path, x_columns, y_column, session_id, 
                                 objective, n_estimators, max_depth, 
                                 learning_rate, subsample, colsample_bytree, 
                                 random_state, **kwargs)


# 注册XGBoost回归工具
@tool
@tool_error_handler
def xgboost_regression_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return xgboost_regression(file_path, x_columns, y_column, session_id,
                              objective, n_estimators, max_depth,
                              learning_rate, subsample, colsample_bytree,
                              random_state, **kwargs)


# 注册XGBoost分析工具（自动判断分类或回归）
@tool
@tool_error_handler
def xgboost_analysis_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return xgboost_analysis(file_path, x_columns, y_column, task_type, session_id, **kwargs)


# 注册SVM分析工具
@tool
@tool_error_handler
def svm_analysis_tool(file_path: str, x_columns: List[str], y_column: str,
                     task_type: str = "classification", session_id: str = None,
                     kernel: str = 'rbf', C: float = 1.0, gamma: str = 'scale', degree: int = 3,
                     coef0: float = 0.0, shrinking: bool = True, probability: bool = True,
                     tol: float = 1e-3, max_iter: int = -1, **kwargs) -> Dict[str, Any]:
    """
    支持向量机(SVM)分析 - 使用SVM进行分类或回归任务

    Args:
        file_path (str): 文件路径
        x_columns (List[str]): 自变量列名列表（特征列）
        y_column (str): 因变量列名（目标列）
        task_type (str): 任务类型 ("classification" 或 "regression")
        session_id (str): 会话ID
        kernel (str): 核函数类型
            - "linear": 线性核
            - "poly": 多项式核
            - "rbf": 径向基函数核 (默认)
            - "sigmoid": Sigmoid核
            - "precomputed": 预计算核
        C (float): 正则化参数，值越大对错误分类的惩罚越大 (默认1.0)
        gamma (str or float): 核函数系数
            - "scale": 1/(n_features * X.var()) (默认)
            - "auto": 1/n_features
            - float: 指定值
        degree (int): 多项式核的度数 (仅对kernel="poly"有效，默认3)
        coef0 (float): 核函数中的独立项 (仅对"poly"和"sigmoid"有效，默认0.0)
        shrinking (bool): 是否使用启发式收缩启发式 (默认True)
        probability (bool): 是否启用概率预测 (默认True)
        tol (float): 停止准则的容忍度 (默认1e-3)
        max_iter (int): 最大迭代次数，-1表示无限制 (默认-1)
        **kwargs: 其他参数

    Returns:
        Dict[str, Any]: 包含SVM分析结果的字典
    """
    return svm_analysis(file_path, x_columns, y_column, task_type, session_id,
                       kernel, C, gamma, degree, coef0, shrinking, probability,
                       tol, max_iter, **kwargs)


# 注册决策树分类工具
@tool
@tool_error_handler
def decision_tree_classification_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return decision_tree_classification(file_path, x_columns, y_column, session_id,
                                      criterion, max_depth, min_samples_split,
                                      min_samples_leaf, max_features, random_state, **kwargs)


# 注册决策树回归工具
@tool
@tool_error_handler
def decision_tree_regression_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return decision_tree_regression(file_path, x_columns, y_column, session_id,
                                  criterion, max_depth, min_samples_split,
                                  min_samples_leaf, max_features, random_state, **kwargs)


# 注册决策树分析工具（自动判断分类或回归）
@tool
@tool_error_handler
def decision_tree_analysis_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return decision_tree_analysis(file_path, x_columns, y_column, task_type, session_id,
                                criterion, max_depth, min_samples_split, min_samples_leaf,
                                max_features, random_state, **kwargs)


# 注册神经网络分类工具
@tool
@tool_error_handler
def neural_network_classification_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return neural_network_classification(file_path, x_columns, y_column, session_id,
                                       hidden_layer_sizes, activation, solver, alpha,
                                       batch_size, learning_rate, learning_rate_init,
                                       max_iter, shuffle, random_state, tol,
                                       verbose, warm_start, momentum, nesterovs_momentum,
                                       early_stopping, validation_fraction, beta_1, beta_2,
                                       epsilon, n_iter_no_change, **kwargs)


# 注册神经网络回归工具
@tool
@tool_error_handler
def neural_network_regression_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return neural_network_regression(file_path, x_columns, y_column, session_id,
                                   hidden_layer_sizes, activation, solver, alpha,
                                   batch_size, learning_rate, learning_rate_init,
                                   max_iter, shuffle, random_state, tol,
                                   verbose, warm_start, momentum, nesterovs_momentum,
                                   early_stopping, validation_fraction, beta_1, beta_2,
                                   epsilon, n_iter_no_change, **kwargs)


# 注册神经网络分析工具（自动判断分类或回归）
@tool
@tool_error_handler
def neural_network_analysis_tool(file_path: str, x_columns: List[str], y_column: str,
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
    return neural_network_analysis(file_path, x_columns, y_column, task_type, session_id, **kwargs)


# 将模块中的函数注册为工具
def register_ml_tools(agent):
    """
    将机器学习工具注册到agent

    Args:
        agent: DataAnalysisAgent实例
    """
    agent.tools.append(logistic_regression_tool)
    agent.tools.append(clustering_analysis_tool)
    agent.tools.append(xgboost_classification_tool)
    agent.tools.append(xgboost_regression_tool)
    agent.tools.append(xgboost_analysis_tool)
    agent.tools.append(svm_analysis_tool)
    agent.tools.append(decision_tree_classification_tool)
    agent.tools.append(decision_tree_regression_tool)
    agent.tools.append(decision_tree_analysis_tool)
    agent.tools.append(neural_network_classification_tool)
    agent.tools.append(neural_network_regression_tool)
    agent.tools.append(neural_network_analysis_tool)
