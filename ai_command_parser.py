"""
AI 命令解析器模块
将用户的自然语言输入转换为 Linux 命令
"""
import os
import re
from typing import Optional
from ai_provider import AIProvider


class AICommandParser:
    """AI 命令解析器"""
    
    def __init__(self, prompt_file: str = "prompts/command_generation.txt"):
        """
        初始化 AI 命令解析器
        
        Args:
            prompt_file: 提示词模板文件路径
        """
        self.ai_provider = AIProvider()
        self.prompt_file = prompt_file
        self.system_prompt = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """
        加载提示词模板
        
        Returns:
            系统提示词字符串
        """
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # 如果文件不存在，使用默认提示词
            return """你是一个专业的 Linux 命令助手。将用户的自然语言描述转换为准确的 Linux 命令。
只返回命令本身，不要返回任何解释、说明或额外文字。
不要使用 markdown 代码块标记。"""
    
    def parse_command(self, user_input: str) -> str:
        """
        将自然语言输入转换为 Linux 命令
        
        Args:
            user_input: 用户的自然语言输入（支持中英文）
            
        Returns:
            清洗后的 Linux 命令字符串
            
        Raises:
            ValueError: 如果输入为空或无效
            Exception: 如果 AI 调用失败
        """
        # 验证输入
        if not user_input or not user_input.strip():
            raise ValueError("输入不能为空")
        
        # 调用 AI 生成命令
        try:
            raw_response = self.ai_provider.generate_response(
                system_prompt=self.system_prompt,
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


if __name__ == "__main__":
    # 简单的测试示例
    try:
        parser = AICommandParser()
        
        # 测试中文输入
        print("测试中文输入:")
        cmd = parser.parse_command("列出所有文件")
        print(f"输入: 列出所有文件")
        print(f"输出: {cmd}\n")
        
        # 测试英文输入
        print("测试英文输入:")
        cmd = parser.parse_command("show disk usage")
        print(f"输入: show disk usage")
        print(f"输出: {cmd}\n")
        
    except Exception as e:
        print(f"错误: {e}")
