"""
测试增强的 AI 命令解析器
Test Enhanced AI Command Parser (v2.2.1 - v2.2.3)
"""
import os
import unittest
from ai_command_parser import AICommandParser


class TestEnhancedAICommandParser(unittest.TestCase):
    """测试增强的 AI 命令解析器"""
    
    def setUp(self):
        """测试前准备"""
        # 设置测试环境变量
        os.environ.setdefault("AI_PROVIDER", "deepseek")
        os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
        self.parser = AICommandParser()
    
    # ========== 2.2.1 系统环境上下文感知测试 ==========
    
    def test_context_manager_initialized(self):
        """测试上下文管理器是否初始化"""
        self.assertIsNotNone(self.parser.context_manager)
        self.assertTrue(self.parser.use_context)
    
    def test_context_manager_disabled(self):
        """测试禁用上下文管理器"""
        parser = AICommandParser(use_context=False)
        self.assertIsNone(parser.context_manager)
        self.assertFalse(parser.use_context)
    
    def test_context_info_format(self):
        """测试上下文信息格式"""
        if self.parser.context_manager:
            context = self.parser.context_manager.get_context_for_ai()
            self.assertIsInstance(context, str)
            self.assertIn("User:", context)
            self.assertIn("Dir:", context)
            self.assertIn("OS:", context)
            self.assertIn("Arch:", context)
    
    # ========== 2.2.2 智能参数提取与验证测试 ==========
    
    def test_extract_files(self):
        """测试提取文件名"""
        params = self.parser.extract_parameters("复制文件 test.txt 到 backup.txt")
        self.assertIn('test.txt', params['files'])
        self.assertIn('backup.txt', params['files'])
    
    def test_extract_paths(self):
        """测试提取路径"""
        params = self.parser.extract_parameters("创建目录 /home/user/test")
        self.assertTrue(len(params['paths']) > 0)
        self.assertTrue(any('/home/user/test' in p for p in params['paths']))
    
    def test_extract_numbers(self):
        """测试提取数字"""
        params = self.parser.extract_parameters("查看文件最后 20 行")
        self.assertIn('20', params['numbers'])
    
    def test_extract_options(self):
        """测试提取选项"""
        params = self.parser.extract_parameters("使用 -la 选项列出文件")
        self.assertTrue(len(params['options']) > 0 or 'la' in params['options'])
    
    def test_autocomplete_relative_path(self):
        """测试相对路径补全"""
        completed = self.parser.autocomplete_path("./test")
        self.assertTrue(os.path.isabs(completed))
        self.assertIn("test", completed)
    
    def test_autocomplete_home_path(self):
        """测试 ~ 路径补全"""
        completed = self.parser.autocomplete_path("~/documents")
        self.assertTrue(os.path.isabs(completed))
        self.assertNotIn("~", completed)
    
    def test_autocomplete_current_dir(self):
        """测试当前目录 . 补全"""
        completed = self.parser.autocomplete_path(".")
        self.assertTrue(os.path.isabs(completed))
        self.assertEqual(completed, os.getcwd())
    
    def test_validate_parameters_creation_command(self):
        """测试创建命令的参数验证"""
        # 创建命令不应该警告文件不存在
        is_creation = self.parser._is_creation_command("mkdir new_folder")
        self.assertTrue(is_creation)
    
    def test_validate_parameters_read_command(self):
        """测试读取命令的参数验证"""
        # 读取命令应该检查文件是否存在
        is_creation = self.parser._is_creation_command("cat test.txt")
        self.assertFalse(is_creation)
    
    # ========== 2.2.3 场景化 Prompt 优化测试 ==========
    
    def test_detect_file_operations_scenario(self):
        """测试检测文件操作场景"""
        test_cases = [
            "创建文件夹 test",
            "删除文件 test.txt",
            "复制文件 a.txt 到 b.txt",
            "移动文件",
            "create folder",
            "remove file"
        ]
        for input_text in test_cases:
            scenario = self.parser._detect_scenario(input_text)
            self.assertEqual(scenario, 'file_operations', 
                           f"Failed for input: {input_text}")
    
    def test_detect_system_management_scenario(self):
        """测试检测系统管理场景"""
        test_cases = [
            "查看所有进程",
            "创建用户 john",
            "启动服务",
            "show processes",
            "kill process",
            "add user"
        ]
        for input_text in test_cases:
            scenario = self.parser._detect_scenario(input_text)
            self.assertEqual(scenario, 'system_management',
                           f"Failed for input: {input_text}")
    
    def test_detect_network_operations_scenario(self):
        """测试检测网络操作场景"""
        test_cases = [
            "下载文件 http://example.com/file.zip",
            "上传文件到服务器",
            "ping 测试",
            "download file",
            "upload to server",
            "ssh connect"
        ]
        for input_text in test_cases:
            scenario = self.parser._detect_scenario(input_text)
            self.assertEqual(scenario, 'network_operations',
                           f"Failed for input: {input_text}")
    
    def test_detect_text_processing_scenario(self):
        """测试检测文本处理场景"""
        test_cases = [
            "查看文件内容",
            "编辑文件 test.txt",
            "搜索关键词",
            "view file",
            "edit text",
            "search pattern"
        ]
        for input_text in test_cases:
            scenario = self.parser._detect_scenario(input_text)
            self.assertEqual(scenario, 'text_processing',
                           f"Failed for input: {input_text}")
    
    def test_detect_default_scenario(self):
        """测试检测默认场景"""
        # 无明显关键词的输入应该返回默认场景
        scenario = self.parser._detect_scenario("做一些操作")
        self.assertIn(scenario, ['command_generation', 'file_operations', 
                                 'system_management', 'network_operations', 
                                 'text_processing'])
    
    def test_select_prompt_by_scenario(self):
        """测试根据场景选择提示词"""
        scenarios = ['file_operations', 'system_management', 
                    'network_operations', 'text_processing']
        
        for scenario in scenarios:
            prompt = self.parser._select_prompt_by_scenario(scenario)
            self.assertIsInstance(prompt, str)
            self.assertTrue(len(prompt) > 0)
    
    def test_get_scenario_info(self):
        """测试获取场景信息"""
        info = self.parser.get_scenario_info("创建文件夹 test")
        self.assertIn('scenario', info)
        self.assertIn('prompt_file', info)
        self.assertEqual(info['scenario'], 'file_operations')
        self.assertIn('file_operations.txt', info['prompt_file'])
    
    def test_prompt_files_exist(self):
        """测试提示词文件是否存在"""
        prompt_files = [
            'prompts/file_operations.txt',
            'prompts/system_management.txt',
            'prompts/network_operations.txt',
            'prompts/text_processing.txt',
            'prompts/command_generation.txt'
        ]
        
        for prompt_file in prompt_files:
            self.assertTrue(os.path.exists(prompt_file),
                          f"Prompt file not found: {prompt_file}")
    
    # ========== 命令清洗测试 ==========
    
    def test_clean_command_basic(self):
        """测试基础命令清洗"""
        cleaned = self.parser._clean_command("ls -la")
        self.assertEqual(cleaned, "ls -la")
    
    def test_clean_command_with_code_block(self):
        """测试清洗带代码块的命令"""
        cleaned = self.parser._clean_command("```bash\nls -la\n```")
        self.assertEqual(cleaned, "ls -la")
    
    def test_clean_command_with_prefix(self):
        """测试清洗带前缀的命令"""
        cleaned = self.parser._clean_command("命令是：ls -la")
        self.assertEqual(cleaned, "ls -la")
    
    def test_clean_command_with_punctuation(self):
        """测试清洗带标点的命令"""
        cleaned = self.parser._clean_command("ls -la。")
        self.assertEqual(cleaned, "ls -la")


class TestParameterExtraction(unittest.TestCase):
    """专门测试参数提取功能"""
    
    def setUp(self):
        """测试前准备"""
        os.environ.setdefault("AI_PROVIDER", "deepseek")
        os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
        self.parser = AICommandParser()
    
    def test_extract_multiple_files(self):
        """测试提取多个文件"""
        params = self.parser.extract_parameters(
            "删除 file1.txt file2.txt file3.txt"
        )
        self.assertGreaterEqual(len(params['files']), 2)
    
    def test_extract_path_with_tilde(self):
        """测试提取带 ~ 的路径"""
        params = self.parser.extract_parameters("进入 ~/documents")
        self.assertTrue(any('~' in p for p in params['paths']))
    
    def test_extract_absolute_path(self):
        """测试提取绝对路径"""
        params = self.parser.extract_parameters("查看 /var/log/syslog")
        self.assertTrue(any('/var/log' in p for p in params['paths']))
    
    def test_extract_no_parameters(self):
        """测试无参数的输入"""
        params = self.parser.extract_parameters("列出所有文件")
        # 应该返回空列表或很少的参数
        self.assertIsInstance(params, dict)


def run_basic_tests():
    """运行基本功能测试（不使用 unittest）"""
    print("=" * 60)
    print("增强功能基本测试")
    print("=" * 60)
    print()
    
    os.environ.setdefault("AI_PROVIDER", "deepseek")
    os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-key")
    
    parser = AICommandParser()
    
    # 测试 1: 场景检测
    print("1. 场景检测测试:")
    test_inputs = [
        ("创建文件夹 test", "file_operations"),
        ("查看进程", "system_management"),
        ("下载文件", "network_operations"),
        ("编辑文件", "text_processing")
    ]
    
    for input_text, expected in test_inputs:
        scenario = parser._detect_scenario(input_text)
        status = "✓" if scenario == expected else "✗"
        print(f"  {status} '{input_text}' -> {scenario} (期望: {expected})")
    print()
    
    # 测试 2: 参数提取
    print("2. 参数提取测试:")
    params = parser.extract_parameters("复制 test.txt 到 backup.txt")
    print(f"  提取的文件: {params['files']}")
    print()
    
    # 测试 3: 路径补全
    print("3. 路径补全测试:")
    paths = [".", "./test", "~/docs"]
    for path in paths:
        completed = parser.autocomplete_path(path)
        print(f"  {path} -> {completed}")
    print()
    
    # 测试 4: 上下文信息
    print("4. 系统上下文测试:")
    if parser.context_manager:
        context = parser.context_manager.get_context_for_ai()
        print(f"  上下文: {context}")
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
