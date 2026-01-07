from typing import Dict, Any
import re
from snownlp import SnowNLP
from collections import Counter
import numpy as np
from utils.file_manager import read_any_file, ensure_data_dir, ensure_session_dir, generate_new_file_path

def analyze_sentiment(file_path: str, column: str, session_id: str = None, **kwargs) -> Dict[str, Any]:
    """
    分析文本情感

    Args:
        file_path (str): 数据文件路径
        column (str): 需要分析情感的列名
        session_id (str): 用户会话ID
        **kwargs: 其他参数，包括:
            - stopwords (List[str]): 自定义停用词列表
            - internet_slang (Dict[str, str]): 网络用语映射字典

    Returns:
        Dict[str, Any]: 情感分析结果，包括情感分布比例、统计数据等
    """

    # 确保数据目录存在
    ensure_data_dir()

    if session_id:
        ensure_session_dir(session_id)

    # 读取数据文件
    df = read_any_file(file_path)

    # 检查列是否存在
    if column not in df.columns:
        raise ValueError(f"列 '{column}' 不存在于数据文件中")

    # 提取指定列的文本数据
    text_data = df[column].dropna().astype(str).tolist()

    # 处理网络用语
    internet_slang = kwargs.get("internet_slang", {})

    # 情感分析结果存储
    sentiments = []
    scores = []

    # 初始化情感分析器
    analyzer = SentimentAnalyzer(internet_slang)

    # 对每条文本进行情感分析
    for text in text_data:
        sentiment, score = analyzer.analyze_sentiment(text)
        sentiments.append(sentiment)
        scores.append(score)

    # 统计情感分布
    sentiment_counts = Counter(sentiments)
    total_count = len(sentiments)

    # 计算各类情感的比例
    positive_ratio = sentiment_counts.get('正面', 0) / total_count if total_count > 0 else 0
    neutral_ratio = sentiment_counts.get('中性', 0) / total_count if total_count > 0 else 0
    negative_ratio = sentiment_counts.get('负面', 0) / total_count if total_count > 0 else 0

    # 计算统计信息
    avg_score = np.mean(scores) if scores else 0
    std_score = np.std(scores) if scores else 0

    # 准备ECharts饼图数据
    pie_chart_data = [
        {"name": "正面", "value": sentiment_counts.get('正面', 0)},
        {"name": "中性", "value": sentiment_counts.get('中性', 0)},
        {"name": "负面", "value": sentiment_counts.get('负面', 0)}
    ]

    # 准备ECharts箱线图数据
    positive_scores = [scores[i] for i, s in enumerate(sentiments) if s == '正面']
    neutral_scores = [scores[i] for i, s in enumerate(sentiments) if s == '中性']
    negative_scores = [scores[i] for i, s in enumerate(sentiments) if s == '负面']

    boxplot_data = {
        "positive": positive_scores,
        "neutral": neutral_scores,
        "negative": negative_scores
    }

    # 返回结果
    return {
        "sentiment_ratios": {
            "positive": positive_ratio,
            "neutral": neutral_ratio,
            "negative": negative_ratio
        },
        "statistics": {
            "total_count": total_count,
            "average_score": float(avg_score),
            "std_score": float(std_score)
        },
        "sentiment_counts": dict(sentiment_counts),
        "echarts_data": {
            "pie_chart": pie_chart_data,
            "boxplot_data": boxplot_data
        }
    }


class SentimentAnalyzer:
    def __init__(self, internet_slang: Dict[str, str] = None):
        # 网络用语词典
        self.internet_slang = internet_slang or {
            '智齿': '支持', '栓q': '谢谢', 'yyds': '永远的神', 'xswl': '笑死我了',
            '破防': '感动', '绝绝子': '非常好', '躺平': '放弃努力', '内卷': '过度竞争',
            '氪金': '充值', '肝': '花费时间', '欧': '运气好', '非': '运气差',
            '大佬': '高手', '萌新': '新手', 'awsl': '啊我死了', 'nb': '牛逼',
            'hhh': '哈哈哈', '233': '哈哈哈', '狗头': '开玩笑', 'doge': '开玩笑',
            '蚌埠住了': '忍不住了', 'emmmm': '犹豫', '呜呜': '哭泣', '啊啊': '激动'
        }

    def preprocess_text(self, text):
        """预处理文本，处理网络用语"""
        if not isinstance(text, str):
            return ""

        # 转换网络用语
        for slang, meaning in self.internet_slang.items():
            text = text.replace(slang, meaning)

        # 移除URL
        text = re.sub(r'http\S+', '', text)
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符但保留中文和基本标点
        text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：""''（）《》【】]', '', text)

        return text.strip()

    def rule_based_correction(self, original_text, sentiment, score):
        """基于规则的修正"""
        text = original_text.lower()

        # 正面规则
        positive_patterns = [
            '智齿', '支持', '好期待', '太棒了', '厉害', '牛逼', 'yyds', '绝绝子',
            '太好了', '喜欢', '爱了', '期待', '不错', '可以', '好好', '哈哈', '哈哈哈',
            '开心', '高兴', '满意', '赞', '顶', '加油', '冲鸭', '太香了'
        ]

        # 负面规则
        negative_patterns = [
            '垃圾', '无语', '失望', '难受', '生气', '坑', '骗', '差评', '不行',
            '不好', '讨厌', '恶心', '吐了', '弃坑', '退游', '卸载', '凉了',
            '逼氪', '太肝', '坑钱', '优化差', '卡顿', '闪退'
        ]

        # 强烈正面词汇直接覆盖
        for pattern in positive_patterns:
            if pattern in text:
                return '正面', max(score, 0.8)  # 确保高分

        # 强烈负面词汇直接覆盖
        for pattern in negative_patterns:
            if pattern in text:
                return '负面', min(score, 0.2)  # 确保低分

        return sentiment, score

    def analyze_sentiment(self, text):
        """分析单条文本情感"""
        original_text = text
        processed_text = self.preprocess_text(text)

        if len(processed_text) < 2:
            return '中性', 0.5

        try:
            s = SnowNLP(processed_text)
            sentiment_score = s.sentiments

            # 根据得分初步分类
            if sentiment_score > 0.6:
                sentiment = '正面'
            elif sentiment_score < 0.4:
                sentiment = '负面'
            else:
                sentiment = '中性'

            # 应用规则修正
            final_sentiment, final_score = self.rule_based_correction(
                original_text, sentiment, sentiment_score
            )

            return final_sentiment, final_score

        except Exception as e:
            print(f"分析错误: {e}")
            return '中性', 0.5
