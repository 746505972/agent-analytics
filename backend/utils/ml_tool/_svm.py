from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
import os
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


def svm_analysis(file_path: str, x_columns: List[str], y_column: str,
                 task_type: str = "classification", session_id: str = None,
                 kernel: str = 'rbf', C: float = 1.0, gamma: str = 'scale', degree: int = 3,
                 coef0: float = 0.0, shrinking: bool = True, probability: bool = True,
                 tol: float = 1e-3, max_iter: int = -1) -> Dict[str, Any]:
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

    Returns:
        Dict[str, Any]: 包含SVM分析结果的字典
    """
    # 检查文件和列的有效性
    df, numeric_x_columns = check_and_read(file_path, x_columns, session_id)

    # 检查目标列是否存在
    if y_column not in df.columns:
        raise ValueError(f"目标列 '{y_column}' 不存在于数据集中")

    # 准备数据
    X = df[numeric_x_columns].dropna()
    y_df = df[y_column].loc[X.index]  # 只保留X中对应行的y值

    # 过滤掉y中的缺失值
    y_clean = y_df.dropna()
    X = X.loc[y_clean.index]
    y = y_clean.values

    if len(X) == 0:
        raise ValueError("没有有效的数据可用于SVM分析")

    # 根据任务类型决定是分类还是回归
    if task_type.lower() == "classification":
        # 对y列进行标签编码（转换分类标签为数值）
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)
        
        # 创建SVM分类器
        model = SVC(
            kernel=kernel,
            C=C,
            gamma=gamma,
            degree=degree,
            coef0=coef0,
            shrinking=shrinking,
            probability=probability,
            tol=tol,
            max_iter=max_iter,
            random_state=42
        )
        
        # 拟合模型
        model.fit(X, y_encoded)
        
        # 预测
        y_pred = model.predict(X)
        
        # 计算评估指标
        accuracy = accuracy_score(y_encoded, y_pred)
        
        # 检查是否为二分类或多分类
        unique_labels = np.unique(y_encoded)
        n_classes = len(unique_labels)
        
        if n_classes > 2:
            # 多分类情况
            precision = precision_score(y_encoded, y_pred, average='macro', zero_division=0)
            recall = recall_score(y_encoded, y_pred, average='macro', zero_division=0)
            f1 = f1_score(y_encoded, y_pred, average='macro', zero_division=0)
            
            # 微平均
            precision_micro = precision_score(y_encoded, y_pred, average='micro', zero_division=0)
            recall_micro = recall_score(y_encoded, y_pred, average='micro', zero_division=0)
            f1_micro = f1_score(y_encoded, y_pred, average='micro', zero_division=0)
        else:
            # 二分类情况
            precision = precision_score(y_encoded, y_pred, zero_division=0)
            recall = recall_score(y_encoded, y_pred, zero_division=0)
            f1 = f1_score(y_encoded, y_pred, zero_division=0)
            precision_micro = recall_micro = f1_micro = None

        # 获取支持向量的数量
        n_support_vectors = model.n_support_
        support_vectors_count = int(np.sum(n_support_vectors))

        # 生成包含原始数据和预测标签的DataFrame
        result_df = df.loc[X.index].copy()
        result_df['svm_predicted_label'] = y_pred
        # 添加原始真实标签
        result_df['actual_label'] = y_encoded

        # 生成结果文件路径
        filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_svm_classification_result"
        result_file_path = os.path.join("data", session_id, f"{filename}.csv")

        # 保存为CSV
        result_df.to_csv(result_file_path, index=False, encoding='utf-8-sig')

        # 准备返回结果
        result = {
            "method": "svm_classification",
            "task_type": task_type,
            "x_columns": numeric_x_columns,
            "y_column": y_column,
            "support_vectors_count": support_vectors_count,
            "n_support_vectors_per_class": n_support_vectors.tolist(),
            "n_classes": n_classes,
            "class_labels": label_encoder.classes_.tolist(),
            "evaluation_metrics": {
                "accuracy": _safe_float(accuracy),
                "precision": _safe_float(precision),
                "recall": _safe_float(recall),
                "f1_score": _safe_float(f1),
                "precision_micro": _safe_float(precision_micro),
                "recall_micro": _safe_float(recall_micro),
                "f1_micro": _safe_float(f1_micro)
            },
            "sample_size": len(X),
            "predicted_labels": [int(label) for label in y_pred],
            "result_file_path": result_file_path,  # 返回结果文件路径
            "model_params": {
                "kernel": kernel,
                "C": C,
                "gamma": gamma,
                "degree": degree,
                "coef0": coef0,
                "shrinking": shrinking,
                "probability": probability,
                "tol": tol,
                "max_iter": max_iter
            }
        }
        
    elif task_type.lower() == "regression":
        # SVM回归
        model = SVR(
            kernel=kernel,
            C=C,
            gamma=gamma,
            degree=degree,
            coef0=coef0,
            shrinking=shrinking,
            tol=tol,
            max_iter=max_iter
        )
        
        # 拟合模型
        model.fit(X, y)
        
        # 预测
        y_pred = model.predict(X)
        
        # 计算评估指标
        mse = mean_squared_error(y, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, y_pred)
        
        # 计算平均绝对误差
        mae = np.mean(np.abs(y - y_pred))
        
        # 获取支持向量的数量
        support_vectors_count = model.support_vectors_.shape[0]

        # 生成包含原始数据和预测值的DataFrame
        result_df = df.loc[X.index].copy()
        result_df['svm_predicted_value'] = y_pred
        result_df['actual_value'] = y

        # 生成结果文件路径
        filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_svm_regression_result"
        result_file_path = os.path.join("data", session_id, f"{filename}.csv")

        # 保存为CSV
        result_df.to_csv(result_file_path, index=False, encoding='utf-8-sig')

        # 准备返回结果
        result = {
            "method": "svm_regression",
            "task_type": task_type,
            "x_columns": numeric_x_columns,
            "y_column": y_column,
            "support_vectors_count": support_vectors_count,
            "evaluation_metrics": {
                "mse": _safe_float(mse),
                "rmse": _safe_float(rmse),
                "r2_score": _safe_float(r2),
                "mae": _safe_float(mae)
            },
            "sample_size": len(X),
            "predicted_values": [float(val) for val in y_pred],
            "result_file_path": result_file_path,  # 返回结果文件路径
            "model_params": {
                "kernel": kernel,
                "C": C,
                "gamma": gamma,
                "degree": degree,
                "coef0": coef0,
                "shrinking": shrinking,
                "tol": tol,
                "max_iter": max_iter
            }
        }
    else:
        raise ValueError(f"不支持的任务类型: {task_type}. 支持的类型: 'classification', 'regression'")

    return result