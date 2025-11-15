"""
聊天路由模块
处理与LLM的交互
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import os
import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由实例
router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    data_id: str = None
    history: list = []

# 初始化千问模型
def get_qwen_model():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    logger.info(f"DASHSCOPE_API_KEY 环境变量设置情况: {bool(api_key)}")
    
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
    
    logger.info("正在初始化千问模型...")
    model = ChatOpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus",
    )
    logger.info("千问模型初始化完成")
    return model

@router.post("/test")
async def test_chat():
    """
    测试接口，用于验证路由是否正常工作
    """
    return JSONResponse(content={"message": "聊天路由工作正常"})

@router.post("/stream")
async def chat_stream(request: Request, chat_request: ChatRequest):
    """
    流式聊天接口
    """
    async def generate():
        try:
            logger.info("开始处理聊天请求")
            # 获取模型实例
            model = get_qwen_model()
            logger.info("模型初始化成功")
            
            # 构建消息历史
            messages = [SystemMessage(content="你是一个数据分析助手，帮助用户分析数据文件。")]
            
            # 添加历史消息
            for msg in chat_request.history:
                if msg["type"] == "sent":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["type"] == "received":
                    messages.append(AIMessage(content=msg["content"]))
            
            # 添加当前用户消息
            messages.append(HumanMessage(content=chat_request.message))
            logger.info(f"构建消息完成，消息数量: {len(messages)}")
            
            # 调用模型进行流式响应
            logger.info("开始调用模型")
            async for chunk in model.astream(messages):
                # 发送每个chunk
                content = chunk.content
                logger.info(f"收到模型响应片段: {content}")
                yield f"data: {json.dumps({'content': content})}\n\n"
            
            # 发送结束标记
            yield "data: [DONE]\n\n"
            logger.info("流式响应完成")
        except Exception as e:
            error_msg = f'后端错误: {str(e)}'
            logger.error(error_msg, exc_info=True)
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")