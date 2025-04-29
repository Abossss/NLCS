import sqlite3

# 建立一个基于硬盘的数据库实例
conn = sqlite3.connect("database.db")

# 关闭与数据库的连接
conn.close()