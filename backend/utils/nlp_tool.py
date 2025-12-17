import os
import sys
from typing import Dict, Any

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
    color_list = ['#FF274B']
    colormap = colors.ListedColormap(color_list)

    system = platform.system()

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
        "image_path": wordcloud_path,
        "top_words": dict(result[:50]),  # 返回前50个高频词
        "total_words": len(report_words)
    }

def test():
    # 测试默认词云
    result = generate_wordcloud(file_path="data/100/千星奇域评论数据最终版_edit.csv", column="content", session_id="100",
                                mask_shape="cloud",)
    print("默认词云测试完成")
    print(result)
    


if __name__ == "__main__":
    test()