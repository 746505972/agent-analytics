# import os
# import asyncio
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
#
# async def test_qwen():
#     print("检查环境变量...")
#     api_key = os.getenv("DASHSCOPE_API_KEY")
#     print(f"DASHSCOPE_API_KEY 设置: {bool(api_key)}")
#
#     if not api_key:
#         print("错误: 未设置 DASHSCOPE_API_KEY 环境变量")
#         return
#
#     print("初始化模型...")
#     try:
#         model = ChatOpenAI(
#             api_key=api_key,
#             base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#             model="qwen-plus",
#         )
#         print("模型初始化成功")
#
#         print("发送测试消息...")
#         messages = [
#             SystemMessage(content="你是一个数据分析助手，帮助用户分析数据文件。"),
#             HumanMessage(content="你好，你是谁？")
#         ]
#
#         print("开始流式响应测试...")
#         async for chunk in model.astream(messages):
#             print(f"收到片段: {chunk.content}")
#
#         print("流式响应测试完成")
#
#     except Exception as e:
#         print(f"测试失败: {e}")
#         import traceback
#         traceback.print_exc()
#
# if __name__ == "__main__":
#     asyncio.run(test_qwen())