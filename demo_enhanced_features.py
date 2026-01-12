#!/usr/bin/env python3
"""
演示增强功能 (Features 2.2.1 - 2.2.3)
Demo Enhanced Features
"""
import os
from context_manager import ContextManager
from ai_command_parser import AICommandParser


def demo_context_manager():
    """演示 2.2.1: 系统环境上下文感知"""
    print("=" * 70)
    print("功能 2.2.1: 系统环境上下文感知")
    print("System Environment Context Awareness")
    print("=" * 70)
    print()
    
    manager = ContextManager()
    
    print("1. 获取系统上下文信息:")
    context = manager.get_context()
    for key, value in context.items():
        print(f"   {key:20s}: {value}")
    print()
    
    print("2. 格式化上下文字符串:")
    print(manager.get_context_string())
    print()
    
    print("3. AI 格式上下文字符串:")
    print(f"   {manager.get_context_for_ai()}")
    print()


def demo_scenario_detection():
    """演示 2.2.3: 场景化 Prompt 优化"""
    print("=" * 70)
    print("功能 2.2.3: 场景化 Prompt 优化")
    print("Scenario-based Prompt Optimization")
    print("=" * 70)
    print()
    
    # 设置测试环境变量
    os.environ.setdefault("AI_PROVIDER", "deepseek")
    os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
    
    parser = AICommandParser()
    
    print("测试不同场景的自动检测:\n")
    
    test_cases = [
        ("创建文件夹 test", "文件操作场景"),
        ("查看所有进程", "系统管理场景"),
        ("下载文件 http://example.com/file.zip", "网络操作场景"),
        ("查看文件 test.txt 的内容", "文本处理场景"),
        ("删除文件 old.txt", "文件操作场景"),
        ("创建用户 john", "系统管理场景"),
        ("ping 测试", "网络操作场景"),
        ("编辑配置文件 config.txt", "文本处理场景")
    ]
    
    for i, (input_text, description) in enumerate(test_cases, 1):
        info = parser.get_scenario_info(input_text)
        print(f"{i}. {description}")
        print(f"   输入: {input_text}")
        print(f"   检测场景: {info['scenario']}")
        print(f"   使用提示词: {info['prompt_file']}")
        print()


def demo_parameter_extraction():
    """演示 2.2.2: 智能参数提取与验证"""
    print("=" * 70)
    print("功能 2.2.2: 智能参数提取与验证")
    print("Intelligent Parameter Extraction and Validation")
    print("=" * 70)
    print()
    
    # 设置测试环境变量
    os.environ.setdefault("AI_PROVIDER", "deepseek")
    os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
    
    parser = AICommandParser()
    
    print("1. 参数提取示例:\n")
    
    test_inputs = [
        "复制文件 test.txt 到 backup.txt",
        "创建目录 /home/user/projects",
        "删除 file1.txt file2.txt file3.txt",
        "查看文件 log.txt 的最后 20 行",
        "下载文件 http://example.com/package.tar.gz"
    ]
    
    for i, input_text in enumerate(test_inputs, 1):
        params = parser.extract_parameters(input_text)
        print(f"{i}. 输入: {input_text}")
        if params['files']:
            print(f"   文件: {params['files']}")
        if params['paths']:
            print(f"   路径: {params['paths']}")
        if params['numbers']:
            print(f"   数字: {params['numbers']}")
        if params['options']:
            print(f"   选项: {params['options']}")
        print()
    
    print("\n2. 路径自动补全示例:\n")
    
    test_paths = [
        (".", "当前目录"),
        ("..", "上级目录"),
        ("./test", "相对路径"),
        ("~/documents", "用户主目录"),
        ("test.txt", "相对文件路径")
    ]
    
    for i, (path, description) in enumerate(test_paths, 1):
        completed = parser.autocomplete_path(path)
        print(f"{i}. {description}")
        print(f"   输入: {path}")
        print(f"   补全: {completed}")
        print()
    
    print("\n3. 参数验证示例:\n")
    
    # 创建一个测试文件
    test_file = "demo_test_file.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file.\n")
    
    test_commands = [
        (f"cat {test_file}", "读取存在的文件"),
        ("cat nonexistent.txt", "读取不存在的文件"),
        ("mkdir new_folder", "创建操作（不检查）")
    ]
    
    for i, (command, description) in enumerate(test_commands, 1):
        is_valid, warnings = parser.validate_parameters(command)
        print(f"{i}. {description}")
        print(f"   命令: {command}")
        print(f"   验证结果: {'有效' if is_valid else '有警告'}")
        if warnings:
            for warning in warnings:
                print(f"   警告: {warning}")
        print()
    
    # 清理测试文件
    os.remove(test_file)


def demo_integrated_features():
    """演示集成功能"""
    print("=" * 70)
    print("集成功能演示")
    print("Integrated Features Demo")
    print("=" * 70)
    print()
    
    # 设置测试环境变量
    os.environ.setdefault("AI_PROVIDER", "deepseek")
    os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
    
    parser = AICommandParser(use_context=True)
    
    print("演示如何结合使用所有增强功能:\n")
    
    print("1. 用户输入自然语言命令")
    user_input = "创建文件夹 my_project"
    print(f"   输入: {user_input}\n")
    
    print("2. 系统自动检测场景")
    info = parser.get_scenario_info(user_input)
    print(f"   检测场景: {info['scenario']}")
    print(f"   选择提示词: {info['prompt_file']}\n")
    
    print("3. 提取和验证参数")
    params = parser.extract_parameters(user_input)
    print(f"   提取的参数: {params}\n")
    
    print("4. 获取系统上下文")
    if parser.context_manager:
        context = parser.context_manager.get_context_for_ai()
        print(f"   系统上下文: {context}\n")
    
    print("5. AI 会结合以上信息生成更准确的命令")
    print("   (实际 API 调用需要配置 .env 文件)\n")


def main():
    """主函数"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 18 + "CLI-AI 增强功能演示" + " " * 18 + "*")
    print("*" + " " * 15 + "Enhanced Features Demo" + " " * 18 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    try:
        # 演示各个功能
        demo_context_manager()
        print("\n")
        
        demo_scenario_detection()
        print("\n")
        
        demo_parameter_extraction()
        print("\n")
        
        demo_integrated_features()
        print("\n")
        
        print("=" * 70)
        print("所有演示完成！")
        print("All demos completed!")
        print("=" * 70)
        print()
        
        print("提示:")
        print("- 这些功能已集成到 AI 命令解析器中")
        print("- 要使用完整功能，请配置 .env 文件并设置 API 密钥")
        print("- 运行 'python ai_command_parser.py' 查看基础测试")
        print("- 运行 'python test_enhanced_parser.py' 运行完整测试套件")
        
    except Exception as e:
        print(f"演示过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
