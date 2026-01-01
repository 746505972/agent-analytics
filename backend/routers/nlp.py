import sys
import os

# 添加项目根目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel
from typing import List, Optional, Dict

from routers.data import load_csv_file
from utils.nlp_tool import generate_wordcloud, analyze_sentiment
from utils.file_manager import get_file_path

router = APIRouter(prefix="/nlp", tags=["nlp"])

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WordCloudRequest(BaseModel):
    """
    词云生成请求模型
    """
    column: str  # 需要生成词云的列名
    shape: Optional[str] = "circle"  # 词云形状
    word_gap: Optional[int] = 20  # 单词间隔
    word_size_range: Optional[List[int]] = [12, 60]  # 字体大小范围
    rotate_step: Optional[int] = 45  # 旋转步长
    width: Optional[int] = 1600  # 图片宽度
    height: Optional[int] = 900  # 图片高度
    color: Optional[List[str]] = ["#FF274B"]  # 词云颜色列表
    max_words: Optional[int] = 200  # 最大词数
    stopwords: Optional[List[str]] = []  # 自定义停用词列表


class SentimentAnalysisRequest(BaseModel):
    """
    情感分析请求模型
    """
    column: str  # 需要分析情感的列名
    stopwords: Optional[List[str]] = []  # 自定义停用词列表
    internet_slang: Optional[Dict[str, str]] = {}  # 网络用语映射


@router.post("/{data_id}/wordcloud")
async def generate_wordcloud_endpoint(request: Request, data_id: str, body: WordCloudRequest):
    """
    生成词云图像接口

    Args:
        request: FastAPI请求对象
        data_id: 数据文件ID
        body: 词云生成请求参数

    Returns:
        JSONResponse: 词云生成结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 获取文件路径
        file_path = get_file_path(data_id, session_id)

        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": f"文件不存在: {file_path}"
                }
            )

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )

        df = result

        # 检查DataFrame是否为空
        if df.empty:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "数据文件为空"
                }
            )

        # 检查指定列是否存在
        if body.column not in df.columns:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"列 '{body.column}' 不存在于数据文件中"
                }
            )

        # 调用工具函数生成词云
        wordcloud_result = generate_wordcloud(
            file_path=file_path,
            column=body.column,
            session_id=session_id,
            shape=body.shape,
            word_gap=body.word_gap,
            word_size_range=body.word_size_range,
            rotate_step=body.rotate_step,
            width=body.width,
            height=body.height,
            color=body.color,
            max_words=body.max_words,
            stopwords=body.stopwords
        )

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "column": body.column,
            "chart_path": wordcloud_result["chart_path"],  # 返回HTML文件路径
            "top_words": wordcloud_result["top_words"],
            "total_words": wordcloud_result["total_words"]
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"生成词云时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@router.post("/{data_id}/sentiment")
async def analyze_sentiment_endpoint(request: Request, data_id: str, body: SentimentAnalysisRequest):
    """
    情感分析接口

    Args:
        request: FastAPI请求对象
        data_id: 数据文件ID
        body: 情感分析请求参数

    Returns:
        JSONResponse: 情感分析结果
    """
    try:
        # 获取session_id
        session_id = request.state.session_id

        # 获取文件路径
        file_path = get_file_path(data_id, session_id)

        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": f"文件不存在: {file_path}"
                }
            )

        # 加载CSV文件
        success, result, status_code = load_csv_file(data_id, session_id)
        if not success:
            return JSONResponse(
                status_code=status_code,
                content={
                    "success": False,
                    "error": result
                }
            )

        df = result

        # 检查DataFrame是否为空
        if df.empty:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "数据文件为空"
                }
            )

        # 检查指定列是否存在
        if body.column not in df.columns:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"列 '{body.column}' 不存在于数据文件中"
                }
            )

        # 调用工具函数进行情感分析
        sentiment_result = analyze_sentiment(
            file_path=file_path,
            column=body.column,
            session_id=session_id,
            stopwords=body.stopwords,
            internet_slang=body.internet_slang
        )

        # 准备返回结果
        result_data = {
            "data_id": data_id,
            "column": body.column,
            "sentiment_ratios": sentiment_result["sentiment_ratios"],
            "statistics": sentiment_result["statistics"],
            "sentiment_counts": sentiment_result["sentiment_counts"],
            "echarts_data": sentiment_result["echarts_data"]
        }

        return JSONResponse(content={
            "success": True,
            "data": result_data
        })
    except Exception as e:
        logger.error(f"情感分析时出错: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )