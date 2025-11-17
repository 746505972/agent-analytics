"""
LLM-Agent 核心模块
使用 LangChain 为核心，负责协调各分析模块，处理自然语言指令，生成分析报告
"""

from langgraph.prebuilt import create_react_agent
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
        
        # 注册内置工具
        self.register_builtin_tools()
        
        # 注册各个模块的工具
        self.register_module_tools()
        
        # 创建agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools
        )
    
    def register_builtin_tools(self):
        """
        注册内置工具
        """
        # 导入文件管理工具
        from utils.file_manager import read_any_file, get_file_path, upload_file, delete_file
        
        # 注册文件读取工具
        @tool
        def read_file(file_path: str) -> dict:
            """读取CSV/Excel文件的前10行数据，参数为文件路径"""
            return read_any_file(file_path).head(10).to_dict()
        
        self.tools.append(read_file)
        
        # 注册获取文件路径工具
        @tool
        def get_file_path_tool(data_id: str, session_id: str = None) -> str:
            """根据data_id获取文件完整路径，参数为data_id和可选的session_id"""
            return get_file_path(data_id, session_id)
        
        self.tools.append(get_file_path_tool)
        
        # 注册文件上传工具
        @tool
        def upload_file_tool(file_path: str, original_filename: str = None, session_id: str = None) -> dict:
            """上传文件，参数为文件路径、原始文件名和可选的session_id"""
            return upload_file(file_path, original_filename, session_id)
        
        self.tools.append(upload_file_tool)
        
        # 注册文件删除工具
        @tool
        def delete_file_tool(data_id: str, session_id: str = None) -> None:
            """删除指定的数据文件，参数为data_id和可选的session_id"""
            return delete_file(data_id, session_id)
        
        self.tools.append(delete_file_tool)
    
    def register_module_tools(self):
        """
        注册各模块提供的工具
        """
        # 导入各模块的注册函数
        from tools.pandas_api import register_pandas_tools
        from tools.nlp_api import register_nlp_tools
        from tools.ml_api import register_ml_tools
        from tools.visualization import register_visualization_tools
        
        # 注册各模块的工具
        register_pandas_tools(self)
        register_nlp_tools(self)
        register_ml_tools(self)
        register_visualization_tools(self)
    
    def process_query(self, query: str, data_context=None):
        """
        处理用户查询
        
        Args:
            query (str): 用户的自然语言查询
            data_context: 当前数据上下文
            
        Returns:
            dict: 处理结果和响应
        """
        try:
            # 准备输入
            messages = []
            
            # 添加系统消息
            system_message = """
你是一个专业的数据分析助手。你的任务是根据用户的问题，使用提供的工具来分析数据并给出专业的回答。

你会收到以下信息：
1. 数据上下文信息：包含当前正在分析的文件的相关信息，如文件名、行列数、列名等
2. 用户问题：用户想要进行的具体分析任务

请严格按照以下规则进行操作：
1. 仔细区分数据上下文信息和用户问题，不要混淆两者
2. 根据用户问题，结合数据上下文信息，选择合适的工具进行分析
3. 如果需要查看数据内容，可以使用文件读取工具
4. 回答时要专业、清晰、有条理
5. 如果用户询问你是否知道当前选择的文件，你应该明确告知用户你了解当前正在分析哪个文件
6. 在回答中主动提及当前分析的文件，让用户知道你了解上下文
"""
            messages.append(SystemMessage(content=system_message))
            
            # 如果有数据上下文，则加入
            if data_context:
                # 构造更清晰的提示信息
                context_info = f"""
<数据上下文信息>
文件ID: {data_context.get('data_id', '未知')}
文件名: {data_context.get('filename', '未知')}
数据形状: {data_context.get('shape', '未知')} (行数, 列数)
列名: {', '.join(data_context.get('columns', []))}
数据类型: {data_context.get('dtypes', '未知')}
示例数据: {data_context.get('sample_data', '无')}
</数据上下文信息>
"""
                messages.append(HumanMessage(content=context_info))
            
            # 添加用户问题
            messages.append(HumanMessage(content=f"<用户问题>{query}</用户问题>"))
            
            # 执行agent
            result = self.agent.invoke({"messages": messages})
            
            # 获取最后一条消息作为输出
            output = result['messages'][-1].content
            
            return {
                'query': query,
                'result': output,
                'status': 'success'
            }
        except Exception as e:
            return {
                'query': query,
                'result': f"处理查询时发生错误: {str(e)}",
                'status': 'error'
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
    
    def register_tool(self, tool_func, tool_name, tool_description):
        """
        注册分析工具
        
        Args:
            tool_func: 工具函数
            tool_name (str): 工具名称
            tool_description (str): 工具描述
        """
        # 使用装饰器创建工具
        decorated_tool = tool(tool_func)
        decorated_tool.name = tool_name
        decorated_tool.description = tool_description
        self.tools.append(decorated_tool)