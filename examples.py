#!/usr/bin/env python3
"""
Example usage of CLI-AI components
This file demonstrates how to use the CLI-AI modules programmatically
"""

from nlp_parser import NLPParser
from command_executor import CommandExecutor

def example_basic_usage():
    """Example: Basic usage of NLP parser and command executor"""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    
    # Initialize components
    parser = NLPParser()
    executor = CommandExecutor()
    
    # Parse natural language input
    user_input = "查看当前目录"
    print(f"\nUser input: '{user_input}'")
    
    command = parser.parse(user_input)
    print(f"Parsed command: {command}")
    
    if command:
        # Execute the command
        result = executor.execute(command, interactive=False)
        
        if result['success']:
            print(f"✅ Success!")
            print(f"Output: {result['output'].strip()}")
        else:
            print(f"❌ Failed!")
            print(f"Error: {result['error']}")


def example_safety_check():
    """Example: Checking for dangerous commands"""
    print("\n" + "=" * 70)
    print("Example 2: Safety Check")
    print("=" * 70)
    
    executor = CommandExecutor()
    
    commands = [
        "pwd",
        "ls -la",
        "rm -rf /",
        "rm -rf *"
    ]
    
    for cmd in commands:
        is_dangerous = executor.is_dangerous_command(cmd)
        status = "⚠️  DANGEROUS" if is_dangerous else "✅ SAFE"
        print(f"\n{status}: {cmd}")


def example_interactive_detection():
    """Example: Detecting interactive commands"""
    print("\n" + "=" * 70)
    print("Example 3: Interactive Command Detection")
    print("=" * 70)
    
    executor = CommandExecutor()
    
    commands = [
        "sudo su",
        "nano test.txt",
        "top",
        "pwd",
        "ls -la"
    ]
    
    for cmd in commands:
        is_interactive = executor.is_interactive_command(cmd)
        mode = "🔄 Interactive" if is_interactive else "📝 Non-interactive"
        print(f"\n{mode}: {cmd}")


def example_custom_mapping():
    """Example: Adding custom command mappings"""
    print("\n" + "=" * 70)
    print("Example 4: Custom Command Mapping")
    print("=" * 70)
    
    parser = NLPParser()
    
    # Add a custom mapping
    parser.add_custom_mapping("我的自定义命令", "echo 'This is my custom command'")
    parser.add_custom_mapping("show system uptime", "uptime")
    
    # Test the custom mappings
    test_inputs = [
        "我的自定义命令",
        "show system uptime"
    ]
    
    for user_input in test_inputs:
        command = parser.parse(user_input)
        print(f"\nInput: '{user_input}'")
        print(f"Command: {command}")


def example_with_parameters():
    """Example: Commands with parameters"""
    print("\n" + "=" * 70)
    print("Example 5: Commands with Parameters")
    print("=" * 70)
    
    parser = NLPParser()
    
    test_inputs = [
        "创建文件夹 myproject",
        "删除文件 old_file.txt",
        "查找文件 config.py",
        "查看文件内容 README.md",
        "create folder newdir",
        "remove file temp.txt"
    ]
    
    for user_input in test_inputs:
        command = parser.parse(user_input)
        print(f"\nInput: '{user_input}'")
        print(f"Command: {command}")


def example_bilingual_support():
    """Example: Bilingual (Chinese/English) support"""
    print("\n" + "=" * 70)
    print("Example 6: Bilingual Support")
    print("=" * 70)
    
    parser = NLPParser()
    
    # Test Chinese and English equivalents
    test_pairs = [
        ("查看当前目录", "show current directory"),
        ("列出文件", "list files"),
        ("查看磁盘空间", "disk space"),
        ("查看内存使用", "memory usage"),
        ("查看进程", "show processes")
    ]
    
    for chinese, english in test_pairs:
        cmd_cn = parser.parse(chinese)
        cmd_en = parser.parse(english)
        
        match = "✅" if cmd_cn == cmd_en else "❌"
        print(f"\n{match} Chinese: '{chinese}' → {cmd_cn}")
        print(f"   English: '{english}' → {cmd_en}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "CLI-AI Examples" + " " * 33 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    example_basic_usage()
    example_safety_check()
    example_interactive_detection()
    example_custom_mapping()
    example_with_parameters()
    example_bilingual_support()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
