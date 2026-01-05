"""
测试 AI 命令解析器模块
Test AI Command Parser Module
"""
import os
from ai_command_parser import AICommandParser


def test_command_cleaning():
    """测试命令清洗功能"""
    print("=" * 60)
    print("测试命令清洗功能 (Test Command Cleaning)")
    print("=" * 60)
    
    # Set dummy environment variables for testing without API
    os.environ.setdefault("AI_PROVIDER", "deepseek")
    os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
    
    parser = AICommandParser()
    
    test_cases = [
        # (输入, 期望输出描述)
        ("ls -la", "基础命令"),
        ("```bash\nls -la\n```", "带 bash 代码块"),
        ("```\nls -la\n```", "带通用代码块"),
        ("`ls -la`", "带单反引号"),
        ("命令是：ls -la", "带中文前缀"),
        ("The command is: ls -la", "带英文前缀"),
        ("ls -la\n\n这个命令会列出所有文件", "带后续解释（应只取第一行）"),
        ("执行：df -h", "执行前缀"),
        ("ls -la。", "带中文句号"),
        ("ls -la.", "带英文句号"),
    ]
    
    print("\n清洗测试用例:")
    for i, (raw, desc) in enumerate(test_cases, 1):
        cleaned = parser._clean_command(raw)
        print(f"{i}. {desc}")
        print(f"   输入: {repr(raw)}")
        print(f"   输出: {repr(cleaned)}")
        print()
    
    print("✅ 命令清洗测试完成\n")


def test_parser_without_api():
    """测试解析器初始化（不调用 API）"""
    print("=" * 60)
    print("测试解析器初始化 (Test Parser Initialization)")
    print("=" * 60)
    
    try:
        # Set dummy environment variables for testing without API
        os.environ.setdefault("AI_PROVIDER", "deepseek")
        os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
        
        # 测试默认初始化
        parser = AICommandParser()
        print("✓ 解析器初始化成功")
        print(f"✓ AI 提供商: {parser.ai_provider.provider}")
        print(f"✓ 模型: {parser.ai_provider.get_model()}")
        print(f"✓ 提示词文件: {parser.prompt_file}")
        print(f"✓ 系统提示词长度: {len(parser.system_prompt)} 字符")
        print()
        
        # 测试输入验证
        print("测试输入验证:")
        try:
            parser.parse_command("")
            print("✗ 应该对空输入抛出异常")
        except ValueError as e:
            print(f"✓ 空输入验证通过: {e}")
        
        try:
            parser.parse_command("   ")
            print("✗ 应该对空白输入抛出异常")
        except ValueError as e:
            print(f"✓ 空白输入验证通过: {e}")
        
        print("\n✅ 解析器初始化测试完成\n")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def test_with_real_api():
    """使用真实 API 测试（需要配置 .env）"""
    print("=" * 60)
    print("使用真实 API 测试 (Test with Real API)")
    print("=" * 60)
    
    # 检查是否配置了 API
    if not os.path.exists('.env'):
        print("⚠️  未找到 .env 配置文件")
        print("   要进行真实 API 测试，请：")
        print("   1. 复制 .env.example 为 .env")
        print("   2. 填入你的 API 密钥")
        print("   3. 重新运行此测试")
        print()
        return
    
    try:
        parser = AICommandParser()
        
        # 测试用例
        test_inputs = [
            ("列出所有文件", "中文输入"),
            ("show disk usage", "英文输入"),
            ("查看内存使用情况", "中文复杂命令"),
            ("create a directory named test", "英文创建目录"),
            ("显示当前目录", "中文简单命令"),
            ("查看进程", "中文进程管理"),
        ]
        
        print("\n真实 API 测试用例:\n")
        success_count = 0
        
        for i, (input_text, desc) in enumerate(test_inputs, 1):
            print(f"{i}. {desc}")
            print(f"   输入: {input_text}")
            try:
                command = parser.parse_command(input_text)
                print(f"   输出: {command}")
                print("   ✓ 成功")
                success_count += 1
            except Exception as e:
                print(f"   ✗ 失败: {e}")
            print()
        
        print(f"✅ 真实 API 测试完成: {success_count}/{len(test_inputs)} 成功\n")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("   请确保 .env 文件配置正确")
        import traceback
        traceback.print_exc()


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("AI 命令解析器测试套件")
    print("AI Command Parser Test Suite")
    print("=" * 60 + "\n")
    
    # 运行所有测试
    test_command_cleaning()
    test_parser_without_api()
    test_with_real_api()
    
    print("=" * 60)
    print("所有测试完成！")
    print("All tests completed!")
    print("=" * 60)
    print("\n提示:")
    print("- 命令清洗和解析器初始化测试不需要 API 配置")
    print("- 真实 API 测试需要配置 .env 文件")
    print("- 要跳过 API 测试，可以只运行前两个测试函数")


if __name__ == "__main__":
    main()
