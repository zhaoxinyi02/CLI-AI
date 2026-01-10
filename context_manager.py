"""
系统环境上下文管理器
System Environment Context Manager

用于收集系统上下文信息，包括：
- 当前工作目录 (pwd)
- 当前用户名 (whoami)
- 操作系统信息 (uname -s)
- 系统架构 (uname -m)
"""
import os
import subprocess
import platform
from typing import Dict, Optional


class ContextManager:
    """系统环境上下文管理器"""
    
    def __init__(self):
        """初始化上下文管理器"""
        self._context_cache: Optional[Dict[str, str]] = None
    
    def _execute_command(self, command: str) -> str:
        """
        执行系统命令并返回输出
        
        Args:
            command: 要执行的命令
            
        Returns:
            命令输出字符串（去除首尾空格）
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_current_directory(self) -> str:
        """
        获取当前工作目录
        
        Returns:
            当前工作目录的绝对路径
        """
        try:
            return os.getcwd()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_username(self) -> str:
        """
        获取当前用户名
        
        Returns:
            当前用户名
        """
        try:
            # 优先使用 os 模块获取用户名（更快）
            import getpass
            return getpass.getuser()
        except Exception:
            # 备用方案：使用 whoami 命令
            return self._execute_command("whoami")
    
    def get_os_name(self) -> str:
        """
        获取操作系统名称
        
        Returns:
            操作系统名称（如 Linux, Darwin, Windows）
        """
        try:
            # 使用 platform 模块获取 OS 名称
            return platform.system()
        except Exception:
            # 备用方案：使用 uname -s 命令
            return self._execute_command("uname -s")
    
    def get_architecture(self) -> str:
        """
        获取系统架构
        
        Returns:
            系统架构（如 x86_64, arm64, aarch64）
        """
        try:
            # 使用 platform 模块获取架构
            return platform.machine()
        except Exception:
            # 备用方案：使用 uname -m 命令
            return self._execute_command("uname -m")
    
    def get_context(self) -> Dict[str, str]:
        """
        获取完整的系统上下文信息
        
        Returns:
            包含所有上下文信息的字典
        """
        if self._context_cache is None:
            self._context_cache = {
                "current_directory": self.get_current_directory(),
                "username": self.get_username(),
                "os_name": self.get_os_name(),
                "architecture": self.get_architecture()
            }
        return self._context_cache
    
    def refresh_context(self) -> Dict[str, str]:
        """
        刷新并重新获取系统上下文信息
        
        Returns:
            包含所有上下文信息的字典
        """
        self._context_cache = None
        return self.get_context()
    
    def get_context_string(self) -> str:
        """
        获取格式化的上下文环境信息字符串
        
        Returns:
            格式化的上下文信息字符串，用于提供给 AI
        """
        context = self.get_context()
        
        context_string = f"""当前系统环境上下文:
- 工作目录: {context['current_directory']}
- 用户名: {context['username']}
- 操作系统: {context['os_name']}
- 系统架构: {context['architecture']}"""
        
        return context_string
    
    def get_context_for_ai(self) -> str:
        """
        获取适合 AI 使用的上下文信息字符串
        更简洁的格式，便于 AI 理解
        
        Returns:
            简洁格式的上下文信息
        """
        context = self.get_context()
        return (
            f"User: {context['username']}, "
            f"Dir: {context['current_directory']}, "
            f"OS: {context['os_name']}, "
            f"Arch: {context['architecture']}"
        )


if __name__ == "__main__":
    # 测试示例
    print("=" * 60)
    print("系统环境上下文管理器测试")
    print("System Context Manager Test")
    print("=" * 60)
    print()
    
    manager = ContextManager()
    
    # 测试单个方法
    print("单个方法测试:")
    print(f"当前目录: {manager.get_current_directory()}")
    print(f"用户名: {manager.get_username()}")
    print(f"操作系统: {manager.get_os_name()}")
    print(f"系统架构: {manager.get_architecture()}")
    print()
    
    # 测试获取完整上下文
    print("完整上下文 (字典):")
    context = manager.get_context()
    for key, value in context.items():
        print(f"  {key}: {value}")
    print()
    
    # 测试格式化输出
    print("格式化上下文字符串:")
    print(manager.get_context_string())
    print()
    
    # 测试 AI 格式输出
    print("AI 格式上下文字符串:")
    print(manager.get_context_for_ai())
    print()
    
    print("=" * 60)
    print("测试完成！")
    print("=" * 60)
