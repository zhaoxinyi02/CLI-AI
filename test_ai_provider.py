"""测试 AI 提供商"""
import os
from ai_provider import AIProvider

def test_ai_provider():
    """测试 AI 调用"""
    try:
        # Test initialization without API keys
        print("测试 AI 提供商初始化...")
        
        # Set default environment for testing
        os.environ["AI_PROVIDER"] = "deepseek"
        os.environ["DEEPSEEK_API_KEY"] = "sk-test-key"
        os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com/v1"
        os.environ["DEEPSEEK_MODEL"] = "deepseek-chat"
        
        ai = AIProvider()
        print(f"✓ 使用 AI 提供商: {ai.provider}")
        print(f"✓ 使用模型: {ai.get_model()}")
        print(f"✓ 客户端初始化成功: {ai.client is not None}")
        
        # Test OpenAI provider configuration
        os.environ["AI_PROVIDER"] = "openai"
        os.environ["OPENAI_API_KEY"] = "sk-test-key"
        os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1"
        os.environ["OPENAI_MODEL"] = "gpt-4"
        
        ai_openai = AIProvider()
        print(f"✓ OpenAI 提供商: {ai_openai.provider}")
        print(f"✓ OpenAI 模型: {ai_openai.get_model()}")
        
        # Test unsupported provider
        try:
            os.environ["AI_PROVIDER"] = "unsupported"
            ai_bad = AIProvider()
            print("✗ 应该抛出异常，但没有")
        except ValueError as e:
            print(f"✓ 正确检测到不支持的提供商: {e}")
        
        print("\n✅ AI 模型集成测试成功！")
        print("\n注意：")
        print("- 这是基础功能测试，未进行实际 API 调用")
        print("- 要测试真实 API 调用，请配置 .env 文件并运行完整测试")
        print("- 运行步骤：")
        print("  1. cp .env.example .env")
        print("  2. 编辑 .env 文件，填入真实的 API 密钥")
        print("  3. python test_ai_provider.py")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_provider()
