from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anonymous-chat-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)

users = {}
banned_users = set()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

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

    content = html.escape(str(data))[:500]
    record = Message(username=username, content=content)
    db.session.add(record)
    db.session.commit()

    emit('message', {'user': username, 'text': content}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    username = users.pop(request.sid, '匿名用户')
    emit('system', f'{username} 离开聊天室', broadcast=True)
    emit('online_count', {'count': len(users)}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
