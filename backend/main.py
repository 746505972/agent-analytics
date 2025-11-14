# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List, Dict
import os
import uuid

from utils.file_manager import upload_file, read_any_file

app = FastAPI(title="Agent-Analytics API", description="数据分析系统的后端API")

# 添加CORS中间件，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保数据目录存在
os.makedirs("data", exist_ok=True)

@app.get("/")
async def root():
    return {"message": "欢迎使用 Agent-Analytics API"}

@app.post("/upload")
async def upload_data_file(file: UploadFile = File(...)):
    """
    上传数据文件接口
    """
    try:
        # 生成唯一的文件名
        file_extension = os.path.splitext(file.filename)[1]
        temp_file_name = f"temp_{uuid.uuid4()}{file_extension}"
        
        # 保存上传的文件
        with open(temp_file_name, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 使用现有的文件管理器处理文件
        result = upload_file(temp_file_name)
        
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

@app.get("/data/{data_id}")
async def get_data_preview(data_id: str, page: int = 1, page_size: int = 10):
    """
    获取数据预览接口
    """
    try:
        file_path = f"data/{data_id}.csv"
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
async def get_data_info(data_id: str):
    """
    获取数据文件信息接口
    """
    try:
        file_path = f"data/{data_id}.csv"
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