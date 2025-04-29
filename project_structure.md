# 项目结构说明

## 目录结构

```
基于自然语言处理的智能客服系统/
├── .venv/                  # Python虚拟环境
├── data/                   # 数据存储
│   └── knowledge.json      # 知识库数据
├── database/               # 数据库相关
│   ├── CreateDatabase.py   # 数据库创建
│   ├── CreateTableStructure.py # 表结构创建
│   ├── DeleteData.py       # 数据删除
│   └── QueryData.py        # 数据查询
├── templates/              # HTML模板
│   ├── admin.html          # 管理员页面
│   ├── admin_chat_records.html # 聊天记录
│   ├── chat.html           # 聊天界面
│   ├── edit_profile.html   # 编辑资料
│   ├── index.html          # 首页
│   ├── login.html          # 登录页面
│   ├── profile.html        # 用户资料
│   └── register.html       # 注册页面
├── train/                  # 训练相关
│   ├── data/               # 训练数据
│   │   ├── dev.txt         # 开发集
│   │   ├── test.txt        # 测试集
│   │   └── train.txt       # 训练集
│   ├── models/             # 模型存储
│   └── nlp_train.py        # NLP训练脚本
├── config.py               # 配置文件
├── database.db             # SQLite数据库文件
├── knowledge_base.py       # 知识库模块
├── main.py                 # Flask主程序
├── prompt.py               # 提示词模块
├── siliconflow.py          # 核心处理模块
└── test_siliconflow.py     # 测试脚本
```

## 关键文件说明

- `main.py`: Flask应用入口，包含所有路由和业务逻辑
- `nlp_train.py`: 自然语言处理模型训练脚本
- `knowledge_base.py`: 知识库管理模块
- `CreateTableStructure.py`: 数据库表结构定义
- `templates/`: 前端页面模板
- `train/data/`: 训练数据集