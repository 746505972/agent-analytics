import os
import sys
from typing import Dict, Any, List

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.file_manager import read_any_file, ensure_data_dir, ensure_session_dir, generate_new_file_path
import jieba.posseg as pseg
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import colors
import platform
import numpy as np
from PIL import Image
from snownlp import SnowNLP
import re

def generate_wordcloud(file_path: str, column: str, session_id: str = None, **kwargs) -> Dict[str, Any]:
    """
    生成词云图像
    
    Args:
        file_path (str): 数据文件路径
        column (str): 需要生成词云的列名
        session_id (str): 用户会话ID
        **kwargs: 其他参数，包括:
            - stopwords (List[str]): 自定义停用词列表
            - max_words (int): 最大词数，默认200
            - width (int): 图片宽度，默认1600
            - height (int): 图片高度，默认900
            - background_color (str): 背景颜色，默认'white'
            - max_font_size (int): 最大字体大小，默认200
            - min_font_size (int): 最小字体大小，默认10
            - mask_shape (str): 蒙版形状，可选值: 'circle', 'heart', 'star', 'cloud', 'default'
            
    Returns:
        Dict[str, Any]: 生成结果信息
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
    text = " ".join(text_data)
    
    # 分词处理
    words = pseg.cut(text)
    
    # 处理停用词
    stopwords = set(STOPWORDS)
    custom_stopwords = kwargs.get("stopwords", [])
    stopwords.update([word.lower() for word in custom_stopwords])
    
    # 提取名词并过滤停用词
    report_words = []
    for word, flag in words:
        word_lower = word.lower()
        if (len(word) >= 2) and ('n' in flag) and (word_lower not in stopwords):
            report_words.append(word)
    
    # 统计高频词汇
    max_words = kwargs.get("max_words", 200)
    result = Counter(report_words).most_common(max_words)
    content = dict(result)
    
    # 词云配置参数
    width = kwargs.get("width", 1600)
    height = kwargs.get("height", 900)
    background_color = kwargs.get("background_color", "white")
    max_font_size = kwargs.get("max_font_size", 200)
    min_font_size = kwargs.get("min_font_size", 10)
    
    # 设置颜色
    color_list = kwargs.get("color_list",['#FF274B'])
    colormap = colors.ListedColormap(color_list)

    system = platform.system()
    font_path = None
    if system == "Windows":
        font_path = r"C:\Windows\Fonts\STLITI.TTF"
    elif system == "Linux":
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    elif system == "Darwin":
        font_path = "/System/Library/Fonts/PingFang.ttc"


    # 处理蒙版
    mask = None
    mask_shape = kwargs.get("mask_shape", "default")
    if mask_shape:
        # 确定蒙版文件路径
        mask_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "masks")
        mask_file = f"{mask_shape}.png"
        mask_path = os.path.join(mask_dir, mask_file)
        
        # 检查蒙版文件是否存在
        if os.path.exists(mask_path):
            # 加载蒙版图片
            mask_image = Image.open(mask_path).convert('RGBA')
            # 转换为numpy数组供wordcloud使用
            mask = np.array(mask_image)
    
    # 生成词云配置
    wordcloud_config = {
        'scale': 4,
        'colormap': colormap,
        'width': width,
        'height': height,
        'background_color': background_color,
        'stopwords': stopwords,
        'max_font_size': max_font_size,
        'min_font_size': min_font_size,
        'font_path': font_path
    }

    
    # 如果有蒙版，则设置蒙版
    if mask is not None:
        wordcloud_config['mask'] = mask

    # 生成词云
    wordcloud = WordCloud(**wordcloud_config)
    wordcloud.generate_from_frequencies(content)
    
    # 生成保存路径
    filename = os.path.splitext(os.path.basename(file_path))[0]
    wordcloud_filename = f"{filename}_{column}_wordcloud.png"
    
    if session_id:
        wordcloud_path = os.path.join("data", session_id, wordcloud_filename)
    else:
        wordcloud_path = os.path.join("data", wordcloud_filename)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(wordcloud_path), exist_ok=True)
    
    # 保存词云图
    wordcloud.to_file(wordcloud_path)
    
    # 返回结果信息
    return {
        "image_path": wordcloud_path.replace("\\", "/"),  # 确保使用正斜杠，避免Windows路径问题
        "top_words": dict(result[:50]),  # 返回前50个高频词
        "total_words": len(report_words)
    }




def test():
    # 测试默认词云
    result = analyze_sentiment(file_path="data/100/千星奇域评论数据最终版_edit.csv", column="content", session_id="100",
                                )
    print(result)
    

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


if __name__ == "__main__":
    test()