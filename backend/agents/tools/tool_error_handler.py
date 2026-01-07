import functools
import traceback

def tool_error_handler(func):
    """
    装饰器：将工具函数的异常转换为错误消息返回值
    这样工具执行错误不会中断整个agent执行流程
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f"工具执行错误: {str(e)}\n错误类型: {type(e).__name__}\n详细堆栈: {traceback.format_exc()}"
            # 返回错误信息作为正常结果，而不是抛出异常
            return {"error": str(e), "error_message": error_message, "success": False}
    return wrapper
