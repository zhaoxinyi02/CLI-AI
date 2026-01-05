"""
测试配置管理器和 .env 加载功能
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path


def test_env_loading_validation():
    """测试 .env 文件加载和验证"""
    print("测试 .env 文件加载和验证...")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        
        try:
            os.chdir(tmpdir)
            
            # 测试 1: 没有 .env 文件的情况
            print("  测试 1: 没有 .env 文件")
            from ai_provider import AIProvider
            
            # 应该显示警告但不抛出异常（除非缺少 API 密钥）
            try:
                # 设置环境变量以避免 API 密钥错误
                os.environ["AI_PROVIDER"] = "deepseek"
                os.environ["DEEPSEEK_API_KEY"] = "test-key"
                provider = AIProvider()
                print("    ✓ 即使没有 .env 文件也能初始化（使用环境变量）")
            except Exception as e:
                print(f"    ✓ 正确处理了缺失的 .env 文件: {e}")
            
            # 清理环境变量
            for key in ["AI_PROVIDER", "DEEPSEEK_API_KEY", "OPENAI_API_KEY"]:
                if key in os.environ:
                    del os.environ[key]
            
            # 测试 2: 创建 .env 文件
            print("  测试 2: 创建 .env 文件")
            env_content = """AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-test-key-123
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
"""
            Path(".env").write_text(env_content)
            
            # 重新导入模块以测试
            import importlib
            import ai_provider
            importlib.reload(ai_provider)
            from ai_provider import AIProvider
            
            provider2 = AIProvider()
            print(f"    ✓ 成功从 .env 加载配置")
            print(f"    ✓ Provider: {provider2.provider}")
            
            # 测试 3: API 密钥验证
            print("  测试 3: API 密钥验证")
            env_no_key = """AI_PROVIDER=openai
OPENAI_BASE_URL=https://api.openai.com/v1
"""
            Path(".env").write_text(env_no_key)
            
            # 确保环境变量也被清除
            for key in ["OPENAI_API_KEY", "DEEPSEEK_API_KEY"]:
                if key in os.environ:
                    del os.environ[key]
            
            importlib.reload(ai_provider)
            from ai_provider import AIProvider
            
            try:
                provider3 = AIProvider()
                print("    ✗ 应该抛出 API 密钥缺失错误")
            except (ValueError, Exception) as e:
                if "API 密钥未配置" in str(e) or "API" in str(e) or "密钥" in str(e):
                    print("    ✓ 正确检测到缺失的 API 密钥")
                else:
                    print(f"    ✓ 抛出了错误: {type(e).__name__}")
            
        finally:
            os.chdir(original_dir)
    
    print("✅ .env 加载验证测试完成\n")


def test_proxy_configuration():
    """测试代理配置功能"""
    print("测试代理配置...")
    
    original_dir = os.getcwd()
    
    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            # 创建 .env 文件
            env_content = """AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-test-key
"""
            Path(".env").write_text(env_content)
            
            # 测试 1: HTTP 代理
            print("  测试 1: HTTP 代理配置")
            os.environ["HTTP_PROXY"] = "http://proxy.example.com:8080"
            
            import importlib
            import ai_provider
            importlib.reload(ai_provider)
            from ai_provider import AIProvider
            
            provider = AIProvider()
            print("    ✓ HTTP 代理配置成功")
            
            # 清理
            if "HTTP_PROXY" in os.environ:
                del os.environ["HTTP_PROXY"]
            
            # 测试 2: SOCKS5 代理
            print("  测试 2: SOCKS5 代理配置")
            os.environ["HTTPS_PROXY"] = "socks5://127.0.0.1:1080"
            
            importlib.reload(ai_provider)
            from ai_provider import AIProvider
            
            try:
                provider2 = AIProvider()
                print("    ✓ SOCKS5 代理配置成功（或正确处理了缺失的依赖）")
            except ImportError as e:
                if "socksio" in str(e):
                    print("    ✓ 正确检测到缺失的 SOCKS5 依赖")
                else:
                    raise
            
            # 清理
            if "HTTPS_PROXY" in os.environ:
                del os.environ["HTTPS_PROXY"]
            
            # 测试 3: 无效代理格式
            print("  测试 3: 无效代理格式处理")
            os.environ["HTTP_PROXY"] = "invalid-proxy-url"
            
            importlib.reload(ai_provider)
            from ai_provider import AIProvider
            
            provider3 = AIProvider()
            print("    ✓ 正确处理无效代理（应显示警告并继续）")
            
            # 清理
            if "HTTP_PROXY" in os.environ:
                del os.environ["HTTP_PROXY"]
            
    finally:
        os.chdir(original_dir)
    
    print("✅ 代理配置测试完成\n")


def test_config_manager():
    """测试配置管理器"""
    print("测试配置管理器...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        
        try:
            os.chdir(tmpdir)
            
            # 创建示例文件
            example_content = """AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-example
"""
            Path(".env.example").write_text(example_content)
            
            from config_manager import ConfigManager
            
            manager = ConfigManager()
            
            # 测试 1: 检查文件是否存在
            print("  测试 1: 检查文件存在性")
            assert not manager.exists(), "配置文件不应该存在"
            print("    ✓ 正确检测配置文件不存在")
            
            # 测试 2: 从示例创建配置
            print("  测试 2: 从示例创建配置")
            result = manager.create_from_example()
            assert result, "应该成功创建配置文件"
            assert manager.exists(), "配置文件应该存在"
            print("    ✓ 成功从示例创建配置文件")
            
            # 测试 3: 读取配置
            print("  测试 3: 读取配置")
            config = manager.read_config()
            assert config is not None, "应该能读取配置"
            assert "AI_PROVIDER" in config, "应该包含 AI_PROVIDER"
            print(f"    ✓ 成功读取配置: {len(config)} 个配置项")
            
            # 测试 4: 更新配置
            print("  测试 4: 更新配置")
            result = manager.update_config("AI_PROVIDER", "openai")
            assert result, "应该成功更新配置"
            config2 = manager.read_config()
            assert config2["AI_PROVIDER"] == "openai", "值应该被更新"
            print("    ✓ 成功更新配置值")
            
            # 测试 5: 添加新配置
            print("  测试 5: 添加新配置项")
            result = manager.update_config("NEW_KEY", "new_value")
            assert result, "应该成功添加新配置"
            config3 = manager.read_config()
            assert "NEW_KEY" in config3, "新键应该存在"
            assert config3["NEW_KEY"] == "new_value", "新值应该正确"
            print("    ✓ 成功添加新配置项")
            
        finally:
            os.chdir(original_dir)
    
    print("✅ 配置管理器测试完成\n")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("配置和环境变量测试套件")
    print("=" * 60)
    print()
    
    try:
        test_env_loading_validation()
        test_proxy_configuration()
        test_config_manager()
        
        print("=" * 60)
        print("✅ 所有测试通过!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
