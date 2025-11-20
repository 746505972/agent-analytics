"""
Session数据清理工具
提供定期清理过期session数据的功能
"""

import os
import time
import shutil
from datetime import datetime, timedelta
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 数据目录
DATA_DIR = "data"

def clean_expired_sessions(expiration_hours: int = 10):
    """
    清理过期的session数据
    
    Args:
        expiration_hours (int): session过期时间（小时），默认10小时
    """
    try:
        if not os.path.exists(DATA_DIR):
            logger.info("数据目录不存在，无需清理")
            return
            
        # 计算过期时间点
        expiration_time = datetime.now() - timedelta(hours=expiration_hours)
        expiration_timestamp = expiration_time.timestamp()
        
        # 遍历数据目录中的所有session目录
        for item in os.listdir(DATA_DIR):
            item_path = os.path.join(DATA_DIR, item)
            
            # 检查是否为目录（session目录）
            if os.path.isdir(item_path):
                # 获取目录的修改时间
                dir_modified_time = os.path.getmtime(item_path)
                
                # 如果目录修改时间早于过期时间，则删除整个目录
                if dir_modified_time < expiration_timestamp:
                    try:
                        shutil.rmtree(item_path)
                        logger.info(f"已删除过期session目录: {item_path}")
                    except Exception as e:
                        logger.error(f"删除过期session目录失败 {item_path}: {e}")
                else:
                    logger.debug(f"Session目录未过期: {item_path}")
                    
    except Exception as e:
        logger.error(f"清理过期session时发生错误: {e}")

def clean_expired_sessions_and_files(expiration_hours: int = 10):
    """
    清理过期的session数据和文件
    
    Args:
        expiration_hours (int): session过期时间（小时），默认10小时
    """
    try:
        if not os.path.exists(DATA_DIR):
            logger.info("数据目录不存在，无需清理")
            return
            
        # 计算过期时间点
        expiration_time = datetime.now() - timedelta(hours=expiration_hours)
        expiration_timestamp = expiration_time.timestamp()
        
        # 遍历数据目录中的所有项目
        for item in os.listdir(DATA_DIR):
            item_path = os.path.join(DATA_DIR, item)
            
            # 如果是目录（session目录）
            if os.path.isdir(item_path):
                # 获取目录的修改时间
                dir_modified_time = os.path.getmtime(item_path)
                
                # 如果目录修改时间早于过期时间，则删除整个目录
                if dir_modified_time < expiration_timestamp:
                    try:
                        shutil.rmtree(item_path)
                        logger.info(f"已删除过期session目录: {item_path}")
                    except Exception as e:
                        logger.error(f"删除过期session目录失败 {item_path}: {e}")
                else:
                    logger.debug(f"Session目录未过期: {item_path}")
            # 如果是文件（非session目录下的文件）
            elif os.path.isfile(item_path):
                # 获取文件的修改时间
                file_modified_time = os.path.getmtime(item_path)
                
                # 如果文件修改时间早于过期时间，则删除文件
                if file_modified_time < expiration_timestamp:
                    try:
                        os.remove(item_path)
                        logger.info(f"已删除过期文件: {item_path}")
                    except Exception as e:
                        logger.error(f"删除过期文件失败 {item_path}: {e}")
                else:
                    logger.debug(f"文件未过期: {item_path}")
                    
    except Exception as e:
        logger.error(f"清理过期session和文件时发生错误: {e}")

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 执行清理任务
    clean_expired_sessions_and_files()