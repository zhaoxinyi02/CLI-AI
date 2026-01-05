"""
AI 提供商抽象层
支持 OpenAI 和 DeepSeek API
"""
import os
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

class AIProvider:
    """AI 提供商基类"""
    
    def __init__(self):
        load_dotenv()
        self.provider = os.getenv("AI_PROVIDER", "deepseek").lower()
        self.client = self._init_client()
    
    def _init_client(self) -> OpenAI:
        """初始化 AI 客户端"""
        if self.provider == "openai":
            return OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            )
        elif self.provider == "deepseek":
            return OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
            )
        else:
            raise ValueError(f"不支持的 AI 提供商: {self.provider}")
    
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
