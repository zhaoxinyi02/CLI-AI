"""
AI 命令解析器模块
将用户的自然语言输入转换为 Linux 命令
增强功能：
- 2.2.1: 系统环境上下文感知
- 2.2.2: 智能参数提取与验证
- 2.2.3: 场景化 Prompt 优化
"""
import os
import re
from typing import Optional, Dict, List, Tuple
from ai_provider import AIProvider
from context_manager import ContextManager


class AICommandParser:
    """AI 命令解析器（增强版）"""
    
    # 场景关键词映射（按优先级排序）
    SCENARIO_KEYWORDS = {
        # 优先级高的场景应该有更具体的关键词
        'network_operations': [
            '下载', '上传', '端口', 'ping', 'SSH', 'FTP', 'http', 'https', 'url',
            'network', 'download', 'upload', 'port', 'wget', 'curl', 'scp', 'ssh', 'ftp',
            'netstat', 'ifconfig', '网络', '连接', 'connect', '远程', 'remote'
        ],
        'system_management': [
            '进程', '用户', '组', '服务', '权限', '管理员', '启动', '停止', '重启',
            'process', 'user', 'group', 'service', 'permission', 'admin', 'sudo',
            'ps', 'top', 'kill', 'useradd', 'userdel', 'usermod', 'systemctl', 'chmod', 'chown',
            'start', 'stop', 'restart', '添加用户', '删除用户'
        ],
        'text_processing': [
            '查看', '编辑', '搜索', '替换', '文本', '内容', '行',
            'view', 'edit', 'search', 'replace', 'text', 'content', 'line',
            'cat', 'grep', 'sed', 'awk', 'nano', 'vi', 'vim', 'less', 'more', 'head', 'tail',
            '显示内容', '查看内容'
        ],
        'file_operations': [
            '创建', '删除', '复制', '移动', '重命名', '文件', '目录', '文件夹',
            'create', 'delete', 'remove', 'copy', 'move', 'rename', 'file', 'directory', 'folder',
            'mkdir', 'rm', 'cp', 'mv', 'touch', 'find', '查找', '压缩', '解压', 'tar', 'zip'
        ]
    }
    
    def __init__(self, prompt_file: str = "prompts/command_generation.txt", use_context: bool = True):
        """
        初始化 AI 命令解析器
        
        Args:
            prompt_file: 提示词模板文件路径（可以为 None，将自动选择场景）
            use_context: 是否使用系统上下文信息
        """
        self.ai_provider = AIProvider()
        self.prompt_file = prompt_file
        self.use_context = use_context
        self.context_manager = ContextManager() if use_context else None
        self.system_prompt = self._load_prompt() if prompt_file else None
    
    def _load_prompt(self, prompt_file: Optional[str] = None) -> str:
        """
        加载提示词模板
        
        Args:
            prompt_file: 提示词文件路径（可选）
        
        Returns:
            系统提示词字符串
        """
        file_to_load = prompt_file or self.prompt_file
        if not file_to_load:
            return self._get_default_prompt()
        
        try:
            with open(file_to_load, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # 如果文件不存在，使用默认提示词
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """获取默认提示词"""
        return """你是一个专业的 Linux 命令助手。将用户的自然语言描述转换为准确的 Linux 命令。
只返回命令本身，不要返回任何解释、说明或额外文字。
不要使用 markdown 代码块标记。"""
    
    def _detect_scenario(self, user_input: str) -> str:
        """
        检测用户输入的场景类型
        
        Args:
            user_input: 用户输入的自然语言
            
        Returns:
            场景类型：file_operations, system_management, network_operations, text_processing
            如果无法判断，返回 'command_generation'（默认场景）
        """
        user_input_lower = user_input.lower()
        
        # 特殊规则：优先级检测
        # 1. 如果包含 URL，很可能是网络操作
        if 'http://' in user_input_lower or 'https://' in user_input_lower or 'ftp://' in user_input_lower:
            return 'network_operations'
        
        # 2. 如果包含"用户"且包含"创建/添加/删除"，是系统管理
        if '用户' in user_input_lower or 'user' in user_input_lower:
            if any(word in user_input_lower for word in ['创建', '添加', '删除', 'create', 'add', 'delete', 'remove']):
                return 'system_management'
        
        # 3. 如果同时包含"编辑"和"文件"，优先文本处理
        if ('编辑' in user_input_lower or 'edit' in user_input_lower) and ('文件' in user_input_lower or 'file' in user_input_lower):
            if any(ext in user_input_lower for ext in ['.txt', '.log', '.conf', '.config', '.ini']):
                return 'text_processing'
        
        # 4. 如果包含"查看内容"或特定的查看命令，是文本处理
        if any(word in user_input_lower for word in ['查看内容', '显示内容', 'view content', 'show content', 'cat ', 'less ', 'more ']):
            return 'text_processing'
        
        # 统计每个场景的关键词匹配数
        scenario_scores = {}
        for scenario, keywords in self.SCENARIO_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword.lower() in user_input_lower)
            scenario_scores[scenario] = score
        
        # 找出得分最高的场景
        max_score = max(scenario_scores.values())
        if max_score > 0:
            # 返回得分最高的场景（按定义顺序，优先级高的会先返回）
            for scenario, score in scenario_scores.items():
                if score == max_score:
                    return scenario
        
        # 默认场景
        return 'command_generation'
    
    def _select_prompt_by_scenario(self, scenario: str) -> str:
        """
        根据场景选择合适的提示词模板
        
        Args:
            scenario: 场景类型
            
        Returns:
            对应场景的提示词内容
        """
        prompt_files = {
            'file_operations': 'prompts/file_operations.txt',
            'system_management': 'prompts/system_management.txt',
            'network_operations': 'prompts/network_operations.txt',
            'text_processing': 'prompts/text_processing.txt',
            'command_generation': 'prompts/command_generation.txt'
        }
        
        prompt_file = prompt_files.get(scenario, 'prompts/command_generation.txt')
        return self._load_prompt(prompt_file)
    
    def parse_command(self, user_input: str, auto_detect_scenario: bool = True) -> str:
        """
        将自然语言输入转换为 Linux 命令
        
        Args:
            user_input: 用户的自然语言输入（支持中英文）
            auto_detect_scenario: 是否自动检测场景并选择对应的提示词
            
        Returns:
            清洗后的 Linux 命令字符串
            
        Raises:
            ValueError: 如果输入为空或无效
            Exception: 如果 AI 调用失败
        """
        # 验证输入
        if not user_input or not user_input.strip():
            raise ValueError("输入不能为空")
        
        # 自动检测场景并选择提示词
        system_prompt = self.system_prompt
        if auto_detect_scenario:
            scenario = self._detect_scenario(user_input)
            system_prompt = self._select_prompt_by_scenario(scenario)
        
        # 如果没有系统提示词，使用默认的
        if not system_prompt:
            system_prompt = self._get_default_prompt()
        
        # 添加系统上下文信息
        if self.use_context and self.context_manager:
            context_info = self.context_manager.get_context_for_ai()
            system_prompt = f"{system_prompt}\n\n系统上下文: {context_info}"
        
        # 调用 AI 生成命令
        try:
            raw_response = self.ai_provider.generate_response(
                system_prompt=system_prompt,
                user_message=user_input.strip(),
                history=None,  # 单轮对话，不传递历史
                temperature=0.3,  # 使用较低温度以获得更确定的输出
                max_tokens=200  # 命令通常很短
            )
            
            # 清洗命令
            cleaned_command = self._clean_command(raw_response)
            
            # 验证清洗后的命令
            if not cleaned_command:
                raise ValueError("AI 返回了空命令")
            
            return cleaned_command
            
        except Exception as e:
            raise Exception(f"命令解析失败: {str(e)}")
    
    def _clean_command(self, raw_output: str) -> str:
        """
        清洗 AI 返回的命令
        去除 markdown 代码块标记、多余的解释文字，提取纯净的命令
        
        Args:
            raw_output: AI 返回的原始输出
            
        Returns:
            清洗后的命令字符串
        """
        if not raw_output:
            return ""
        
        command = raw_output.strip()
        
        # 去除 markdown 代码块标记
        # 匹配 ```bash\ncommand\n``` 或 ```\ncommand\n``` 格式
        code_block_pattern = r'^```(?:bash|sh|shell)?\s*\n?(.*?)\n?```$'
        match = re.search(code_block_pattern, command, re.DOTALL | re.MULTILINE)
        if match:
            command = match.group(1).strip()
        
        # 去除单独的反引号（如 `command`）
        if command.startswith('`') and command.endswith('`'):
            command = command[1:-1].strip()
        
        # 去除常见的解释性前缀
        # 例如："命令是：ls -la" -> "ls -la"
        prefixes = [
            r'^命令[是为][:：]\s*',
            r'^[Tt]he command is[:：]\s*',
            r'^[Cc]ommand[:：]\s*',
            r'^执行[:：]\s*',
            r'^[Rr]un[:：]\s*',
            r'^使用[:：]\s*',
            r'^[Uu]se[:：]\s*',
        ]
        for prefix in prefixes:
            command = re.sub(prefix, '', command, flags=re.IGNORECASE)
        
        # 只保留第一行（如果有多行）
        lines = command.split('\n')
        command = lines[0].strip()
        
        # 去除行尾的句号、逗号等标点
        command = re.sub(r'[。，、；.,:;]+$', '', command)
        
        # 基础格式检查：去除前导/尾随空格
        command = command.strip()
        
        return command
    
    def extract_parameters(self, user_input: str) -> Dict[str, List[str]]:
        """
        从用户输入中提取关键参数
        
        Args:
            user_input: 用户的自然语言输入
            
        Returns:
            包含提取参数的字典，键为参数类型，值为参数列表
        """
        params = {
            'files': [],
            'directories': [],
            'paths': [],
            'options': [],
            'numbers': []
        }
        
        # 提取文件名（带扩展名）
        file_pattern = r'\b[\w\-]+\.\w+\b'
        params['files'] = re.findall(file_pattern, user_input)
        
        # 提取路径（包含 / 或 ~）
        path_pattern = r'[~/][\w/\-\.]*'
        params['paths'] = re.findall(path_pattern, user_input)
        
        # 提取目录名（不带扩展名的词）
        # 这个比较简单，可能需要更复杂的逻辑
        
        # 提取数字
        number_pattern = r'\b\d+\b'
        params['numbers'] = re.findall(number_pattern, user_input)
        
        # 提取常见选项标志
        option_pattern = r'-{1,2}[\w\-]+'
        params['options'] = re.findall(option_pattern, user_input)
        
        return params
    
    def validate_parameters(self, command: str) -> Tuple[bool, List[str]]:
        """
        验证命令中的参数（主要是文件和路径）
        
        Args:
            command: 生成的命令字符串
            
        Returns:
            (是否全部有效, 警告信息列表)
        """
        warnings = []
        all_valid = True
        
        # 提取命令中的路径参数
        # 简单的正则匹配，可能不完美
        path_patterns = [
            r'(?:^|\s)([~/][\w/\-\.]+)',  # 绝对路径或 ~ 路径
            r'(?:^|\s)(\.{1,2}/[\w/\-\.]+)',  # 相对路径
            r'(?:^|\s)([\w\-]+\.\w+)(?:\s|$)',  # 文件名
        ]
        
        paths_to_check = []
        for pattern in path_patterns:
            matches = re.findall(pattern, command)
            paths_to_check.extend(matches)
        
        # 检查路径是否存在
        for path in paths_to_check:
            # 跳过一些特殊情况
            if path in ['.', '..', '/', '~']:
                continue
            
            # 扩展 ~ 为用户主目录
            expanded_path = os.path.expanduser(path)
            
            # 如果是相对路径，基于当前目录检查
            if not os.path.isabs(expanded_path):
                expanded_path = os.path.join(os.getcwd(), expanded_path)
            
            # 检查读取操作的文件/目录是否存在
            # 对于创建操作，不需要检查
            if not self._is_creation_command(command):
                if not os.path.exists(expanded_path):
                    warnings.append(f"路径不存在: {path}")
                    all_valid = False
        
        return all_valid, warnings
    
    def _is_creation_command(self, command: str) -> bool:
        """判断是否是创建操作的命令"""
        creation_keywords = ['mkdir', 'touch', 'create', '>', 'echo']
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in creation_keywords)
    
    def autocomplete_path(self, partial_path: str) -> str:
        """
        路径自动补全，将相对路径转换为绝对路径
        
        Args:
            partial_path: 部分路径或相对路径
            
        Returns:
            补全后的绝对路径
        """
        # 扩展 ~ 为用户主目录
        expanded = os.path.expanduser(partial_path)
        
        # 转换为绝对路径
        if not os.path.isabs(expanded):
            expanded = os.path.abspath(expanded)
        
        # 规范化路径（去除 . 和 ..）
        normalized = os.path.normpath(expanded)
        
        return normalized
    
    def get_scenario_info(self, user_input: str) -> Dict[str, str]:
        """
        获取场景检测信息
        
        Args:
            user_input: 用户输入
            
        Returns:
            包含场景类型和提示词文件的字典
        """
        scenario = self._detect_scenario(user_input)
        prompt_files = {
            'file_operations': 'prompts/file_operations.txt',
            'system_management': 'prompts/system_management.txt',
            'network_operations': 'prompts/network_operations.txt',
            'text_processing': 'prompts/text_processing.txt',
            'command_generation': 'prompts/command_generation.txt'
        }
        
        return {
            'scenario': scenario,
            'prompt_file': prompt_files.get(scenario, 'prompts/command_generation.txt')
        }


if __name__ == "__main__":
    # 简单的测试示例
    print("=" * 60)
    print("AI 命令解析器增强功能测试")
    print("=" * 60)
    print()
    
    try:
        # 设置测试环境变量
        os.environ.setdefault("AI_PROVIDER", "deepseek")
        os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
        
        parser = AICommandParser()
        
        # 测试场景检测
        print("1. 测试场景检测:")
        test_inputs = [
            "创建文件夹 test",
            "查看所有进程",
            "下载文件 http://example.com/file.zip",
            "查看文件 test.txt 的内容"
        ]
        
        for input_text in test_inputs:
            scenario_info = parser.get_scenario_info(input_text)
            print(f"   输入: {input_text}")
            print(f"   场景: {scenario_info['scenario']}")
            print(f"   提示词文件: {scenario_info['prompt_file']}")
            print()
        
        # 测试参数提取
        print("2. 测试参数提取:")
        test_inputs = [
            "复制文件 test.txt 到 backup.txt",
            "创建目录 /home/user/projects",
            "删除 file1.txt file2.txt 和 file3.txt",
            "查看文件 log.txt 的最后 20 行"
        ]
        
        for input_text in test_inputs:
            params = parser.extract_parameters(input_text)
            print(f"   输入: {input_text}")
            print(f"   提取的参数: {params}")
            print()
        
        # 测试路径补全
        print("3. 测试路径自动补全:")
        test_paths = [
            ".",
            "..",
            "./test",
            "~/documents",
            "test.txt"
        ]
        
        for path in test_paths:
            completed = parser.autocomplete_path(path)
            print(f"   输入: {path}")
            print(f"   补全: {completed}")
            print()
        
        # 测试系统上下文
        print("4. 测试系统上下文:")
        if parser.context_manager:
            context = parser.context_manager.get_context_for_ai()
            print(f"   上下文信息: {context}")
        else:
            print("   上下文管理器未启用")
        print()
        
        print("=" * 60)
        print("基础功能测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

