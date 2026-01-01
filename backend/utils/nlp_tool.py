import os
import sys
from typing import Dict, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.file_manager import read_any_file, ensure_data_dir, ensure_session_dir, generate_new_file_path
import jieba.posseg as pseg
from collections import Counter
from matplotlib import colors
import numpy as np
from snownlp import SnowNLP
import re

# 导入pyecharts相关模块
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import ThemeType

def generate_wordcloud(file_path: str, column: str, session_id: str = None, **kwargs) -> Dict[str, Any]:
    """
    生成词云图像
    
    Args:
        file_path (str): 数据文件路径
        column (str): 需要生成词云的列名
        session_id (str): 用户会话ID
        **kwargs: 其他参数，包括:
            - shape (str): 词云形状，默认'circle'，可选值: 'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'
            - word_gap (int): 单词间隔，默认20
            - word_size_range (List[int]): 字体大小范围，默认[12, 60]
            - rotate_step (int): 旋转步长，默认45
            - width (int): 图片宽度，默认1600
            - height (int): 图片高度，默认900
            - color (List[str]): 词云颜色列表
            - max_words (int): 最大词数，默认200
            - stopwords (List[str]): 自定义停用词列表
            
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
    stopwords = set()  # 不再使用wordcloud的STOPWORDS
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
    
    # 将结果转换为适合pyecharts WordCloud的数据格式
    wordcloud_data = [(word, count) for word, count in result]
    
    # 词云配置参数
    width = kwargs.get("width", 1600)
    height = kwargs.get("height", 900)
    shape = kwargs.get("shape", "circle")
    word_gap = kwargs.get("word_gap", 20)
    word_size_range = kwargs.get("word_size_range", [12, 60])
    rotate_step = kwargs.get("rotate_step", 45)
    
    # 设置颜色
    color_list = kwargs.get("color", ['#FF274B', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE'])
    
    # 创建保存目录
    save_dir = f'data/{session_id}' if session_id else 'data'
    os.makedirs(save_dir, exist_ok=True)

    # 生成HTML文件路径
    filename = os.path.splitext(os.path.basename(file_path))[0]
    wordcloud_filename = f"{filename}_{column}_wordcloud.html"
    chart_path = f'{save_dir}/{wordcloud_filename}'
    
    # 创建WordCloud实例
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(
            width=f"{width}px", 
            height=f"{height}px",
            theme=ThemeType.WHITE
        ))
        .add(
            series_name="词云",
            data_pair=wordcloud_data,
            word_size_range=word_size_range,  # 字体大小范围
            shape=shape,  # 词云形状
            word_gap=word_gap,  # 单词间隔
            rotate_step=rotate_step,  # 旋转步长
            textstyle_opts=opts.TextStyleOpts(color=color_list),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True),
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True,background_color="#fff"),
                                              magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False),
                                              data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                                              data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                                                )),
        )
    )
    
    # 保存图表到HTML文件
    wordcloud.render(chart_path)
    
    # 返回结果信息
    return {
        "chart_path": chart_path,  # 返回HTML文件路径
        "top_words": dict(result[:50]),  # 返回前50个高频词
        "total_words": len(report_words)
    }


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
