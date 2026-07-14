from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
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

socketio = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)

users = {}
user_rooms = {}
message_rate = {}


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), default='')
    creator = db.Column(db.String(32), default='匿名用户')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(32))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('rooms.html')


@app.route('/chat/<int:room_id>')
def chat(room_id):
    return render_template('index.html', room_id=room_id)


@app.route('/api/rooms')
def rooms():
    return jsonify([
        {
            'id': r.id,
            'name': r.name,
            'description': r.description
        }
        for r in Room.query.all()
    ])


@app.route('/api/rooms/create', methods=['POST'])
def create_room():
    data = request.json or {}
    room = Room(
        name=data.get('name', '匿名聊天室'),
        description=data.get('description', '')
    )
    db.session.add(room)
    db.session.commit()
    return jsonify({'id': room.id, 'name': room.name})


@socketio.on('connect')
def connect():
    username = f'游客{random.randint(1000,9999)}'
    users[request.sid] = username
    emit('user_info', {'username': username})


@socketio.on('join_room')
def handle_join(data):
    room_id = str(data.get('room_id'))
    username = users.get(request.sid, '匿名用户')
    join_room(room_id)
    user_rooms[request.sid] = room_id

    history = Message.query.filter_by(room_id=int(room_id)).order_by(Message.id.desc()).limit(50).all()
    emit('room_history', [
        {'username': m.username, 'content': m.content}
        for m in reversed(history)
    ])

    emit('system_message', {'message': f'{username} 加入聊天室'}, room=room_id)


@socketio.on('send_message')
def send_message(data):
    room_id = user_rooms.get(request.sid)
    if not room_id:
        return

    username = users.get(request.sid, '匿名用户')
    content = html.escape(str(data.get('content', '')))[:500]

    if not content:
        return

    last = message_rate.get(request.sid, 0)
    if time.time() - last < 1:
        return
    message_rate[request.sid] = time.time()

    db.session.add(Message(
        room_id=int(room_id),
        username=username,
        content=content
    ))
    db.session.commit()

    emit('new_message', {
        'username': username,
        'content': content
    }, room=room_id)


@socketio.on('disconnect')
def disconnect():
    users.pop(request.sid, None)
    user_rooms.pop(request.sid, None)
    message_rate.pop(request.sid, None)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
