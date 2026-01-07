import jieba.posseg as pseg
from typing import Dict, Any
import os
from collections import Counter
# 导入pyecharts相关模块
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import ThemeType

from utils.file_manager import read_any_file, ensure_data_dir, ensure_session_dir, generate_new_file_path

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
    color_list = kwargs.get("color",
                            ['#FF274B', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8',
                             '#F7DC6F', '#BB8FCE'])

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
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True,
                                                                                               background_color="#fff"),
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
