from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os
import pandas as pd
import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 尝试不同的导入方式
try:
    # 首先尝试相对导入
    from ..utils.file_manager import get_file_path, delete_file
except ImportError:
    try:
        # 如果相对导入失败，尝试绝对导入
        from utils.file_manager import get_file_path, delete_file
    except ImportError:
        # 最后尝试直接添加到路径并导入
        import sys
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, parent_dir)
        from utils.file_manager import get_file_path, delete_file

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/files")
async def get_user_files(request: Request):
    """
    获取用户上传的文件列表
    """
    # 获取session_id
    session_id = request.state.session_id
    try:
        # 构建用户目录路径
        user_dir = os.path.join("data", session_id)
        
        # 检查目录是否存在
        if not os.path.exists(user_dir):
            return JSONResponse(content={
                "success": True,
                "data": [],
                "session_id": session_id
            })
        
        # 获取目录中的所有CSV文件
        files = []
        for filename in os.listdir(user_dir):
            if filename.endswith(".csv"):
                file_path = os.path.join(user_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        # 获取文件信息
                        stat = os.stat(file_path)
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
                        
                        files.append({
                            "data_id": os.path.splitext(filename)[0],
                            "filename": filename,
                            "rows": len(df),
                            "columns": len(df.columns),
                            "size": stat.st_size,
                            "modified": stat.st_mtime
                        })
                    except Exception as e:
                        # 如果某个文件读取出错，跳过该文件
                        logger.error(f"读取文件 {filename} 时出错: {str(e)}")
                        continue
        
        return JSONResponse(content={
            "success": True,
            "data": files,
            "session_id": session_id
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
        )