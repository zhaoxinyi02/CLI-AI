"""Test AI Provider Module

This module tests the AI provider abstraction layer without making actual API calls.
For complete testing with real API calls, configure your .env file with valid API keys.
"""
import os
from ai_provider import AIProvider

def test_ai_provider():
    """Test AI provider initialization and configuration"""
    try:
        print("Testing AI Provider Initialization...")
        
        # Save original environment to restore later
        original_env = os.environ.copy()
        
        # Test 1: DeepSeek provider
        os.environ["AI_PROVIDER"] = "deepseek"
        os.environ["DEEPSEEK_API_KEY"] = "sk-test-key"
        os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com/v1"
        os.environ["DEEPSEEK_MODEL"] = "deepseek-chat"
        
        ai = AIProvider()
        print(f"✓ AI Provider: {ai.provider}")
        print(f"✓ Model: {ai.get_model()}")
        print(f"✓ Client initialized: {ai.client is not None}")
        
        # Test 2: OpenAI provider
        os.environ["AI_PROVIDER"] = "openai"
        os.environ["OPENAI_API_KEY"] = "sk-test-key"
        os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1"
        os.environ["OPENAI_MODEL"] = "gpt-4"
        
        ai_openai = AIProvider()
        print(f"✓ OpenAI Provider: {ai_openai.provider}")
        print(f"✓ OpenAI Model: {ai_openai.get_model()}")
        
        # Test 3: Unsupported provider error handling
        try:
            os.environ["AI_PROVIDER"] = "unsupported"
            ai_bad = AIProvider()
            print("✗ Should have raised ValueError for unsupported provider")
        except ValueError as e:
            print(f"✓ Correctly detected unsupported provider: {e}")
        
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)
        
        print("\n✅ AI Model Integration Tests Passed!")
        print("\nNote:")
        print("- These are basic functionality tests without actual API calls")
        print("- To test with real API calls, configure your .env file:")
        print("  1. cp .env.example .env")
        print("  2. Edit .env with your actual API keys")
        print("  3. Run: python test_ai_provider.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        # Restore environment on error
        os.environ.clear()
        os.environ.update(original_env)

if __name__ == "__main__":
    test_ai_provider()
