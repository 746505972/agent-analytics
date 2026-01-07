from typing import List, Dict, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, QuantileTransformer, PowerTransformer
import numpy as np
from .check_and_read import check_and_read
from ..file_manager import generate_new_file_path


def dimensionless_processing(file_path: str, columns: List[str], method: str = "standard",
                             session_id: str = None, **kwargs) -> Dict[str, Any]:
    """
    量纲处理 - 对数据进行标准化、归一化等处理

    Args:
        file_path (str): 文件路径
        columns (List[str]): 需要处理的列名列表
        method (str): 处理方法
            - "standard": Z-score标准化 (默认)
            - "minmax": 最小-最大归一化 [0,1]
            - "robust": 鲁棒缩放 (使用中位数和四分位数)
            - "unit": 单位向量化 (L2范数)
            - "quantile": 分位数变换
            - "yeo-johnson": Yeo-Johnson变换
            - "box-cox": Box-Cox变换
            - "l1": L1范数标准化
            - "l2": L2范数标准化 (与unit相同)
            - "max": 最大值标准化
        session_id (str): 会话ID
        **kwargs: 其他参数，用于特定方法的配置
            - n_quantiles: 分位数变换的分位数数量 (默认100)
            - output_distribution: 分位数变换的输出分布 ('uniform'或'normal')
            - standardize: 是否在power变换后标准化数据 (默认True)

    Returns:
        Dict[str, Any]: 处理结果信息
    """
    df, numeric_columns = check_and_read(file_path, columns, session_id)

    # 根据方法选择对应的处理器
    if method == "standard":
        scaler = StandardScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    elif method == "minmax":
        scaler = MinMaxScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    elif method == "robust":
        scaler = RobustScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    elif method in ["unit", "l2"]:
        # L2范数标准化
        df[numeric_columns] = df[numeric_columns].div(
            np.linalg.norm(df[numeric_columns], axis=0), axis=1
        )

    elif method == "l1":
        # L1范数标准化
        df[numeric_columns] = df[numeric_columns].div(
            np.linalg.norm(df[numeric_columns], ord=1, axis=0), axis=1
        )

    elif method == "max":
        # 最大值标准化
        df[numeric_columns] = df[numeric_columns].div(
            df[numeric_columns].abs().max(), axis=1
        )

    elif method == "quantile":
        # 分位数变换
        n_quantiles = kwargs.get('n_quantiles', min(100, len(df)))
        output_distribution = kwargs.get('output_distribution', 'uniform')
        scaler = QuantileTransformer(n_quantiles=n_quantiles,
                                     output_distribution=output_distribution,
                                     random_state=0)
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    elif method == "yeo-johnson":
        # Yeo-Johnson变换
        standardize = kwargs.get('standardize', True)
        scaler = PowerTransformer(method='yeo-johnson', standardize=standardize)
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    elif method == "box-cox":
        # Box-Cox变换 (仅适用于正值)
        # 检查是否有非正值
        if (df[numeric_columns] <= 0).any().any():
            # 对非正值添加常数使其变为正值
            min_val = df[numeric_columns].min().min()
            if min_val <= 0:
                df[numeric_columns] = df[numeric_columns] + abs(min_val) + 1

        standardize = kwargs.get('standardize', True)
        scaler = PowerTransformer(method='box-cox', standardize=standardize)
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    else:
        raise ValueError(f"不支持的量纲处理方法: {method}")

    # 保存处理后的数据
    new_filename, new_file_path = generate_new_file_path(file_path, session_id)
    df.to_csv(new_file_path, index=False, encoding="utf-8-sig")

    return {
        "data_id": new_filename,
        "saved_path": new_file_path,
        "processed_columns": numeric_columns,
        "method": method
    }
