# main.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List, Dict
import os
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

from utils.file_manager import upload_file, read_any_file, delete_file, get_file_path
from routers.chat import router as chat_router

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

@app.get("/user/files")
async def get_user_files(request: Request):
    """
    获取用户上传的文件列表
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建用户目录路径
        user_dir = os.path.join("data", session_id)
        
        # 检查目录是否存在
        if not os.path.exists(user_dir):
            return JSONResponse(content={
                "success": True,
                "data": []
            })
        
        # 获取目录中的所有CSV文件
        files = []
        for filename in os.listdir(user_dir):
            if filename.endswith(".csv"):
                file_path = os.path.join(user_dir, filename)
                if os.path.isfile(file_path):
                    # 获取文件信息
                    stat = os.stat(file_path)
                    df = pd.read_csv(file_path, encoding="utf-8-sig")
                    
                    files.append({
                        "data_id": os.path.splitext(filename)[0],
                        "filename": filename,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "size": stat.st_size,
                        "modified": stat.st_mtime
                    })
        
        return JSONResponse(content={
            "success": True,
            "data": files
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

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

@app.delete("/data/{data_id}")
async def delete_data(request: Request, data_id: str):
    """
    删除数据文件接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        logger.info(f"尝试删除数据文件: {data_id}, session_id: {session_id}")
        
        # 删除文件时检查session_id
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            logger.warning(f"尝试删除不存在的文件: {file_path}")
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 删除文件
        delete_file(data_id, session_id)
        logger.info(f"数据文件删除成功: {data_id}")
        
        return JSONResponse(content={
            "success": True,
            "message": "数据文件删除成功"
        })
    except Exception as e:
        logger.error(f"删除数据文件时出错: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.get("/data/{data_id}")
async def get_data_preview(request: Request, data_id: str, page: int = 1, page_size: int = 10):
    """
    获取数据预览接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建文件路径
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 读取CSV文件
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        
        # 计算分页信息
        total_rows = len(df)
        total_pages = (total_rows + page_size - 1) // page_size
        
        # 获取当前页数据
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_data = df.iloc[start_idx:end_idx]
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "data_id": data_id,
                "columns": list(df.columns),
                "rows": total_rows,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "data": page_data.replace({pd.NA: None, pd.NaT: None}).to_dict('records')
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.get("/data/{data_id}/info")
async def get_data_info(request: Request, data_id: str):
    """
    获取数据文件信息接口
    """
    try:
        # 获取session_id
        session_id = request.state.session_id
        
        # 构建文件路径
        file_path = get_file_path(data_id, session_id)
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "数据文件不存在"
                }
            )
        
        # 读取CSV文件
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "data_id": data_id,
                "filename": f"{data_id}.csv",
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)