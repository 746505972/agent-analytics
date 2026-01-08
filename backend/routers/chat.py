"""
聊天路由模块
处理与LLM的交互
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import os
import numpy as np
import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from utils.file_manager import get_file_path
# 导入Agent
from agents import DataAnalysisAgent

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由实例
router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    data_id: str = None
    history: list = []

# 初始化全局agent实例
agent = DataAnalysisAgent()

class SessionTitleManager:
    def __init__(self):
        self.session_titles = {}
    
    def is_first_query(self, session_id: str, history: list) -> bool:
        """
        判断是否是当前会话的第一次查询
        """ 
        # 统计用户发送的消息数量（type为'sent'的消息）
        user_message_count = 0
        for msg in history:
            # 前端的消息对象有type字段，但在history中可能只有content和type等信息
            if isinstance(msg, dict) and msg.get('type') == 'sent':
                user_message_count += 1
        
        # 如果用户只发送过一条消息，则表示这是第一次查询
        return user_message_count == 1
    
    def generate_session_title(self, user_query: str, data_context=None) -> str:
        """
        根据用户查询和数据上下文生成会话标题
        """
        import os
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
            
        llm = ChatOpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model="qwen-plus"
        )
        
        # 构造提示词，让AI生成会话标题
        prompt = f"请根据用户的数据分析需求生成一个简洁的会话标题（不超过15个字）：{user_query}。只需要返回标题，不要其他内容。"
        
        try:
            response = llm.invoke(prompt)
            title = response.content.strip()
            # 限制标题长度
            if len(title) > 20:
                title = title[:20] + "..."
            return title
        except Exception as e:
            logger.error(f"生成会话标题时出错: {e}")
            # 如果生成失败，返回用户查询的前几个字
            return user_query[:10] + "..." if len(user_query) > 10 else user_query

# 创建会话标题管理器实例
title_manager = SessionTitleManager()

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
            session_id = request.state.session_id
            
            logger.info("开始处理聊天请求")
            # 移除了聊天请求数据的日志打印，以保护用户隐私
            
            # 如果有data_id，获取文件路径并读取数据作为上下文
            data_context = None
            if chat_request.data_id:
                try:
                    # 获取session_id
                    file_path = get_file_path(chat_request.data_id, session_id)
                    # 移除了文件路径的日志打印，以保护用户隐私
                    if os.path.exists(file_path):
                        import pandas as pd
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                        # 处理NaN值，将其替换为None以便JSON序列化
                        df = df.replace({pd.NA: None, pd.NaT: None, np.nan: None})
                        
                        # 确保所有值都可以被JSON序列化
                        for col in df.columns:
                            def convert_value(x):
                                if pd.isna(x) or x is None:
                                    return None
                                if hasattr(x, 'item'):
                                    try:
                                        return x.item()
                                    except (ValueError, OverflowError):
                                        return str(x)
                                return x
                            df[col] = df[col].apply(convert_value)
                        
                        data_context = {
                            "data_id": chat_request.data_id,
                            "filename": f"{chat_request.data_id}.csv",
                            "file_path":f"data/{session_id}/{chat_request.data_id}.csv",
                            "shape": df.shape,
                            "columns": list(df.columns),
                            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                            "sample_data": df.head().to_dict(),
                            "session_id": session_id  # 添加session_id到数据上下文
                        }
                        # 移除了数据上下文的日志打印，以保护用户隐私
                    else:
                        logger.warning(f"文件不存在: {file_path}")
                except Exception as e:
                    logger.warning(f"读取数据上下文时出错: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
            
            # 流式执行agent，传递session_id给工具
            async for response_chunk in agent.process_query_stream(chat_request.message, data_context, session_id):
                if response_chunk['type'] == 'tool_calls':
                    yield f"data: {json.dumps({'tool_calls': response_chunk['data']})}\n\n"
                elif response_chunk['type'] == 'content':
                    yield f"data: {json.dumps({'content': response_chunk['data']})}\n\n"
                # elif response_chunk['type'] == 'error':
                #     yield f"data: {json.dumps({'error': response_chunk['data']})}\n\n"
                elif response_chunk['type'] == 'end':
                    yield "data: [DONE]\n\n"
                    break
            
            logger.info("流式响应完成")
        except Exception as e:
            error_msg = f'后端错误: {str(e)}'
            logger.error(error_msg, exc_info=True)
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")