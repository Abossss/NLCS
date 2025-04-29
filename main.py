import json
from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from knowledge_base import KnowledgeBase

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'  # 请在生产环境中更换为随机密钥

# 初始化知识库
knowledge_base = KnowledgeBase()

# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            conn = get_db_connection()
            conn.execute('UPDATE users SET last_login = datetime("now", "localtime") WHERE username = ?', (username,))
            conn.commit()
            conn.close()
            session['username'] = username
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if 'username' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        
        try:
            conn = get_db_connection()
            existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            
            if existing_user:
                flash('Username already exists', 'danger')
            elif len(password) < 6:
                flash('Password must be at least 6 characters', 'danger')
            else:

                conn.execute('INSERT INTO users (username, password, role, email, register_time) VALUES (?, ?, ?, ?, datetime("now", "localtime"))',
                             (username, generate_password_hash(password), 'user', email))
                conn.commit()
                flash('Registration successful! Please login', 'success')
                return redirect(url_for('login_page'))
        except Exception as e:
            conn.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
        finally:
            if 'conn' in locals():
                conn.close()
    
    return render_template('register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You need admin privileges to access this page', 'danger')
        return redirect(url_for('login_page'))
    
    conn = get_db_connection()
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    admin_count = conn.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('admin',)).fetchone()[0]
    users = conn.execute('SELECT username, role, register_time FROM users').fetchall()
    conn.close()
    
    # 加载聊天记录
    try:
        with open('data/knowledge.json', 'r', encoding='utf-8') as f:
            chat_records = json.load(f)
    except FileNotFoundError:
        chat_records = []
        print("警告: knowledge.json文件未找到")
    except json.JSONDecodeError:
        chat_records = []
        print("警告: knowledge.json文件格式错误")
    
    stats = {
        'total_users': total_users,
        'admin_count': admin_count
    }
    
    return render_template('admin.html',
                         username=session['username'],
                         stats=stats,
                         users=users,
                         chat_records=chat_records)

@app.route('/admin/chat-records')
def admin_chat_records():
    if 'username' not in session or session.get('role') != 'admin':
        flash('You need admin privileges to access this page', 'danger')
        return redirect(url_for('login_page'))
    
    # 加载聊天记录
    try:
        with open('data/knowledge.json', 'r', encoding='utf-8') as f:
            chat_records = json.load(f)
    except FileNotFoundError:
        chat_records = []
        print("警告: knowledge.json文件未找到")
    except json.JSONDecodeError:
        chat_records = []
        print("警告: knowledge.json文件格式错误")
    
    return render_template('admin_chat_records.html',
                         username=session['username'],
                         chat_records=chat_records)
                         
@app.route('/admin/chat-records/delete', methods=['DELETE'])
def delete_chat_records():
    if 'username' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': '无权限执行此操作'}, 403
    
    try:
        with open('data/knowledge.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        return {'success': True, 'message': '聊天记录已清空'}
    except Exception as e:
        return {'success': False, 'message': f'删除失败: {str(e)}'}, 500
        
@app.route('/admin/chat-records/export', methods=['GET'])
def export_chat_records():
    if 'username' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': '无权限执行此操作'}, 403
    
    try:
        with open('data/knowledge.json', 'r', encoding='utf-8') as f:
            chat_records = json.load(f)
        return json.dumps(chat_records, ensure_ascii=False)
    except FileNotFoundError:
        return {'success': False, 'message': '聊天记录文件不存在'}, 404
    except json.JSONDecodeError:
        return {'success': False, 'message': '聊天记录文件格式错误'}, 500
    except Exception as e:
        return {'success': False, 'message': f'导出失败: {str(e)}'}, 500

@app.route('/profile')
def user_profile():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (session['username'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)
    
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login_page'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        
        conn = get_db_connection()
        try:
            conn.execute('UPDATE users SET email = ? WHERE username = ?', 
                        (email, session['username']))
            conn.commit()
            flash('资料更新成功', 'success')
            return redirect(url_for('user_profile'))
        except Exception as e:
            conn.rollback()
            flash(f'更新失败: {str(e)}', 'danger')
        finally:
            conn.close()
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (session['username'],)).fetchone()
    conn.close()
    return render_template('edit_profile.html', user=user)
    
@app.route('/profile_info/<username>')
def profile_info(username):
    if 'username' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': '无权限执行此操作'}, 403
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if not user:
        return {'success': False, 'message': '用户不存在'}, 404
    
    return {
        'success': True,
        'user': {
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    }

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('chat.html', username=session['username'])

@app.route('/api/chat', methods=['POST'])
def api_chat():
    if 'username' not in session:
        return {'success': False, 'message': '请先登录'}, 401
    
    data = request.get_json()
    if not data or 'message' not in data:
        return {'success': False, 'message': '无效的请求数据'}, 400
    
    from siliconflow import SiliconFlowChat
    from config import API_CONFIG
    chatbot = SiliconFlowChat(API_CONFIG["api_key"])
    response = chatbot.get_response(data["message"])
    
    # 记录问答到知识库
    try:
        knowledge_base.add_record(data["message"], response, session['username'])
    except Exception as e:
        print(f"知识库记录失败: {str(e)}")
    
    return {
        'success': True,
        'response': response
    }


@app.route('/admin/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    if 'username' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': '无权限执行此操作'}, 403
    
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        return {'success': True, 'message': '用户删除成功'}
    except Exception as e:
        conn.rollback()
        return {'success': False, 'message': f'删除失败: {str(e)}'}, 500
    finally:
        conn.close()

@app.route('/admin/edit_user/<username>', methods=['PUT'])
def edit_user(username):
    if 'username' not in session or session.get('role') != 'admin':
        return {'success': False, 'message': '无权限执行此操作'}, 403
    
    data = request.json
    conn = get_db_connection()
    try:
        # 更新用户名时需要检查是否已存在
        if 'new_username' in data and data['new_username'] != username:
            existing = conn.execute('SELECT * FROM users WHERE username = ?', 
                                  (data['new_username'],)).fetchone()
            if existing:
                return {'success': False, 'message': '用户名已存在'}, 400
        
        # 构建更新语句
        update_fields = []
        update_values = []
        
        if 'new_username' in data:
            update_fields.append('username = ?')
            update_values.append(data['new_username'])
        if 'email' in data:
            update_fields.append('email = ?')
            update_values.append(data['email'])
        if 'role' in data:
            update_fields.append('role = ?')
            update_values.append(data['role'])
        if 'password' in data:
            update_fields.append('password = ?')
            update_values.append(generate_password_hash(data['password']))
        
        if not update_fields:
            return {'success': False, 'message': '没有提供更新字段'}, 400
            
        update_values.append(username)
        update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE username = ?"
        
        conn.execute(update_query, update_values)
        conn.commit()
        return {'success': True, 'message': '用户信息更新成功'}
    except Exception as e:
        conn.rollback()
        return {'success': False, 'message': f'更新失败: {str(e)}'}, 500
    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)