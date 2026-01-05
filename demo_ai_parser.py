#!/usr/bin/env python3
"""
AI 命令解析器演示脚本
Demonstrates the AI Command Parser functionality
"""
import os
from ai_command_parser import AICommandParser


def main():
    """演示 AI 命令解析器功能"""
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("=" * 60)
        print("⚠️  未检测到 .env 配置文件")
        print("   请按照以下步骤配置:")
        print("   1. cp .env.example .env")
        print("   2. 编辑 .env 文件，填入你的 API 密钥")
        print("   3. 重新运行此脚本")
        print("=" * 60)
        return
    
    print("=" * 60)
    print("AI 命令解析器演示")
    print("AI Command Parser Demo")
    print("=" * 60)
    print()
    
    try:
        # 创建解析器
        parser = AICommandParser()
        print(f"✓ 解析器已初始化")
        print(f"✓ AI 提供商: {parser.ai_provider.provider}")
        print(f"✓ 模型: {parser.ai_provider.get_model()}")
        print()
        
        # 示例测试用例
        test_cases = [
            "列出所有文件",
            "show disk usage",
            "查看内存使用情况",
            "create a directory named test",
            "显示当前目录",
        ]
        
        print("开始测试命令解析:")
        print("-" * 60)
        
        for i, test_input in enumerate(test_cases, 1):
            print(f"\n{i}. 输入: {test_input}")
            try:
                command = parser.parse_command(test_input)
                print(f"   输出: {command}")
                print(f"   ✓ 解析成功")
            except Exception as e:
                print(f"   ✗ 解析失败: {e}")
        
        print()
        print("-" * 60)
        print("演示完成!")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请确保 .env 文件配置正确")


if __name__ == "__main__":
    main()
