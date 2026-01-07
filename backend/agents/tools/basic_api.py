import os

from langchain_core.tools import tool
from .tool_error_handler import tool_error_handler

def register_builtin_tools(self):
    """
    注册内置工具
    """
    # 导入文件管理工具
    from utils.file_manager import read_any_file, get_file_path, upload_file, delete_file

    # 注册文件读取工具
    @tool
    @tool_error_handler
    def read_file(file_path: str, n: int = 10) -> dict:
        """
        读取文件的前n行数据
        Args:
        file_path (str): 文件路径
        n (int): 行数，默认为10
        """
        return read_any_file(file_path).head(n).to_dict()

    self.tools.append(read_file)

    # 注册文件删除工具
    @tool
    @tool_error_handler
    def delete_file_tool(data_id: str, session_id: str = None) -> None:
        """
        删除指定的数据文件
        Args:
        data_id (str): 文件ID
        session_id (str): session_id
        """
        return delete_file(data_id, session_id)

    self.tools.append(delete_file_tool)

    # 注册获取用户文件列表工具
    @tool
    @tool_error_handler
    def list_user_files(session_id: str = None) -> list:
        """
        获取用户上传的文件列表
        Args:
        session_id (str): session_id
        """
        # 如果没有提供session_id，返回空列表
        if not session_id:
            return []

        # 导入并调用获取用户文件列表的函数
        try:
            from routers.data import get_user_files_list
            return get_user_files_list(session_id)
        except Exception as e:
            # 如果出现错误，返回空列表
            return []

    self.tools.append(list_user_files)

    # 注册添加标题行工具
    @tool
    @tool_error_handler
    def add_header_row_tool(file_path: str, column_names: list, session_id: str = None) -> dict:
        """
        为没有标题行的文件添加标题行并创建新文件
        Args:
        file_path (str): 文件路径
        column_names (list): 列名列表
        session_id: session_id
        """
        from utils.file_manager import add_header_to_file, get_file_path

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        return add_header_to_file(file_path, column_names, session_id, mode="add")

    self.tools.append(add_header_row_tool)

    # 注册修改标题行工具
    @tool
    @tool_error_handler
    def modify_header_row_tool(file_path: str, column_names: list, session_id: str = None) -> dict:
        """
        修改文件的现有标题行并创建新文件
        Args:
        file_path (str): 文件路径
        column_names (list): 新的列名列表
        session_id: session_id
        """
        from utils.file_manager import add_header_to_file, get_file_path

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        return add_header_to_file(file_path, column_names, session_id, mode="modify")

    self.tools.append(modify_header_row_tool)

    # 注册删除首行工具
    @tool
    @tool_error_handler
    def remove_first_row_tool(file_path: str, session_id: str = None) -> dict:
        """
        删除文件的第一行（通常是有问题的标题行）并创建新文件
        Args:
        file_path (str): 文件路径
        session_id: session_id
        """
        from utils.file_manager import add_header_to_file, get_file_path

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        return add_header_to_file(file_path, [], session_id, mode="remove")

    self.tools.append(remove_first_row_tool)

    # 注册删除列工具
    @tool
    @tool_error_handler
    def delete_columns_tool(file_path: str, columns_to_delete: list, session_id: str = None) -> dict:
        """
        删除文件中的指定列并创建新文件
        Args:
        file_path (str): 文件路径
        columns_to_delete (list): 要删除的列名列表
        session_id (str): session_id
        """
        from utils.file_manager import delete_columns, get_file_path

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")

        return delete_columns(file_path, columns_to_delete, session_id)

    self.tools.append(delete_columns_tool)
