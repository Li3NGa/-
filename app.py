from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anonymous-chat-secret'
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    username = f'游客{random.randint(1000, 9999)}'
    users[request.sid] = username
    emit('system', f'{username} 加入聊天室', broadcast=True)

@socketio.on('message')
def message(data):
    username = users.get(request.sid, '匿名用户')
    emit('message', {'user': username, 'text': data}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    username = users.pop(request.sid, '匿名用户')
    emit('system', f'{username} 离开聊天室', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
