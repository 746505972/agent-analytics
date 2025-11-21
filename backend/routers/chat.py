"""
聊天路由模块
处理与LLM的交互
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import os
import pandas as pd
import numpy as np
import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

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
            # 调试：打印从cookie获取的session_id
            session_id = request.state.session_id
            logger.info(f"调试信息 - Session ID: {session_id}")
            
            logger.info("开始处理聊天请求")
            # 移除了聊天请求数据的日志打印，以保护用户隐私
            
            # 如果有data_id，获取文件路径并读取数据作为上下文
            data_context = None
            if chat_request.data_id:
                try:
                    from utils.file_manager import get_file_path
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
            
            # 执行agent，传递session_id给工具
            result = agent.process_query(chat_request.message, data_context, session_id)
            
            # 发送工具调用信息
            if result.get('tool_calls'):
                yield f"data: {json.dumps({'tool_calls': result['tool_calls']})}\n\n"
            
            # 发送结果信息
            response_text = result['result']
            for i in range(0, len(response_text), 10):
                chunk = response_text[i:i+10]
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            
            # 发送结束标记
            yield "data: [DONE]\n\n"
            logger.info("流式响应完成")
        except Exception as e:
            error_msg = f'后端错误: {str(e)}'
            logger.error(error_msg, exc_info=True)
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/execute")
async def execute_command(request: Request, chat_request: ChatRequest):
    """
    执行特定命令接口
    """
    try:
        # 调试：打印从cookie获取的session_id
        session_id = request.state.session_id
        logger.info(f"调试信息 - Session ID: {session_id}")
        
        logger.info("开始处理命令执行请求")
        
        # 如果有data_id，获取文件路径并读取数据作为上下文
        data_context = None
        if chat_request.data_id:
            try:
                from utils.file_manager import get_file_path
                # 获取session_id
                file_path = get_file_path(chat_request.data_id, session_id)
                if os.path.exists(file_path):
                    import pandas as pd
                    df = pd.read_csv(file_path, encoding="utf-8-sig")
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
                        "shape": df.shape,
                        "columns": list(df.columns),
                        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                        "sample_data": df.head().to_dict(),
                        "session_id": session_id  # 添加session_id到数据上下文
                    }
            except Exception as e:
                logger.warning(f"读取数据上下文时出错: {e}")
        
        # 使用agent处理查询，传递session_id
        result = agent.process_query(chat_request.message, data_context, session_id)
        
        return JSONResponse(content={
            "success": True,
            "result": result['result'],
            "tool_calls": result.get('tool_calls', [])
        })
    except Exception as e:
        error_msg = f'执行命令时出错: {str(e)}'
        logger.error(error_msg, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": error_msg
            }
        )