from flask import Flask, request, jsonify
import requests
from prompt import AIPersonality
import config

class SiliconFlowChat:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = config.API_CONFIG["base_url"]
        

    
    def get_response(self, message):
        """获取AI客服响应"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            payload = {
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
            
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"请求API时出错: {str(e)}"
        except KeyError:
            return "解析API响应时出错"
        except Exception as e:
            return f"处理请求时发生未知错误: {str(e)}"

app = Flask(__name__)
chatbot = SiliconFlowChat(config.API_CONFIG["api_key"])

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "消息不能为空"}), 400
    
    response = chatbot.get_response(message)
    return jsonify({"response": response})