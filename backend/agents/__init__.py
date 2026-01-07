from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os

class DataAnalysisAgent:
    """
    数据分析 Agent 类
    负责解析用户指令、调度分析工具、生成分析报告
    """
    
    def __init__(self):
        """
        初始化 Agent
        """
        self.tools = []
        self.agent = None
        self.setup_agent()
        self.system_message ="""
            你是一个专业的数据分析助手。你的任务是根据用户的问题，使用提供的工具来分析数据并给出专业的回答。
            
            你会收到以下信息：
            1. 数据上下文信息：包含当前正在分析的文件的相关信息，如文件名、行列数、列名等
            2. 用户问题：用户想要进行的具体分析任务
            
            请严格按照以下规则进行操作：
            1. 仔细区分数据上下文信息和用户问题，不要混淆两者
            2. 调用工具时一定要传入session_id          
            3. 根据用户问题，结合数据上下文信息，选择合适的工具进行分析
            4. 如果需要查看数据内容，可以使用文件读取工具
            5. 回答时要专业、清晰、有条理
            6. 在回答中主动提及当前分析的文件ID，让用户知道你了解上下文，但不要说出文件路径
            """
    
    def setup_agent(self):
        """
        设置 Agent，注册可用工具
        """
        # 初始化模型
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
            
        self.llm = ChatOpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model="qwen-plus"
        )
        
        # 注册各个模块的工具
        self.register_module_tools()
        
        # 创建agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools
        )
    
    def register_module_tools(self):
        """
        注册各模块提供的工具
        """
        # 导入各模块的注册函数
        from .tools.pandas_api import register_pandas_tools
        from .tools.ml_api import register_ml_tools
        from .tools.basic_api import register_builtin_tools
        
        # 注册各模块的工具
        register_builtin_tools(self)
        register_pandas_tools(self)
        register_ml_tools(self)
    # TODO: 实现流式响应(DONE) & 添加分析结果上下文
    async def process_query_stream(self, query: str, data_context=None, session_id=None):
        """
        流式处理用户查询
        
        Args:
            query (str): 用户的自然语言查询
            data_context: 当前数据上下文
            session_id: 用户会话ID
            
        Yields:
            dict: 处理过程中的流式响应
        """
        try:
            # 准备输入
            messages = []
            
            # 添加系统消息

            messages.append(SystemMessage(content=self.system_message))
            
            # 如果有数据上下文，则加入
            if data_context:
                # 构造更清晰的提示信息
                context_info = f"""
                    <数据上下文信息>
                    文件ID(data_id): {data_context.get('data_id', '未知')}
                    session_id: {session_id}
                    文件路径:{data_context.get('file_path', '未知')}
                    数据形状: {data_context.get('shape', '未知')} (行数, 列数)
                    列名: {', '.join(data_context.get('columns', []))}
                    数据类型: {data_context.get('dtypes', '未知')}
                    示例数据: {data_context.get('sample_data', '无')}
                    </数据上下文信息>
                    """
                # 移除了数据上下文信息的日志打印，以保护用户隐私
                messages.append(HumanMessage(content=context_info))
            
            # 添加用户问题
            messages.append(HumanMessage(content=f"<用户问题>{query}</用户问题>"))
            
            # 执行agent，传递session_id给工具
            config = {"recursion_limit": 50}
            if session_id:
                config["session_id"] = session_id

                async for token, metadata in self.agent.astream(
                        {"messages": messages},
                        config=config,
                        stream_mode="messages",
                ):
                    # if token.content:
                    #     print("========token:", token.content)
                    # 检查token是否包含工具调用
                    if hasattr(token, 'tool_calls') and token.tool_calls:
                        for tool_call in token.tool_calls:
                            tool_call_info = {
                                "name": tool_call["name"],
                                "args": tool_call["args"]
                            }
                            # 流式返回工具调用信息
                            yield {
                                'type': 'tool_calls',
                                'data': [tool_call_info]
                            }
                    
                    # 检查token是否包含内容
                    if hasattr(token, 'content') and token.content:
                        # 检查是否是工具执行结果（ToolMessage）
                        # 工具执行结果通常包含特定格式的内容，如错误或成功信息，或者包含tool_call_id
                        # 或者检查metadata中的节点信息
                        langgraph_node = metadata.get("langgraph_node", "") if metadata else ""
                        
                        # 如果是工具节点的输出，跳过不发送给前端
                        if langgraph_node == "tools":
                            continue
                        
                        # 如果内容是字典或列表（通常是工具执行结果），也跳过
                        if isinstance(token.content, (dict, list)):
                            continue
                        
                        # 检查是否是工具执行结果的其他标识
                        if isinstance(token.content, str) and ('error' in token.content.lower() or 'success' in token.content.lower()):
                            # 如果是错误信息，尝试让AI处理
                            continue  # 跳过直接返回错误内容，让AI处理
                        
                        yield {
                            'type': 'content',
                            'data': token.content
                        }
            
            # 发送结束标记
            yield {
                'type': 'end',
                'data': None
            }
        except Exception as e:
            import traceback
            error_info = f"处理查询时发生错误，请稍后重试。"
            print(f"处理查询时发生错误: {traceback.format_exc()}")
            yield {
                'type': 'error',
                'data': error_info
            }

    
    def generate_report(self, analysis_results):
        """
        根据分析结果生成报告
        
        Args:
            analysis_results (dict): 分析结果
            
        Returns:
            str: 生成的分析报告
        """
        # 构造报告生成提示
        prompt = f"""
        基于以下分析结果生成一份详细的分析报告：
        
        {analysis_results}
        
        请以清晰、专业的语言组织这份报告。
        """
        
        response = self.llm.invoke(prompt)
        return response.content
