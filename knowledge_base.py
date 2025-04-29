import json
import os
from datetime import datetime

class KnowledgeBase:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.knowledge_file = os.path.join(data_dir, 'knowledge.json')
        
        # 确保data目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        # 初始化知识库文件
        if not os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def add_record(self, question, answer, username=None):
        """添加新的问答记录
        :param username: 用户名，可选参数
        """
        try:
            with open(self.knowledge_file, 'r+', encoding='utf-8') as f:
                try:
                    records = json.load(f)
                except json.JSONDecodeError:
                    records = []
                
                records.append({
                    'question': question,
                    'answer': answer,
                    'username': username,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                f.seek(0)
                json.dump(records, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"知识库记录失败: {str(e)}")
    
    def get_all_records(self):
        """获取所有知识记录"""
        with open(self.knowledge_file, 'r', encoding='utf-8') as f:
            return json.load(f)    
    def search_records(self, keyword):
        """根据关键词搜索记录"""
        records = self.get_all_records()
        return [r for r in records if keyword.lower() in r['question'].lower() or 
                                  keyword.lower() in r['answer'].lower()]
