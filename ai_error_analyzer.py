"""
AI 错误分析器模块
使用 AI 分析命令执行错误并提供解决方案
"""
import os
from typing import Dict, Optional
from ai_provider import AIProvider


class AIErrorAnalyzer:
    """AI 错误分析器"""
    
    def __init__(self):
        """初始化 AI 错误分析器"""
        self.ai_provider = None
        self._init_ai_provider()
    
    def _init_ai_provider(self):
        """初始化 AI 提供商，如果失败则不使用 AI"""
        try:
            self.ai_provider = AIProvider()
        except Exception as e:
            print(f"⚠️  AI 提供商初始化失败: {e}")
            print("   错误分析将使用基础模式")
            self.ai_provider = None
    
    def analyze_error(self, command: str, error_output: str, return_code: int) -> Dict[str, str]:
        """
        分析命令执行错误
        
        Args:
            command: 执行的命令
            error_output: 错误输出
            return_code: 返回码
            
        Returns:
            包含分析结果的字典：
            {
                'analysis': 错误原因分析,
                'suggestion': 建议的解决方案,
                'alternative_command': 可选的替代命令（如果有）
            }
        """
        if not self.ai_provider:
            return self._basic_error_analysis(command, error_output, return_code)
        
        try:
            # 构建分析提示词
            system_prompt = """你是一个 Linux 系统专家。你的任务是分析命令执行错误并提供解决方案。

分析错误时请：
1. 简明扼要地说明错误原因（1-2句话）
2. 提供具体的解决方案
3. 如果需要，提供替代命令

请用中文回复，格式如下：
原因：[错误原因]
解决方案：[具体步骤]
替代命令：[如果有替代命令就提供，没有就写"无"]"""

            user_message = f"""命令：{command}
错误输出：{error_output}
返回码：{return_code}

请分析这个错误并提供解决方案。"""

            # 调用 AI 分析
            response = self.ai_provider.generate_response(
                system_prompt=system_prompt,
                user_message=user_message,
                temperature=0.3,
                max_tokens=500
            )
            
            # 解析响应
            return self._parse_ai_response(response)
            
        except Exception as e:
            print(f"⚠️  AI 错误分析失败: {e}")
            return self._basic_error_analysis(command, error_output, return_code)
    
    def _parse_ai_response(self, response: str) -> Dict[str, str]:
        """解析 AI 响应"""
        result = {
            'analysis': '',
            'suggestion': '',
            'alternative_command': ''
        }
        
        lines = response.split('\n')
        current_key = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('原因：') or line.startswith('原因:'):
                current_key = 'analysis'
                result['analysis'] = line.replace('原因：', '').replace('原因:', '').strip()
            elif line.startswith('解决方案：') or line.startswith('解决方案:'):
                current_key = 'suggestion'
                result['suggestion'] = line.replace('解决方案：', '').replace('解决方案:', '').strip()
            elif line.startswith('替代命令：') or line.startswith('替代命令:'):
                current_key = 'alternative_command'
                alt_cmd = line.replace('替代命令：', '').replace('替代命令:', '').strip()
                if alt_cmd != '无' and alt_cmd.lower() != 'none':
                    result['alternative_command'] = alt_cmd
            elif current_key and line:
                # 继续追加到当前字段
                result[current_key] += ' ' + line
        
        # 如果解析失败，返回原始响应
        if not result['analysis'] and not result['suggestion']:
            result['analysis'] = response
        
        return result
    
    def _basic_error_analysis(self, command: str, error_output: str, return_code: int) -> Dict[str, str]:
        """基础错误分析（不使用 AI）"""
        result = {
            'analysis': '',
            'suggestion': '',
            'alternative_command': ''
        }
        
        error_lower = error_output.lower()
        
        # 常见错误模式匹配
        if 'permission denied' in error_lower or '权限' in error_output:
            result['analysis'] = '权限不足'
            result['suggestion'] = '尝试使用 sudo 运行命令'
            if not command.startswith('sudo'):
                result['alternative_command'] = f'sudo {command}'
        
        elif 'command not found' in error_lower or '未找到命令' in error_output:
            result['analysis'] = '命令未找到'
            result['suggestion'] = '请检查命令是否正确，或需要安装相应软件包'
        
        elif 'no such file or directory' in error_lower or '没有那个文件' in error_output:
            result['analysis'] = '文件或目录不存在'
            result['suggestion'] = '请检查文件路径是否正确'
        
        elif 'already exists' in error_lower or '已存在' in error_output:
            result['analysis'] = '文件或目录已存在'
            result['suggestion'] = '使用不同的名称，或先删除/重命名现有文件'
            # 检查是否是 mkdir 命令
            if command.startswith('mkdir'):
                folder_name = command.replace('mkdir', '').strip().split()[0]
                result['alternative_command'] = f'rm -rf {folder_name} && {command}'
        
        else:
            result['analysis'] = f'命令执行失败，返回码: {return_code}'
            result['suggestion'] = '请检查命令参数和权限'
        
        return result


class AICommandSuggester:
    """AI 命令建议器 - 建议下一步操作"""
    
    def __init__(self):
        """初始化 AI 命令建议器"""
        self.ai_provider = None
        self._init_ai_provider()
    
    def _init_ai_provider(self):
        """初始化 AI 提供商"""
        try:
            self.ai_provider = AIProvider()
        except Exception as e:
            print(f"⚠️  AI 提供商初始化失败: {e}")
            self.ai_provider = None
    
    def suggest_next_command(self, command: str, output: str, success: bool) -> Optional[str]:
        """
        根据命令执行结果建议下一步操作
        
        Args:
            command: 已执行的命令
            output: 命令输出
            success: 是否执行成功
            
        Returns:
            建议的下一个命令（自然语言描述），如果没有建议则返回 None
        """
        if not self.ai_provider:
            return None
        
        try:
            system_prompt = """你是一个 Linux 助手。根据用户刚执行的命令和结果，建议一个合理的下一步操作。

规则：
1. 只在有明确后续操作时才建议，不要强行建议
2. 建议应该是自然的工作流延续
3. 用一句简短的自然语言描述建议（不要返回具体命令）
4. 如果没有明确的后续操作，返回"无"

例如：
- 如果用户创建了文件夹，可能想进入该文件夹
- 如果用户列出了文件，可能想查看某个文件
- 如果用户查看了磁盘空间发现空间不足，可能想清理
- 如果命令失败，建议修复或查看更多信息"""

            status = "成功" if success else "失败"
            user_message = f"""命令：{command}
状态：{status}
输出：{output[:500]}

请建议下一步操作（用自然语言描述，或返回"无"）。"""

            response = self.ai_provider.generate_response(
                system_prompt=system_prompt,
                user_message=user_message,
                temperature=0.5,
                max_tokens=200
            )
            
            response = response.strip()
            if response and response != '无' and response.lower() != 'none':
                return response
            
        except Exception as e:
            # 建议功能不应中断主流程
            # 可以考虑添加日志记录
            pass
        
        return None


if __name__ == "__main__":
    # 测试错误分析器
    print("测试 AI 错误分析器\n")
    
    analyzer = AIErrorAnalyzer()
    
    # 测试案例
    test_command = "cat /root/secret.txt"
    test_error = "cat: /root/secret.txt: Permission denied"
    test_return_code = 1
    
    print(f"命令: {test_command}")
    print(f"错误: {test_error}")
    print(f"返回码: {test_return_code}\n")
    
    result = analyzer.analyze_error(test_command, test_error, test_return_code)
    
    print("分析结果:")
    print(f"原因: {result['analysis']}")
    print(f"建议: {result['suggestion']}")
    if result['alternative_command']:
        print(f"替代命令: {result['alternative_command']}")
