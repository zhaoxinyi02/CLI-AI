"""
测试系统环境上下文管理器
Test System Environment Context Manager
"""
import os
import unittest
from context_manager import ContextManager


class TestContextManager(unittest.TestCase):
    """测试上下文管理器"""
    
    def setUp(self):
        """测试前准备"""
        self.manager = ContextManager()
    
    def test_get_current_directory(self):
        """测试获取当前目录"""
        cwd = self.manager.get_current_directory()
        self.assertIsInstance(cwd, str)
        self.assertTrue(len(cwd) > 0)
        self.assertFalse(cwd.startswith("Error"))
        # 验证返回的是绝对路径
        self.assertTrue(os.path.isabs(cwd))
    
    def test_get_username(self):
        """测试获取用户名"""
        username = self.manager.get_username()
        self.assertIsInstance(username, str)
        self.assertTrue(len(username) > 0)
        self.assertFalse(username.startswith("Error"))
    
    def test_get_os_name(self):
        """测试获取操作系统名称"""
        os_name = self.manager.get_os_name()
        self.assertIsInstance(os_name, str)
        self.assertTrue(len(os_name) > 0)
        self.assertFalse(os_name.startswith("Error"))
        # 验证返回的是常见的操作系统名称
        self.assertIn(os_name, ["Linux", "Darwin", "Windows", "Unix"])
    
    def test_get_architecture(self):
        """测试获取系统架构"""
        arch = self.manager.get_architecture()
        self.assertIsInstance(arch, str)
        self.assertTrue(len(arch) > 0)
        self.assertFalse(arch.startswith("Error"))
    
    def test_get_context(self):
        """测试获取完整上下文"""
        context = self.manager.get_context()
        self.assertIsInstance(context, dict)
        
        # 验证所有必需的键存在
        required_keys = ["current_directory", "username", "os_name", "architecture"]
        for key in required_keys:
            self.assertIn(key, context)
            self.assertIsInstance(context[key], str)
            self.assertTrue(len(context[key]) > 0)
    
    def test_context_caching(self):
        """测试上下文缓存"""
        # 第一次调用
        context1 = self.manager.get_context()
        # 第二次调用应该返回缓存的结果
        context2 = self.manager.get_context()
        self.assertEqual(context1, context2)
        self.assertIs(context1, context2)  # 应该是同一个对象
    
    def test_refresh_context(self):
        """测试刷新上下文"""
        # 获取初始上下文
        context1 = self.manager.get_context()
        # 刷新上下文
        context2 = self.manager.refresh_context()
        # 值应该相同但不是同一个对象
        self.assertEqual(context1, context2)
        self.assertIsNot(context1, context2)
    
    def test_get_context_string(self):
        """测试获取格式化上下文字符串"""
        context_str = self.manager.get_context_string()
        self.assertIsInstance(context_str, str)
        self.assertTrue(len(context_str) > 0)
        
        # 验证字符串包含所有必需信息
        self.assertIn("工作目录", context_str)
        self.assertIn("用户名", context_str)
        self.assertIn("操作系统", context_str)
        self.assertIn("系统架构", context_str)
    
    def test_get_context_for_ai(self):
        """测试获取 AI 格式的上下文字符串"""
        ai_context = self.manager.get_context_for_ai()
        self.assertIsInstance(ai_context, str)
        self.assertTrue(len(ai_context) > 0)
        
        # 验证字符串包含所有必需信息
        self.assertIn("User:", ai_context)
        self.assertIn("Dir:", ai_context)
        self.assertIn("OS:", ai_context)
        self.assertIn("Arch:", ai_context)
    
    def test_context_values_consistency(self):
        """测试上下文值的一致性"""
        # 多次调用单个方法，结果应该一致
        cwd1 = self.manager.get_current_directory()
        cwd2 = self.manager.get_current_directory()
        self.assertEqual(cwd1, cwd2)
        
        username1 = self.manager.get_username()
        username2 = self.manager.get_username()
        self.assertEqual(username1, username2)


def run_basic_tests():
    """运行基本测试（不使用 unittest）"""
    print("=" * 60)
    print("基本功能测试")
    print("=" * 60)
    print()
    
    manager = ContextManager()
    
    print("✓ 创建上下文管理器成功")
    
    # 测试各个方法
    tests = [
        ("获取当前目录", manager.get_current_directory),
        ("获取用户名", manager.get_username),
        ("获取操作系统", manager.get_os_name),
        ("获取系统架构", manager.get_architecture),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            print(f"✓ {test_name}: {result}")
        except Exception as e:
            print(f"✗ {test_name}: {e}")
    
    print()
    
    # 测试完整上下文
    try:
        context = manager.get_context()
        print("✓ 获取完整上下文:")
        for key, value in context.items():
            print(f"    {key}: {value}")
    except Exception as e:
        print(f"✗ 获取完整上下文失败: {e}")
    
    print()
    
    # 测试格式化输出
    try:
        context_str = manager.get_context_string()
        print("✓ 格式化上下文字符串:")
        print(context_str)
    except Exception as e:
        print(f"✗ 格式化上下文字符串失败: {e}")
    
    print()
    
    # 测试 AI 格式
    try:
        ai_context = manager.get_context_for_ai()
        print("✓ AI 格式上下文字符串:")
        print(ai_context)
    except Exception as e:
        print(f"✗ AI 格式上下文字符串失败: {e}")
    
    print()
    print("=" * 60)
    print("基本功能测试完成")
    print("=" * 60)


if __name__ == "__main__":
    # 运行基本测试
    run_basic_tests()
    
    print("\n")
    
    # 运行 unittest 测试
    print("=" * 60)
    print("单元测试")
    print("=" * 60)
    unittest.main(verbosity=2)
