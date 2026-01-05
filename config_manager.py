"""
配置管理模块
用于查看和编辑 .env 配置文件
"""
import os
import sys
from pathlib import Path
from typing import Dict, Optional


class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, env_path: str = ".env"):
        self.env_path = Path(env_path)
        self.example_path = Path(".env.example")
    
    def exists(self) -> bool:
        """检查配置文件是否存在"""
        return self.env_path.exists()
    
    def create_from_example(self) -> bool:
        """从示例文件创建配置文件"""
        if not self.example_path.exists():
            print(f"错误: 示例配置文件 {self.example_path} 不存在")
            return False
        
        try:
            # 复制示例文件
            content = self.example_path.read_text(encoding='utf-8')
            self.env_path.write_text(content, encoding='utf-8')
            print(f"✓ 已创建配置文件: {self.env_path}")
            return True
        except Exception as e:
            print(f"错误: 创建配置文件失败: {e}")
            return False
    
    def read_config(self) -> Optional[Dict[str, str]]:
        """读取配置文件内容"""
        if not self.exists():
            return None
        
        try:
            config = {}
            with open(self.env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过注释和空行
                    if not line or line.startswith('#'):
                        continue
                    
                    # 解析键值对
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
            
            return config
        except Exception as e:
            print(f"错误: 读取配置文件失败: {e}")
            return None
    
    def update_config(self, key: str, value: str) -> bool:
        """更新配置文件中的某个值"""
        if not self.exists():
            print(f"错误: 配置文件 {self.env_path} 不存在")
            return False
        
        try:
            # 读取所有行
            lines = []
            key_found = False
            
            with open(self.env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped = line.strip()
                    
                    # 如果找到了要更新的键
                    if stripped and not stripped.startswith('#') and '=' in stripped:
                        current_key = stripped.split('=', 1)[0].strip()
                        if current_key == key:
                            lines.append(f"{key}={value}\n")
                            key_found = True
                            continue
                    
                    lines.append(line)
            
            # 如果键不存在，添加到文件末尾
            if not key_found:
                lines.append(f"\n# 用户添加\n{key}={value}\n")
            
            # 写回文件
            with open(self.env_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"✓ 已更新配置: {key}={value}")
            return True
            
        except Exception as e:
            print(f"错误: 更新配置失败: {e}")
            return False
    
    def display_config(self, show_secrets: bool = False):
        """显示当前配置"""
        config = self.read_config()
        
        if config is None:
            print("\n配置文件不存在")
            print("使用 'config init' 创建配置文件")
            return
        
        print("\n当前配置:")
        print("=" * 50)
        
        # 定义敏感键（需要隐藏）
        sensitive_keys = ['API_KEY', 'KEY', 'SECRET', 'PASSWORD', 'TOKEN']
        
        for key, value in sorted(config.items()):
            # 检查是否是敏感信息
            is_sensitive = any(sk in key.upper() for sk in sensitive_keys)
            
            if is_sensitive and not show_secrets:
                # 隐藏敏感信息，只显示前几位
                if value and len(value) > 8:
                    masked_value = value[:4] + "****" + value[-4:]
                else:
                    masked_value = "****"
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}")
        
        print("=" * 50)
        
        if not show_secrets:
            print("\n提示: 使用 'config show --secrets' 显示完整的敏感信息")


def handle_config_command(args: list) -> bool:
    """
    处理 config 命令
    
    Args:
        args: 命令参数列表
        
    Returns:
        是否成功处理
    """
    manager = ConfigManager()
    
    # 没有参数，显示配置
    if not args:
        manager.display_config()
        return True
    
    command = args[0].lower()
    
    # config show - 显示配置
    if command in ['show', 'view', 'display']:
        show_secrets = '--secrets' in args or '-s' in args
        manager.display_config(show_secrets=show_secrets)
        return True
    
    # config init - 初始化配置
    elif command in ['init', 'create', 'setup']:
        if manager.exists():
            response = input(f"配置文件已存在。是否覆盖？(y/n): ").strip().lower()
            if response not in ['y', 'yes', '是']:
                print("已取消")
                return True
        
        manager.create_from_example()
        return True
    
    # config set KEY VALUE - 设置配置项
    elif command == 'set':
        if len(args) < 3:
            print("用法: config set KEY VALUE")
            return False
        
        key = args[1]
        value = ' '.join(args[2:])  # 值可能包含空格
        manager.update_config(key, value)
        return True
    
    # config edit - 使用编辑器编辑
    elif command == 'edit':
        if not manager.exists():
            print("配置文件不存在，使用 'config init' 创建")
            return False
        
        # 使用系统默认编辑器
        editor = os.getenv('EDITOR', 'nano')
        os.system(f"{editor} {manager.env_path}")
        print("配置文件已更新")
        return True
    
    # config help - 帮助
    elif command in ['help', '-h', '--help']:
        print_config_help()
        return True
    
    else:
        print(f"未知的 config 命令: {command}")
        print("使用 'config help' 查看帮助")
        return False


def print_config_help():
    """打印 config 命令帮助"""
    print("\n配置命令帮助:")
    print("=" * 50)
    print("  config                    - 显示当前配置")
    print("  config show               - 显示当前配置")
    print("  config show --secrets     - 显示配置（包含敏感信息）")
    print("  config init               - 创建配置文件")
    print("  config set KEY VALUE      - 设置配置项")
    print("  config edit               - 使用编辑器编辑配置")
    print("  config help               - 显示此帮助")
    print("=" * 50)
    print("\n示例:")
    print("  config init")
    print("  config set AI_PROVIDER openai")
    print("  config set OPENAI_API_KEY sk-xxx")
    print("  config show --secrets")
