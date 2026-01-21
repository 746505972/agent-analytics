"""
该模块暂未使用
"""

from langchain_core.tools import tool
from .tool_error_handler import tool_error_handler


def register_search_tools(self):
    @tool
    @tool_error_handler
    def get_tools_list():
        """
        获取工具列表
        """
        tools = {"basic": ['read_file','delete_file_tool','list_user_files', 'add_header_row_tool', 'modify_header_row_tool', 'remove_first_row_tool', 'delete_columns_tool'],
                 "pandas": ['remove_invalid_samples_tool', 'handle_missing_values_tool', 'dimensionless_processing_tool', 'scientific_calculation_tool', 'one_hot_encoding_tool', 'statistical_summary_tool', 'correlation_analysis_tool', 'text_to_numeric_or_datetime_tool', 'normality_test_tool', 't_test_tool', 'f_test_tool', 'chi_square_test_tool', 'non_parametric_test_tool', 'linear_regression_tool'],
                 "machine learning": ['logistic_regression_tool', 'clustering_analysis_tool', 'xgboost_classification_tool', 'xgboost_regression_tool', 'xgboost_analysis_tool', 'svm_analysis_tool'],
                 "search": ['get_tools_list','get_tool_description']}

        return tools

    self.tools.append(get_tools_list)

    @tool
    @tool_error_handler
    def get_tool_description(tool_name: str):
        """
        获取工具描述
        """
        match tool_name:
            case "read_file":
                content = """
                读取文件的前n行数据
                Args:
                    file_path (str): 文件路径
                    n (int): 行数，默认为10
                """
            case "delete_file_tool":
                content = """
                删除指定的数据文件
                Args:
                    data_id (str): 文件ID
                    session_id (str): session_id
                """
            case "list_user_files":
                content = """
                获取用户上传的文件列表
                Args:
                    session_id (str): session_id
                """
            case "add_header_row_tool":
                content = """
                为没有标题行的文件添加标题行并创建新文件
                Args:
                    file_path (str): 文件路径
                    column_names (list): 列名列表
                    session_id: session_id
                """
            case "modify_header_row_tool":
                content = """
                修改文件的现有标题行并创建新文件
                Args:
                    file_path (str): 文件路径
                    column_names (list): 新的列名列表
                    session_id: session_id
                """
            case "remove_first_row_tool":
                content = """
                删除文件的第一行（通常是有问题的标题行）并创建新文件
                Args:
                    file_path (str): 文件路径
                    session_id: session_id
                """
            case "delete_columns_tool":
                content = """
                删除文件中的指定列并创建新文件
                Args:
                    file_path (str): 文件路径
                    columns_to_delete (list): 要删除的列名列表
                    session_id (str): session_id
                """
            case "remove_invalid_samples_tool":
                content = """
                去除无效样本 - 处理重复数据和超出阈值的行列
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
                    remove_duplicates (bool): 是否去除重复行
                    remove_duplicate_cols (bool): 是否删除重复列
                    remove_constant_cols (bool): 是否删除所有数据都相同的列
                    row_missing_threshold (float): 行缺失值阈值 (0-1之间)
                    col_missing_threshold (float): 列缺失值阈值 (0-1之间)
                """
            case "handle_missing_values_tool":
                content = """
                对缺失数据进行插值
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
                    specified_columns (List[str]): 指定要处理的列名列表，如果为None则处理所有列
                    interpolation_method (str): 插值方法 ("linear", "ffill", "bfill", "mean", "median", "mode", "knn", "constant")
                    fill_value (Any): 当使用constant方法时的填充值
                    knn_neighbors (int): KNN插值的邻居数量
                """
            case "dimensionless_processing_tool":
                content = """
                量纲处理 - 对数据进行标准化、归一化等处理
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
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
                """
            case "scientific_calculation_tool":
                content = """
                科学计算 - 对数据执行数学运算
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
                    columns (List[str]): 需要处理的列名列表
                    operation (str): 运算类型 ("log", "exp", "power", "sqrt", "poly")
                    params (dict): 运算参数
                """
            case "one_hot_encoding_tool":
                content = """
                独热编码 - 对分类变量进行独热编码处理
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
                    columns (List[str]): 需要处理的列名列表
                    drop_first (bool): 是否删除第一个虚拟变量以避免多重共线性
                """
            case "statistical_summary_tool":
                content = """
                统计摘要 - 计算并返回指定列的统计摘要信息
                返回包括样本量、平均值、中位数、方差、标准差、最小值、最大值、四分位数、峰度、偏度等在内的全面统计信息
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
                    columns (List[str]): 需要处理的列名列表
                """
            case "text_to_numeric_or_datetime_tool":
                content = """
                文本转数值/时间 - 将包含千位分隔符、单位缩写（K,M等）的文本列转换为数值列，或将时间戳转换为时间列
            
                Args:
                    file_path (str): 文件路径
                    columns (List[str]): 需要处理的列名列表
                    convert_to (str): 转换目标类型 "numeric" 或 "datetime"
                    session_id (str): 会话ID
                    datetime_format (str): 时间格式(可选)，如转换为时间时可指定格式，例如 "%Y-%m-%d %H:%M:%S"
                """
            case "correlation_analysis_tool":
                content = """
                相关性分析 - 计算并返回指定列之间的相关系数和p值
                返回每对变量之间的相关系数以及对应的p值，用于评估变量间的相关性强弱和统计显著性
                Args:
                    file_path (str): 文件路径
                    session_id (str): session_id
                    columns (List[str]): 需要分析的列名列表
                    method (str): 相关性计算方法 ("pearson", "spearman", "kendall")
                """
            case "normality_test_tool":
                content = """
                正态性检验（自带常值检验）
            
                Args:
                    file_path (str): 文件路径
                    columns (List[str]): 需要检验的列名列表
                    session_id (str): session_id
                    method (str): 正态性检验方法 ("shapiro", "normaltest")
                    alpha (float): 显著性水平 (默认0.05)
                    group_by (str): 分组列名，如果提供则按组进行正态性检验
                """
            case "t_test_tool":
                content = """
                T检验 - 对数据执行不同类型的T检验，自带正态性检验
            
                Args:
                    file_path (str): 文件路径
                    columns (List[str]): 需要分析的列名列表
                    test_type (str): T检验类型
                        - "one_sample": 单样本T检验
                        - "independent": 独立样本T检验
                        - "paired": 配对样本T检验
                    session_id (str): 会话ID
                    **kwargs: 其他参数，用于特定检验的配置
                        - popmean: 单样本t检验中的总体均值 (用于"one_sample"类型)
                        - equal_var: 独立样本t检验中是否假设方差相等 (用于"independent"类型)
                        - group_col: 分组列名，用于独立样本t检验 (用于"independent"类型)
                        - normality_method: 正态性检验方法 ("shapiro", "normaltest")
                        - alpha: 显著性水平 (默认0.05)
            
                Returns:
                    Dict[str, Any]: 包含T检验结果和正态性检验结果的字典
                """
            case "f_test_tool":
                content = """
                F检验 - 对数据执行F检验，用于检验多个样本的方差是否相等或进行方差分析(ANOVA)
            
                Args:
                    file_path (str): 文件路径
                    columns (List[str]): 需要分析的列名列表
                    session_id (str): 会话ID
                    group_by (str): 分组列名，用于进行组间方差分析
                    alpha (float): 显著性水平 (默认0.05)
            
                Returns:
                    Dict[str, Any]: 包含F检验结果的字典
                """
            case "chi_square_test_tool":
                content = """
                卡方检验 - 对分类变量进行独立性检验或拟合优度检验
            
                Args:
                    file_path (str): 文件路径
                    columns (List[str]): 需要分析的列名列表（需要是分类变量列）
                    session_id (str): 会话ID
                    group_by (str): 分组列名，用于进行独立性检验
                    alpha (float): 显著性水平 (默认0.05)
            
                Returns:
                    Dict[str, Any]: 包含卡方检验结果的字典
                """
            case "non_parametric_test_tool":
                content = """
                非参数检验 - 提供多种非参数检验方法
            
                Args:
                    file_path (str): 文件路径
                    columns (List[str]): 需要分析的列名列表
                    test_type (str): 非参数检验类型
                        - "mannwhitney": Mann-Whitney U检验（两个独立样本）
                        - "wilcoxon": Wilcoxon符号秩检验（两个相关样本）
                        - "kruskal": Kruskal-Wallis检验（多个独立样本）
                        - "kolmogorov_smirnov": Kolmogorov-Smirnov检验（单样本或两样本）
                    session_id (str): 会话ID
                    group_by (str): 分组列名，用于进行分组检验
                    alpha (float): 显著性水平 (默认0.05)
                    **kwargs: 其他参数
                        - alternative: 检验方向 ("two-sided", "less", "greater")
                        - distribution: 单样本K-S检验的理论分布 ("norm", "uniform", "expon", "logistic")
            
                Returns:
                    Dict[str, Any]: 包含非参数检验结果的字典
                """
            case "linear_regression_tool":
                content = """
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
            case "logistic_regression_tool":
                content = """
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
            case "clustering_analysis_tool":
                content = """
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
            case "xgboost_classification_tool":
                content = """
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
            case "xgboost_regression_tool":
                content = """
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
            case "xgboost_analysis_tool":
                content = """
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
            case "svm_analysis_tool":
                content = """
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
            case _:
                content = "文档不存在"

        return  content

    self.tools.append(get_tool_description)



