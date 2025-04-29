import unittest
from unittest.mock import patch
from siliconflow import SiliconFlowChat

class TestSiliconFlowChat(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.chat = SiliconFlowChat(self.api_key)
    
    @patch('siliconflow.requests.post')
    def test_get_response_success(self, mock_post):
        # 模拟成功响应
        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "测试回复"}}]
        }
        
        result = self.chat.get_response("测试消息")
        self.assertEqual(result, "测试回复")
    
    @patch('siliconflow.requests.post')
    def test_get_response_error(self, mock_post):
        # 模拟错误响应
        mock_post.side_effect = Exception("API错误")
        
        result = self.chat.get_response("测试消息")
        self.assertEqual(result, "发生错误: API错误")

def main():
    api_key = input("请输入API密钥: ")
    chat = SiliconFlowChat(api_key)
    while True:
        message = input("请输入消息(输入q退出): ")
        if message.lower() == 'q':
            break
        response = chat.get_response(message)
        print(f"响应结果: {response}")
        print(f"响应类型: {response}")

if __name__ == '__main__':
    # unittest.main()
    main()