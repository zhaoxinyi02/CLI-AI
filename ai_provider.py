"""
AI 提供商抽象层
支持 OpenAI 和 DeepSeek API
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv
import httpx

class AIProvider:
    """AI 提供商基类"""
    
    def __init__(self):
        self._load_env_with_validation()
        self.provider = os.getenv("AI_PROVIDER", "deepseek").lower()
        self.client = self._init_client()
    
    def _load_env_with_validation(self):
        """加载并验证 .env 文件"""
        env_path = Path(".env")
        
        # 尝试加载 .env 文件
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        else:
            # .env 文件不存在，显示警告
            print("⚠️  警告: .env 文件未找到", file=sys.stderr)
            print("", file=sys.stderr)
            print("建议操作:", file=sys.stderr)
            print("  1. 复制示例配置文件: cp .env.example .env", file=sys.stderr)
            print("  2. 编辑 .env 文件，填入您的 API 密钥", file=sys.stderr)
            print("  3. 重新运行程序", file=sys.stderr)
            print("", file=sys.stderr)
            print("或者使用 'config' 命令创建配置文件", file=sys.stderr)
            print("", file=sys.stderr)
            
            # 仍然尝试从环境变量加载（可能在系统环境变量中设置）
            load_dotenv()
    
    def _get_proxy_config(self) -> Optional[httpx.HTTPTransport]:
        """配置代理设置，支持 HTTP 和 SOCKS5"""
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
        
        if not http_proxy and not https_proxy:
            return None
        
        try:
            # 优先使用 HTTPS 代理
            proxy_url = https_proxy or http_proxy
            
            # 验证代理 URL 格式
            if not proxy_url.startswith(("http://", "https://", "socks5://", "socks5h://")):
                print(f"⚠️  警告: 代理 URL 格式无效: {proxy_url}", file=sys.stderr)
                print("   支持的格式: http://, https://, socks5://, socks5h://", file=sys.stderr)
                print("   将继续不使用代理", file=sys.stderr)
                return None
            
            # 创建代理配置
            # 注意: OpenAI SDK 使用 httpx，它会自动处理代理设置
            # 我们只需要返回 None，让 httpx 从环境变量中读取代理
            return None
            
        except Exception as e:
            print(f"⚠️  警告: 代理配置失败: {e}", file=sys.stderr)
            print("   将继续不使用代理", file=sys.stderr)
            return None
    
    def _init_client(self) -> OpenAI:
        """初始化 AI 客户端"""
        # 配置代理（如果设置了）
        self._get_proxy_config()
        
        api_key = None
        base_url = None
        
        try:
            if self.provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
                
                if not api_key:
                    raise ValueError(
                        "OpenAI API 密钥未配置\n"
                        "请在 .env 文件中设置 OPENAI_API_KEY\n"
                        "或使用 'config' 命令配置"
                    )
                
                return OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
                
            elif self.provider == "deepseek":
                api_key = os.getenv("DEEPSEEK_API_KEY")
                base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
                
                if not api_key:
                    raise ValueError(
                        "DeepSeek API 密钥未配置\n"
                        "请在 .env 文件中设置 DEEPSEEK_API_KEY\n"
                        "或使用 'config' 命令配置"
                    )
                
                return OpenAI(
                    api_key=api_key,
                    base_url=base_url
                )
            else:
                raise ValueError(
                    f"不支持的 AI 提供商: {self.provider}\n"
                    f"支持的提供商: openai, deepseek\n"
                    f"请在 .env 文件中设置 AI_PROVIDER"
                )
        except ImportError as e:
            # 处理 SOCKS5 代理相关的导入错误
            if "socksio" in str(e) or "socks" in str(e).lower():
                # 清除 SOCKS5 代理设置并重试
                http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
                https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
                
                if http_proxy and "socks" in http_proxy.lower():
                    os.environ.pop("HTTP_PROXY", None)
                    os.environ.pop("http_proxy", None)
                if https_proxy and "socks" in https_proxy.lower():
                    os.environ.pop("HTTPS_PROXY", None)
                    os.environ.pop("https_proxy", None)
                
                print("⚠️  警告: SOCKS5 代理需要安装额外依赖", file=sys.stderr)
                print("   请运行: pip install httpx[socks]", file=sys.stderr)
                print("   将继续不使用 SOCKS5 代理", file=sys.stderr)
                print("", file=sys.stderr)
                
                # 重试初始化
                if self.provider == "openai":
                    return OpenAI(api_key=api_key, base_url=base_url)
                elif self.provider == "deepseek":
                    return OpenAI(api_key=api_key, base_url=base_url)
            raise
    
    def get_model(self) -> str:
        """获取当前使用的模型"""
        if self.provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4")
        elif self.provider == "deepseek":
            return os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        else:
            raise ValueError(f"不支持的 AI 提供商: {self.provider}")
    
    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        生成 AI 响应
        
        Args:
            system_prompt: 系统提示词
            user_message: 用户消息
            history: 对话历史 [{"role": "user", "content": "..."}, ...]
            temperature: 温度参数（0-1）
            max_tokens: 最大 token 数
            
        Returns:
            AI 生成的文本响应
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.get_model(),
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            content = response.choices[0].message.content
            if content is None:
                raise Exception("AI 返回了空响应")
            return content.strip()
        except Exception as e:
            raise Exception(f"AI 调用失败: {str(e)}")
