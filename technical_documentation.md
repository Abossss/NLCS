# 技术文档

## 系统架构

本系统采用MVC架构设计，主要分为三层：
1. **模型层**: 数据库操作和NLP模型
   - `database/`: SQLite数据库操作
   - `train/nlp_train.py`: 文本分类模型训练
2. **视图层**: HTML模板
   - `templates/`: 前端页面
3. **控制层**: Flask路由
   - `main.py`: 处理HTTP请求

## 核心算法

### 自然语言处理模块
- 使用PyTorch实现文本分类模型
- 包含词汇表构建、文本向量化等功能
- 支持自定义最大序列长度

### 知识库管理
- 基于JSON文件存储问答知识
- 支持增删改查操作

## API设计

### 用户认证
- `/login`: 用户登录
- `/register`: 用户注册

### 客服功能
- `/chat`: 智能问答接口

### 管理后台
- `/admin/dashboard`: 管理面板
- `/admin/chat-records`: 聊天记录管理

## 数据库设计

### users表
- username: 用户名(唯一)
- password: 加密密码
- role: 用户角色
- email: 电子邮箱
- register_time: 注册时间
- last_login: 最后登录时间