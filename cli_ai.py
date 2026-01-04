#!/usr/bin/env python3
"""
CLI-AI: Terminal AI Assistant for Linux Commands
Helps Linux beginners execute commands using natural language
"""

import sys
import os

# Optional: colorama for colored terminal output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Define dummy color codes if colorama not available
    class ColorCodes:
        """Fallback color codes when colorama is not available"""
        pass
    
    Fore = type('Fore', (), {
        'GREEN': '', 'RED': '', 'YELLOW': '', 'BLUE': '',
        'CYAN': '', 'MAGENTA': '', 'WHITE': ''
    })()
    
    Style = type('Style', (), {
        'BRIGHT': '', 'RESET_ALL': ''
    })()

from nlp_parser import NLPParser
from command_executor import CommandExecutor


class CLIAI:
    """Main CLI-AI application"""
    
    def __init__(self):
        self.parser = NLPParser()
        self.executor = CommandExecutor()
        self.running = True
    
    def print_welcome(self):
        """Print welcome message"""
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("=" * 70)
        print("  CLI-AI: Terminal AI Assistant")
        print("  帮助 Linux 初学者使用自然语言执行命令")
        print("=" * 70)
        print(f"{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}使用说明:")
        print("  - 用中文或英文描述你想做的操作")
        print("  - 输入 'help' 查看常用命令")
        print("  - 输入 'history' 查看命令历史")
        print("  - 输入 'exit' 或 'quit' 退出程序")
        print(f"{Style.RESET_ALL}")
    
    def print_help(self):
        """Print help information with common command examples"""
        print(f"\n{Fore.CYAN}常用命令示例:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}系统管理:")
        print("  切换到管理员 / switch to administrator")
        print("  查看当前目录 / show current directory")
        print("  查看磁盘空间 / disk space")
        print("  查看内存使用 / memory usage")
        print(f"\n{Fore.GREEN}文件操作:")
        print("  列出文件 / list files")
        print("  创建文件夹 test / create folder test")
        print("  删除文件 test.txt / remove file test.txt")
        print("  查找文件 test.txt / find file test.txt")
        print("  查看文件内容 test.txt / show file test.txt")
        print(f"\n{Fore.GREEN}进程管理:")
        print("  查看进程 / show processes")
        print("  系统监控 / monitor system")
        print(f"\n{Fore.GREEN}网络:")
        print("  查看网络 / show ip")
        print("  ping测试 / test network")
        print(f"{Style.RESET_ALL}")
    
    def print_history(self):
        """Print command history"""
        history = self.executor.get_history_from_file(limit=20)
        if history:
            print(f"\n{Fore.CYAN}最近执行的命令:{Style.RESET_ALL}")
            for entry in history:
                print(f"  {entry.strip()}")
        else:
            print(f"{Fore.YELLOW}暂无命令历史{Style.RESET_ALL}")
    
    def confirm_execution(self, command):
        """
        Ask user to confirm command execution
        
        Args:
            command (str): Command to execute
            
        Returns:
            bool: True if user confirms
        """
        # Check if command is dangerous
        is_dangerous = self.executor.is_dangerous_command(command)
        
        if is_dangerous:
            print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  警告: 这是一个危险命令！{Style.RESET_ALL}")
            print(f"{Fore.RED}此命令可能会造成数据丢失或系统损坏！{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}我将执行命令: {Fore.WHITE}{Style.BRIGHT}{command}{Style.RESET_ALL}")
        
        while True:
            try:
                response = input(f"{Fore.CYAN}是否继续？(y/n): {Style.RESET_ALL}").strip().lower()
                if response in ['y', 'yes', '是', 'ok']:
                    return True
                elif response in ['n', 'no', '否', 'cancel']:
                    return False
                else:
                    print(f"{Fore.RED}请输入 y 或 n{Style.RESET_ALL}")
            except (EOFError, KeyboardInterrupt):
                print()
                return False
    
    def execute_command(self, command):
        """
        Execute a command and display results
        
        Args:
            command (str): Command to execute
        """
        # Check if command needs interactive mode
        is_interactive = self.executor.is_interactive_command(command)
        
        if is_interactive:
            print(f"{Fore.CYAN}执行交互式命令...{Style.RESET_ALL}")
        
        # Execute command
        result = self.executor.execute(command, interactive=is_interactive)
        
        # Display results
        if result['success']:
            if not is_interactive and result['output']:
                print(f"\n{Fore.GREEN}执行成功:{Style.RESET_ALL}")
                print(result['output'])
        else:
            print(f"\n{Fore.RED}执行失败:{Style.RESET_ALL}")
            if result['error']:
                print(f"{Fore.RED}{result['error']}{Style.RESET_ALL}")
            if result.get('return_code', -1) != 0:
                print(f"{Fore.RED}返回码: {result['return_code']}{Style.RESET_ALL}")
    
    def process_input(self, user_input):
        """
        Process user input and execute corresponding command
        
        Args:
            user_input (str): User's input
        """
        user_input = user_input.strip()
        
        if not user_input:
            return
        
        # Handle special commands
        if user_input.lower() in ['exit', 'quit', '退出']:
            self.running = False
            print(f"{Fore.CYAN}再见！{Style.RESET_ALL}")
            return
        
        if user_input.lower() in ['help', '帮助', 'h', '?']:
            self.print_help()
            return
        
        if user_input.lower() in ['history', '历史']:
            self.print_history()
            return
        
        # Parse natural language to command
        command = self.parser.parse(user_input)
        
        if command:
            # Confirm before execution
            if self.confirm_execution(command):
                self.execute_command(command)
            else:
                print(f"{Fore.YELLOW}已取消执行{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}抱歉，我不理解这个命令。{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}提示: 输入 'help' 查看常用命令示例{Style.RESET_ALL}")
    
    def run(self):
        """Main application loop"""
        self.print_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = input(f"\n{Fore.GREEN}{Style.BRIGHT}CLI-AI> {Style.RESET_ALL}")
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}使用 'exit' 退出程序{Style.RESET_ALL}")
            except EOFError:
                self.running = False
                print(f"\n{Fore.CYAN}再见！{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}错误: {str(e)}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    try:
        app = CLIAI()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
