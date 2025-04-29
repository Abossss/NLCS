"""
AI客服prompt生成模块
"""

import config

class AIPersonality:
    """
    AI客服prompt生成器
    """
        
    @classmethod
    def manage_dialogue(cls, message: str) -> dict:
        """根据用户消息生成API调用参数"""
        return {
            "model": config.MODEL_CONFIG["model_name"],
            "messages": [
                {"role": "system", "content": config.SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            "max_tokens": config.MODEL_CONFIG["max_tokens"],
            "temperature": config.MODEL_CONFIG["temperature"],
            "stream": config.MODEL_CONFIG["stream"],
            "stop": config.MODEL_CONFIG["stop"]
        }