"""
测试 AI 错误分析器和命令建议器模块
Test AI Error Analyzer and Command Suggester Module
"""
import os
from ai_error_analyzer import AIErrorAnalyzer, AICommandSuggester


def test_error_analyzer_init():
    """测试错误分析器初始化"""
    print("=" * 60)
    print("测试错误分析器初始化 (Test Error Analyzer Initialization)")
    print("=" * 60)
    
    try:
        # Set dummy environment variables for testing
        os.environ.setdefault("AI_PROVIDER", "deepseek")
        os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
        
        analyzer = AIErrorAnalyzer()
        print("✓ 错误分析器初始化成功")
        
        if analyzer.ai_provider:
            print(f"✓ AI 提供商: {analyzer.ai_provider.provider}")
        else:
            print("⚠️  AI 提供商未启用，使用基础模式")
        
        print("\n✅ 初始化测试完成\n")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def test_basic_error_analysis():
    """测试基础错误分析（不使用 API）"""
    print("=" * 60)
    print("测试基础错误分析 (Test Basic Error Analysis)")
    print("=" * 60)
    
    try:
        analyzer = AIErrorAnalyzer()
        
        test_cases = [
            {
                'name': '权限不足',
                'command': 'cat /root/secret.txt',
                'error': 'cat: /root/secret.txt: Permission denied',
                'return_code': 1
            },
            {
                'name': '命令未找到',
                'command': 'invalidcommand',
                'error': 'bash: invalidcommand: command not found',
                'return_code': 127
            },
            {
                'name': '文件不存在',
                'command': 'cat nonexistent.txt',
                'error': 'cat: nonexistent.txt: No such file or directory',
                'return_code': 1
            },
            {
                'name': '文件已存在',
                'command': 'mkdir test',
                'error': 'mkdir: cannot create directory \'test\': File exists',
                'return_code': 1
            }
        ]
        
        print("\n基础错误分析测试用例:\n")
        
        for i, case in enumerate(test_cases, 1):
            print(f"{i}. {case['name']}")
            print(f"   命令: {case['command']}")
            print(f"   错误: {case['error']}")
            
            result = analyzer._basic_error_analysis(
                case['command'],
                case['error'],
                case['return_code']
            )
            
            print(f"   分析: {result['analysis']}")
            print(f"   建议: {result['suggestion']}")
            if result['alternative_command']:
                print(f"   替代命令: {result['alternative_command']}")
            print()
        
        print("✅ 基础错误分析测试完成\n")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def test_command_suggester_init():
    """测试命令建议器初始化"""
    print("=" * 60)
    print("测试命令建议器初始化 (Test Command Suggester Initialization)")
    print("=" * 60)
    
    try:
        os.environ.setdefault("AI_PROVIDER", "deepseek")
        os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
        
        suggester = AICommandSuggester()
        print("✓ 命令建议器初始化成功")
        
        if suggester.ai_provider:
            print(f"✓ AI 提供商: {suggester.ai_provider.provider}")
        else:
            print("⚠️  AI 提供商未启用")
        
        print("\n✅ 初始化测试完成\n")
        
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
        analyzer = AIErrorAnalyzer()
        
        if not analyzer.ai_provider:
            print("⚠️  AI 提供商未启用，跳过真实 API 测试")
            return
        
        print("\n真实 API 错误分析测试:\n")
        
        # 测试用例
        test_command = "cat /root/secret.txt"
        test_error = "cat: /root/secret.txt: Permission denied"
        test_return_code = 1
        
        print(f"命令: {test_command}")
        print(f"错误: {test_error}")
        print(f"返回码: {test_return_code}\n")
        
        result = analyzer.analyze_error(test_command, test_error, test_return_code)
        
        print("AI 分析结果:")
        print(f"原因: {result['analysis']}")
        print(f"建议: {result['suggestion']}")
        if result['alternative_command']:
            print(f"替代命令: {result['alternative_command']}")
        
        print("\n✅ 真实 API 测试完成\n")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("   请确保 .env 文件配置正确")
        import traceback
        traceback.print_exc()


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("AI 错误分析器测试套件")
    print("AI Error Analyzer Test Suite")
    print("=" * 60 + "\n")
    
    # 运行所有测试
    test_error_analyzer_init()
    test_basic_error_analysis()
    test_command_suggester_init()
    test_with_real_api()
    
    print("=" * 60)
    print("所有测试完成！")
    print("All tests completed!")
    print("=" * 60)
    print("\n提示:")
    print("- 初始化和基础分析测试不需要 API 配置")
    print("- 真实 API 测试需要配置 .env 文件")


if __name__ == "__main__":
    main()
