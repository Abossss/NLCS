import sqlite3

# 连接数据库
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# 删除数据
cur.execute("DELETE FROM users WHERE id=1")

# 提交更改
conn.commit()

# 查询剩余数据
cur.execute("SELECT * FROM users")
rows = cur.fetchall()

# 打印结果
for row in rows:
    print(row)

# 关闭连接
conn.close()