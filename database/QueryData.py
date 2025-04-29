import sqlite3

def get_user_by_username(username):
    """根据用户名查询用户信息"""
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    
    conn.close()
    return user

def get_all_users():
    """获取所有用户信息"""
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    
    conn.close()
    return users