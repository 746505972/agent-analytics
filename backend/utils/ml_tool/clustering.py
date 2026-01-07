from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.decomposition import PCA
import warnings
import os
from pathlib import Path
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


def clustering_analysis(file_path: str, 
                        columns: List[str], 
                        method: str = "kmeans", 
                        n_clusters: int = 3, 
                        session_id: str = None,
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
    # 检查文件和列的有效性
    df, numeric_columns = check_and_read(file_path, columns, session_id)

    # 确保有足够的数值列用于聚类
    if not numeric_columns:
        raise ValueError("没有有效的数值型列用于聚类分析")

    # 获取参数
    standardize = kwargs.get("standardize", True)
    max_iter = kwargs.get("max_iter", 300)

    # 准备数据
    X = df[numeric_columns].dropna()

    if len(X) == 0:
        raise ValueError("没有有效的数据可用于聚类分析")

    if len(X) < n_clusters:
        raise ValueError(f"数据样本数量({len(X)})少于指定的簇数量({n_clusters})")

    # 标准化数据
    if standardize:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X.values

    # 根据方法选择聚类算法
    if method == "kmeans":
        init_method = kwargs.get("init", "k-means++")
        model = KMeans(
            n_clusters=n_clusters,
            init=init_method,
            max_iter=max_iter,
            random_state=42,
            n_init=10
        )
    elif method == "hierarchical":
        linkage = kwargs.get("linkage", "ward")
        model = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage=linkage
        )
    elif method == "dbscan":
        eps = kwargs.get("eps", 0.5)
        min_samples = kwargs.get("min_samples", 5)
        model = DBSCAN(
            eps=eps,
            min_samples=min_samples
        )
    elif method == "gmm":
        covariance_type = kwargs.get("covariance_type", "full")
        model = GaussianMixture(
            n_components=n_clusters,
            covariance_type=covariance_type,
            random_state=42,
            max_iter=max_iter
        )
    else:
        raise ValueError(f"不支持的聚类方法: {method}")

    # 执行聚类
    cluster_labels = model.fit_predict(X_scaled)

    # 对于DBSCAN，需要调整簇数量（DBSCAN会生成-1的噪声点标签）
    if method == "dbscan":
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)

    # 计算聚类评估指标
    evaluation_metrics = {}
    if n_clusters > 1 and len(set(cluster_labels)) > 1:  # 只有在有多个簇时才计算轮廓系数
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                silhouette_avg = silhouette_score(X_scaled, cluster_labels)
                evaluation_metrics["silhouette_score"] = _safe_float(silhouette_avg)
            except:
                evaluation_metrics["silhouette_score"] = None

        try:
            calinski_harabasz = calinski_harabasz_score(X_scaled, cluster_labels)
            evaluation_metrics["calinski_harabasz_score"] = _safe_float(calinski_harabasz)
        except:
            evaluation_metrics["calinski_harabasz_score"] = None

    # 计算每个簇的统计信息
    cluster_stats = {}
    unique_labels = np.unique(cluster_labels)
    for label in unique_labels:
        mask = cluster_labels == label
        cluster_data = X.iloc[mask] if isinstance(X, pd.DataFrame) else pd.DataFrame(X_scaled[mask], columns=numeric_columns)
        
        cluster_stats[str(label)] = {
            "size": int(np.sum(mask)),
            "proportion": _safe_float(np.sum(mask) / len(cluster_labels)),
            "centroid": {col: _safe_float(cluster_data[col].mean()) for col in numeric_columns}
        }

    # 获取原始数据的索引（去除缺失值后的）
    original_indices = X.index.tolist()

    # 将聚类结果保存为CSV
    # 创建包含原始数据和聚类标签的DataFrame
    result_df = df.loc[original_indices].copy()  # 使用原始数据的子集
    result_df['cluster_label'] = cluster_labels

    # 生成结果文件路径
    filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_clustering_result"
    result_file_path = os.path.join("data", session_id, f"{filename}.csv")

    # 保存为CSV
    result_df.to_csv(result_file_path, index=False, encoding='utf-8-sig')

    # 准备返回结果
    result = {
        "method": method,
        "columns": numeric_columns,
        "n_clusters": n_clusters,
        "cluster_labels": [int(label) for label in cluster_labels][:19],  # 保留原始标签列表用于前端显示统计
        "original_indices": original_indices,
        "cluster_stats": cluster_stats,
        "evaluation_metrics": evaluation_metrics,
        "sample_size": len(cluster_labels),
        "result_file_path": result_file_path,  # 返回结果文件路径
        "model_params": {
            "n_clusters": n_clusters,
            "standardize": standardize,
            "max_iter": max_iter
        }
    }

    # 添加特定算法的参数
    if method == "kmeans":
        result["model_params"]["init"] = init_method
    elif method == "dbscan":
        result["model_params"]["eps"] = eps
        result["model_params"]["min_samples"] = min_samples
    elif method == "hierarchical":
        result["model_params"]["linkage"] = linkage
    elif method == "gmm":
        result["model_params"]["covariance_type"] = covariance_type

    return result