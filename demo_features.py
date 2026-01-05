#!/usr/bin/env python3
"""
CLI-AI 功能演示
展示 AI 智能解析、错误分析和命令建议功能
"""
import os
import sys

# 设置测试环境变量（如果没有 .env 文件）
if not os.path.exists('.env'):
    print("=" * 70)
    print("演示模式：使用模拟 AI 功能")
    print("=" * 70)
    print("提示：要体验完整的 AI 功能，请配置 .env 文件\n")
    os.environ['AI_PROVIDER'] = 'deepseek'
    os.environ['DEEPSEEK_API_KEY'] = 'sk-demo-key'

from colorama import init, Fore, Style
init(autoreset=True)

from ai_command_parser import AICommandParser
from ai_error_analyzer import AIErrorAnalyzer, AICommandSuggester


def demo_ai_command_parser():
    """演示 AI 命令解析功能"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print("演示 1: AI 智能命令解析")
    print(f"{'=' * 70}{Style.RESET_ALL}\n")
    
    print("功能说明：")
    print("- AI 能够理解自然语言并转换为准确的 Linux 命令")
    print("- 支持中文和英文输入")
    print("- 自动清洗命令格式\n")
    
    try:
        parser = AICommandParser()
        
        # 测试用例
        test_cases = [
            ("列出所有文件", "中文 - 简单命令"),
            ("查看当前目录下所有文件的详细信息", "中文 - 复杂描述"),
            ("show disk usage", "英文 - 简单命令"),
            ("find all txt files in current directory", "英文 - 复杂查询"),
            ("创建一个名为 myproject 的文件夹", "中文 - 带参数"),
        ]
        
        print(f"{Fore.YELLOW}演示测试用例：{Style.RESET_ALL}\n")
        
        for i, (input_text, desc) in enumerate(test_cases, 1):
            print(f"{Fore.GREEN}{i}. {desc}{Style.RESET_ALL}")
            print(f"   输入：{input_text}")
            
            try:
                # 注意：这里会调用真实 API（如果配置了）
                # 否则会失败，这是正常的
                command = parser.parse_command(input_text)
                print(f"   {Fore.CYAN}→ AI 解析结果：{Style.BRIGHT}{command}{Style.RESET_ALL}")
            except Exception as e:
                print(f"   {Fore.YELLOW}⚠️  需要配置 API 密钥才能使用 AI 解析{Style.RESET_ALL}")
                print(f"   {Fore.YELLOW}   示例输出：ls -la{Style.RESET_ALL}")
                break
            print()
        
    except Exception as e:
        print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")


def demo_error_analyzer():
    """演示错误分析功能"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print("演示 2: AI 错误分析与修复建议")
    print(f"{'=' * 70}{Style.RESET_ALL}\n")
    
    print("功能说明：")
    print("- 自动分析命令执行错误的原因")
    print("- 提供具体的修复建议")
    print("- 生成替代命令供用户选择\n")
    
    try:
        analyzer = AIErrorAnalyzer()
        
        # 测试用例
        error_cases = [
            {
                'name': '权限不足错误',
                'command': 'cat /root/secret.txt',
                'error': 'cat: /root/secret.txt: Permission denied',
                'return_code': 1
            },
            {
                'name': '命令未找到',
                'command': 'invalidcmd',
                'error': 'bash: invalidcmd: command not found',
                'return_code': 127
            },
            {
                'name': '文件不存在',
                'command': 'cat nonexistent.txt',
                'error': 'cat: nonexistent.txt: No such file or directory',
                'return_code': 1
            },
        ]
        
        print(f"{Fore.YELLOW}演示错误分析：{Style.RESET_ALL}\n")
        
        for i, case in enumerate(error_cases, 1):
            print(f"{Fore.GREEN}{i}. {case['name']}{Style.RESET_ALL}")
            print(f"   命令：{case['command']}")
            print(f"   错误：{Fore.RED}{case['error']}{Style.RESET_ALL}")
            
            # 使用基础错误分析（不需要 API）
            result = analyzer._basic_error_analysis(
                case['command'],
                case['error'],
                case['return_code']
            )
            
            print(f"   {Fore.CYAN}分析：{result['analysis']}{Style.RESET_ALL}")
            print(f"   {Fore.CYAN}建议：{result['suggestion']}{Style.RESET_ALL}")
            if result['alternative_command']:
                print(f"   {Fore.GREEN}替代命令：{Style.BRIGHT}{result['alternative_command']}{Style.RESET_ALL}")
            print()
        
        print(f"{Fore.YELLOW}注意：配置 API 后可获得更智能的 AI 分析{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"{Fore.RED}错误：{e}{Style.RESET_ALL}")


def demo_command_suggester():
    """演示命令建议功能"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print("演示 3: 智能命令建议（自动模式）")
    print(f"{'=' * 70}{Style.RESET_ALL}\n")
    
    print("功能说明：")
    print("- 根据命令执行结果智能建议下一步操作")
    print("- 理解用户的工作流程")
    print("- 提供自然语言形式的建议\n")
    
    print(f"{Fore.YELLOW}演示场景：{Style.RESET_ALL}\n")
    
    scenarios = [
        {
            'command': 'mkdir myproject',
            'output': '',
            'success': True,
            'expected_suggestion': '进入刚创建的目录'
        },
        {
            'command': 'ls -la',
            'output': 'total 48\n-rw-r--r-- 1 user user 1234 Jan 5 file.txt\n...',
            'success': True,
            'expected_suggestion': '查看某个文件的内容'
        },
        {
            'command': 'df -h',
            'output': 'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   48G   2.0G  96% /',
            'success': True,
            'expected_suggestion': '清理磁盘空间或查找大文件'
        },
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{Fore.GREEN}{i}. 场景{Style.RESET_ALL}")
        print(f"   命令：{scenario['command']}")
        print(f"   状态：{'✓ 成功' if scenario['success'] else '✗ 失败'}")
        print(f"   {Fore.CYAN}预期建议：{scenario['expected_suggestion']}{Style.RESET_ALL}")
        print()
    
    print(f"{Fore.YELLOW}注意：自动建议功能需要配置 API 并启用 AUTO_CONTINUE_MODE{Style.RESET_ALL}\n")


def demo_configuration():
    """演示配置选项"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print("配置指南")
    print(f"{'=' * 70}{Style.RESET_ALL}\n")
    
    print("在 config.py 中配置 AI 功能：\n")
    
    print(f"{Fore.GREEN}1. AI 智能解析（推荐启用）{Style.RESET_ALL}")
    print("   USE_AI_PARSING = True")
    print("   # 使用 AI 模型解析自然语言，理解能力更强\n")
    
    print(f"{Fore.GREEN}2. AI 错误分析（推荐启用）{Style.RESET_ALL}")
    print("   AI_ERROR_ANALYSIS = True")
    print("   # 智能分析错误并提供修复建议\n")
    
    print(f"{Fore.GREEN}3. 自动建议模式（可选）{Style.RESET_ALL}")
    print("   AUTO_CONTINUE_MODE = False")
    print("   # 自动建议下一步操作，适合学习者\n")
    
    print("在 .env 中配置 API 密钥：\n")
    
    print(f"{Fore.CYAN}OpenAI 配置示例：{Style.RESET_ALL}")
    print("   AI_PROVIDER=openai")
    print("   OPENAI_API_KEY=sk-your-openai-key")
    print("   OPENAI_MODEL=gpt-4\n")
    
    print(f"{Fore.CYAN}DeepSeek 配置示例：{Style.RESET_ALL}")
    print("   AI_PROVIDER=deepseek")
    print("   DEEPSEEK_API_KEY=sk-your-deepseek-key")
    print("   DEEPSEEK_MODEL=deepseek-chat\n")
    
    print(f"{Fore.YELLOW}快速开始：{Style.RESET_ALL}")
    print("   cp .env.example .env")
    print("   # 编辑 .env 填入你的 API 密钥")
    print("   python3 cli_ai.py\n")


def main():
    """主函数"""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print("CLI-AI v2.2 功能演示")
    print("Terminal AI Assistant - Feature Demonstration")
    print(f"{'=' * 70}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}本演示将展示以下功能：{Style.RESET_ALL}")
    print("1. AI 智能命令解析")
    print("2. AI 错误分析与修复建议")
    print("3. 智能命令建议（自动模式）")
    print("4. 配置指南\n")
    
    input(f"{Fore.CYAN}按 Enter 键开始演示...{Style.RESET_ALL}")
    
    # 运行各个演示
    demo_ai_command_parser()
    input(f"\n{Fore.CYAN}按 Enter 键继续下一个演示...{Style.RESET_ALL}")
    
    demo_error_analyzer()
    input(f"\n{Fore.CYAN}按 Enter 键继续下一个演示...{Style.RESET_ALL}")
    
    demo_command_suggester()
    input(f"\n{Fore.CYAN}按 Enter 键查看配置指南...{Style.RESET_ALL}")
    
    demo_configuration()
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'=' * 70}")
    print("演示完成！")
    print(f"{'=' * 70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}下一步：{Style.RESET_ALL}")
    print("1. 配置 .env 文件以启用完整的 AI 功能")
    print("2. 运行 python3 cli_ai.py 开始使用")
    print("3. 查看 README.md 了解更多详情\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}演示已中断{Style.RESET_ALL}")
        sys.exit(0)
