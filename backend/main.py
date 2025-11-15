# main.py
import sys
import os

# 添加当前目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List, Dict
import uuid
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 确保所有相关的日志器都设置为INFO级别
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)

# 检查环境变量
logger.info(f"DASHSCOPE_API_KEY 环境变量设置情况: {bool(os.getenv('DASHSCOPE_API_KEY'))}")

# 使用绝对导入代替相对导入
from utils.file_manager import upload_file, read_any_file, delete_file, get_file_path
from routers.chat import router as chat_router
from routers.data import router as data_router
from routers.files import router as files_router

app = FastAPI(title="Agent-Analytics API", description="数据分析系统的后端API")

# 添加CORS中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)
app.include_router(data_router)
app.include_router(files_router)

# 确保数据目录存在
os.makedirs("data", exist_ok=True)

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # 为每个请求生成或获取session_id
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # 将session_id添加到请求状态中
    request.state.session_id = session_id
    
    response = await call_next(request)
    
    # 设置session cookie
    if not request.cookies.get("session_id"):
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    return response

@app.get("/")
async def root():
    return {"message": "欢迎使用 Agent-Analytics API"}

@app.post("/upload")
async def upload_data_file(request: Request, file: UploadFile = File(...)):
    """
    上传数据文件接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 生成唯一的文件名
        file_extension = os.path.splitext(file.filename)[1]
        temp_file_name = f"temp_{uuid.uuid4()}{file_extension}"
        
        # 保存上传的文件
        with open(temp_file_name, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 使用现有的文件管理器处理文件，传入原始文件名和session_id
        result = upload_file(temp_file_name, file.filename, session_id)
        
        # 删除临时文件
        os.remove(temp_file_name)
        
        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)