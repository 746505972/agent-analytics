import os
import sys

# 添加项目根目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel
from typing import List, Dict, Any

from routers.data import load_csv_file

# 导入pyecharts相关模块
from pyecharts import options as opts
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType


router = APIRouter(prefix="/charts", tags=["charts"])

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartConfig(BaseModel):
    chart_type: str
    data_id: str
    x_axis_column: str
    y_axis_columns: List[str]
    chart_title: str = "图表标题"
    chart_styles: Dict[str, Any] = {
        "showGrid": True,
        "smoothLine": True,  # 仅对折线图有效
        "showArea": False,   # 仅对折线图有效
        "showLabel": False,
        "showLegend": True,
        "xAxisLabelRotate": 0,
        "yAxisMin": None,
        "yAxisMax": None,
        "stack": False,
        "step": False,       # 仅对折线图有效
        "showSymbol": True,  # 仅对折线图有效
        "showToolbox": True
    }
    color_scheme: int = 0
    custom_colors: Dict[str, str] = {"line": "#5470c6", "bar": "#5470c6"}


@router.post("/generate")
async def generate_chart(request: Request, config: ChartConfig):
    """
    生成图表HTML并返回文件路径
    """
    try:
        session_id = request.state.session_id

        # 加载数据
        success, df, status_code = load_csv_file(config.data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={"success": False, "error": df}
            )

        # 过滤掉空的Y轴字段
        valid_y_axis_columns = [col for col in config.y_axis_columns if col != '']

        # 创建保存目录
        save_dir = f'data/{session_id}'
        os.makedirs(save_dir, exist_ok=True)

        # 创建临时HTML文件
        chart_path = f'{save_dir}/temp.html'

        # 根据图表类型生成图表
        if config.chart_type == 'line':
            chart = create_line_chart(df, config, valid_y_axis_columns)
        elif config.chart_type == 'bar':
            chart = create_bar_chart(df, config, valid_y_axis_columns)
        elif config.chart_type == 'bar':
            chart = create_bar_chart(df, config, valid_y_axis_columns)
        elif config.chart_type == 'scatter':
            chart = create_scatter_chart(df, config, valid_y_axis_columns)
        elif config.chart_type == 'pie':
            chart = create_pie_chart(df, config, valid_y_axis_columns)
        elif config.chart_type == 'histogram':
            chart = create_histogram_chart(df, config, valid_y_axis_columns)
        elif config.chart_type == 'boxplot':
            chart = create_boxplot_chart(df, config, valid_y_axis_columns)
        else:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": f"不支持的图表类型: {config.chart_type}"}
            )

        # 保存图表到HTML文件
        chart.render(chart_path)


        # 返回图表路径
        return JSONResponse(content={
            "success": True,
            "chart_path": chart_path
        })

    except Exception as e:
        logger.error(f"生成图表时出错: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


def create_line_chart(df, config, y_axis_columns):
    """创建折线图"""
    # 获取颜色方案
    color_schemes = [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
    ]
    colors = color_schemes[config.color_scheme % len(color_schemes)]

    # 创建折线图实例
    line = Line(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500px"))
    
    # 设置全局配置
    line.set_global_opts(
        title_opts=opts.TitleOpts(title=config.chart_title),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(is_show=config.chart_styles.get("showLegend", True)),
        toolbox_opts=opts.ToolboxOpts(is_show=config.chart_styles.get("showToolbox", True), feature=opts.ToolBoxFeatureOpts(save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True))),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            name=config.x_axis_column,
            axislabel_opts=opts.LabelOpts(rotate=config.chart_styles.get("xAxisLabelRotate", 0)),
            splitline_opts=opts.SplitLineOpts(is_show=config.chart_styles.get("showGrid", True))
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            min_=config.chart_styles.get("yAxisMin"),
            max_=config.chart_styles.get("yAxisMax"),
            splitline_opts=opts.SplitLineOpts(is_show=config.chart_styles.get("showGrid", True))
        ),
        datazoom_opts=[
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
            opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
        ]
    )

    # 添加X轴数据
    x_data = df[config.x_axis_column].tolist()
    line.add_xaxis(xaxis_data=x_data)

    # 添加Y轴系列
    for i, y_col in enumerate(y_axis_columns):
        y_data = df[y_col].tolist()
        color = colors[i % len(colors)] if i < len(colors) else config.custom_colors.get("line", "#5470c6")
        line.add_yaxis(
            series_name=y_col,
            y_axis=y_data,
            symbol_size=4 if config.chart_styles.get("showSymbol", True) else 0,
            is_smooth=config.chart_styles.get("smoothLine", True),
            is_step=config.chart_styles.get("step", False),
            is_connect_nones=False,
            label_opts=opts.LabelOpts(is_show=config.chart_styles.get("showLabel", False)),
            linestyle_opts=opts.LineStyleOpts(color=color, width=2),
            itemstyle_opts=opts.ItemStyleOpts(color=color),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3) if config.chart_styles.get("showArea", False) else None,
            stack=config.chart_styles.get("stack", False)
        )

    return line


def create_bar_chart(df, config, y_axis_columns):
    """创建柱状图"""
    # 获取颜色方案
    color_schemes = [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
    ]
    colors = color_schemes[config.color_scheme % len(color_schemes)]

    # 创建柱状图实例
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500px"))
    
    # 设置全局配置
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=config.chart_title),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        legend_opts=opts.LegendOpts(is_show=config.chart_styles.get("showLegend", True)),
        toolbox_opts=opts.ToolboxOpts(is_show=config.chart_styles.get("showToolbox", True), feature=opts.ToolBoxFeatureOpts(save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True))),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            name=config.x_axis_column,
            axislabel_opts=opts.LabelOpts(rotate=config.chart_styles.get("xAxisLabelRotate", 0)),
            splitline_opts=opts.SplitLineOpts(is_show=config.chart_styles.get("showGrid", True))
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            min_=config.chart_styles.get("yAxisMin"),
            max_=config.chart_styles.get("yAxisMax"),
            splitline_opts=opts.SplitLineOpts(is_show=config.chart_styles.get("showGrid", True))
        ),
        datazoom_opts=[
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
            opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
        ]
    )

    # 添加X轴数据
    x_data = df[config.x_axis_column].tolist()
    bar.add_xaxis(xaxis_data=x_data)

    # 添加Y轴系列
    for i, y_col in enumerate(y_axis_columns):
        y_data = df[y_col].tolist()
        color = colors[i % len(colors)] if i < len(colors) else config.custom_colors.get("bar", "#5470c6")
        bar.add_yaxis(
            series_name=y_col,
            y_axis=y_data,
            label_opts=opts.LabelOpts(is_show=config.chart_styles.get("showLabel", False)),
            itemstyle_opts=opts.ItemStyleOpts(color=color),
            stack=config.chart_styles.get("stack", False)
        )

    return bar


def create_scatter_chart(df, config, y_axis_columns):
    """创建散点图"""
    # 获取颜色方案
    color_schemes = [
        ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074'],
        ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1'],
        ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53', '#eedd78', '#73a373', '#73b9bc', '#7289ab']
    ]
    colors = color_schemes[config.color_scheme % len(color_schemes)]

    # 创建散点图实例
    from pyecharts.charts import Scatter
    scatter = Scatter(init_opts=opts.InitOpts(theme=ThemeType.WHITE, width="100%", height="500px"))
    
    # 设置全局配置
    scatter.set_global_opts(
        title_opts=opts.TitleOpts(title=config.chart_title),
        tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="cross"),
        legend_opts=opts.LegendOpts(is_show=config.chart_styles.get("showLegend", True)),
        toolbox_opts=opts.ToolboxOpts(is_show=config.chart_styles.get("showToolbox", True), feature=opts.ToolBoxFeatureOpts(save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True))),
        xaxis_opts=opts.AxisOpts(
            type_="value",
            name=config.x_axis_column,
            splitline_opts=opts.SplitLineOpts(is_show=config.chart_styles.get("showGrid", True))
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=config.y_axis_columns[0] if config.y_axis_columns else "Y轴",
            splitline_opts=opts.SplitLineOpts(is_show=config.chart_styles.get("showGrid", True))
        ),
        datazoom_opts=[
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
            opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
        ]
    )

    # 添加X轴数据
    x_data = df[config.x_axis_column].tolist()
    
    # 添加Y轴系列（散点图通常只处理一个Y轴，但为了保持一致性，我们处理多个Y轴）
    for i, y_col in enumerate(y_axis_columns):
        y_data = df[y_col].tolist()
        # 将X和Y数据组合成散点数据
        scatter_data = [[x_data[j], y_data[j]] for j in range(len(x_data))]
        color = colors[i % len(colors)] if i < len(colors) else config.custom_colors.get("scatter", "#5470c6")
        scatter.add_yaxis(
            series_name=y_col,
            y_axis=scatter_data,
            label_opts=opts.LabelOpts(is_show=config.chart_styles.get("showLabel", False)),
            itemstyle_opts=opts.ItemStyleOpts(color=color),
            symbol_size=10
        )

    return scatter
