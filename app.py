from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import html
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'anonymous-chat-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
socketio = SocketIO(app, cors_allowed_origins='*', message_queue=redis_url)
db = SQLAlchemy(app)

users = {}
banned_users = set()
message_rate = {}

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history')
def history():
    messages = Message.query.order_by(Message.id.desc()).limit(50).all()
    return jsonify([
        {'user': m.username, 'text': m.content, 'time': m.created_at.isoformat()}
        for m in reversed(messages)
    ])

@app.route('/admin/users')
def admin_users():
    return jsonify({'online': list(users.values()), 'count': len(users)})

@app.route('/admin/ban/<user>')
def admin_ban(user):
    banned_users.add(user)
    return jsonify({'status': 'banned', 'user': user})

@socketio.on('connect')
def connect():
    username = f'游客{random.randint(1000,9999)}'
    users[request.sid] = username
    emit('system', f'{username} 加入聊天室', broadcast=True)
    emit('online_count', {'count': len(users)}, broadcast=True)

@socketio.on('message')
def message(data):
    username = users.get(request.sid, '匿名用户')

    if username in banned_users:
        return

    now = time.time()
    last = message_rate.get(request.sid, 0)
    if now - last < 1:
        emit('system', '发送过快，请稍后再试')
        return
    message_rate[request.sid] = now

    content = html.escape(str(data))[:500]
    if not content.strip():
        return

    db.session.add(Message(username=username, content=content))
    db.session.commit()

    emit('message', {
        'user': username,
        'text': content,
        'time': datetime.utcnow().isoformat()
    }, broadcast=True)

@socketio.on('set_nickname')
def set_nickname(name):
    if not name:
        return
    safe_name = html.escape(str(name))[:16]
    users[request.sid] = safe_name
    emit('system', f'用户修改昵称为 {safe_name}', broadcast=True)

@socketio.on('disconnect')
def disconnect():
    username = users.pop(request.sid, '匿名用户')
    message_rate.pop(request.sid, None)
    emit('system', f'{username} 离开聊天室', broadcast=True)
    emit('online_count', {'count': len(users)}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
