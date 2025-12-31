# main.py
import asyncio
import os
import sys

# 添加当前目录到sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)
# 确保数据目录存在
os.makedirs("data", exist_ok=True)
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
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
from utils.file_manager import upload_file
from utils.cleanup import clean_expired_sessions_and_files
from routers.chat import router as chat_router
from routers.data import router as data_router
from routers.files import router as files_router
from routers.analysis import router as analysis_router
from routers.nlp import router as nlp_router
from routers.charts import router as charts_router

app = FastAPI(title="Agent-Analytics API", description="数据分析系统的后端API")

# 添加CORS中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:5173", "http://localhost:5173"],  # Electron前端地址和开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)
app.include_router(data_router)
app.include_router(files_router)
app.include_router(analysis_router)
app.include_router(nlp_router)
app.include_router(charts_router)

# 挂载静态文件目录，使生成的图片可以通过URL访问
app.mount("/data", StaticFiles(directory="data"), name="data")

# 存储定时任务的引用
cleanup_task = None

async def periodic_cleanup():
    """
    定期清理过期的session数据
    """
    while True:
        try:
            logger.info("开始执行定期清理任务...")
            clean_expired_sessions_and_files(expiration_hours=10)  # 10小时过期
            logger.info("定期清理任务执行完成")
        except Exception as e:
            logger.error(f"定期清理任务执行出错: {e}")
        
        # 每隔10分钟执行一次清理
        await asyncio.sleep(3600)  # 600秒 = 10分钟

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # 为每个请求生成或获取session_id
    session_id = request.cookies.get("session_id")
    if not session_id:
        # session_id = str(uuid.uuid4())
        session_id = "000"
    
    # 将session_id添加到请求状态中
    request.state.session_id = session_id
    
    response = await call_next(request)
    
    # 设置session cookie
    if not request.cookies.get("session_id"):
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    # 添加ngrok跳过浏览器警告头部
    response.headers["ngrok-skip-browser-warning"] = "true"
    
    return response

@app.get("/")
async def root():
    return {"message": "欢迎使用 Agent-Analytics API"}

@app.get("/upload")
async def get_upload():
    """
    上传文件页面占位符
    """
    return JSONResponse(content={
        "message": "请使用POST方法上传文件"
    })

@app.post("/upload")
async def upload_data_file(request: Request, file: UploadFile = File(...)):
    """
    上传数据文件接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 检查文件类型
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.csv', '.xls', '.xlsx']:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "不支持的文件类型，请上传CSV、XLS或XLSX格式的文件"
                }
            )
        
        # 生成唯一的文件名
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
        # 如果在处理过程中出现任何错误，确保清理临时文件
        if 'temp_file_name' in locals() and os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    # 在Electron环境中，使用127.0.0.1而不是0.0.0.0以确保安全连接
    uvicorn.run(app, host="127.0.0.1", port=8000)