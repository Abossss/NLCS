import sqlite3

def create_users_table():
    """创建用户表"""
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user',
    email TEXT,
    register_time TIMESTAMP ,
    last_login TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def add_user(username, password, role='user', email=None):
    """添加新用户"""
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
                   (username, password, role, email))
        conn.commit()
        print(f"用户 {username} 注册成功！")
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def init_database():
    """初始化数据库"""
    create_users_table()
    add_user('Admin', '123456', 'admin')