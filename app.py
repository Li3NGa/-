from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import uuid
import html
import time
import os
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'anonymous-chat-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chat.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

redis_url = os.getenv('REDIS_URL')
socketio = SocketIO(app, cors_allowed_origins='*', message_queue=redis_url)

db = SQLAlchemy(app)
limiter = Limiter(get_remote_address, app=app, default_limits=['200 per day', '50 per hour'])

users = {}
user_rooms = {}
message_rate = {}

try:
    redis_client = redis.Redis.from_url(redis_url) if redis_url else None
except Exception:
    redis_client = None


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(32), nullable=False)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), default='')


class RoomMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    user_uuid = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), default='member')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    user_uuid = db.Column(db.String(64))
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
    return jsonify([{'id': r.id, 'name': r.name, 'description': r.description} for r in Room.query.all()])


@app.route('/api/rooms/create', methods=['POST'])
@limiter.limit('10 per minute')
def create_room():
    data = request.json or {}
    room = Room(name=data.get('name', '匿名聊天室'), description=data.get('description', ''))
    db.session.add(room)
    db.session.commit()
    return jsonify({'id': room.id, 'name': room.name})


@socketio.on('connect')
def connect():
    user_uuid = str(uuid.uuid4())
    nickname = f'游客{user_uuid[:6]}'
    users[request.sid] = {'uuid': user_uuid, 'nickname': nickname}
    db.session.add(User(uuid=user_uuid, nickname=nickname))
    db.session.commit()
    emit('user_info', {'username': nickname, 'uuid': user_uuid})


@socketio.on('join_room')
def handle_join(data):
    room_id = str(data.get('room_id'))
    user = users.get(request.sid, {'uuid': '', 'nickname': '匿名用户'})
    join_room(room_id)
    user_rooms[request.sid] = room_id

    if redis_client:
        redis_client.sadd(f'room:{room_id}:users', user['uuid'])

    if user['uuid']:
        db.session.add(RoomMember(room_id=int(room_id), user_uuid=user['uuid'], role='member'))
        db.session.commit()

    online = redis_client.scard(f'room:{room_id}:users') if redis_client else 0
    emit('online_count', {'count': online}, room=room_id)

    history = Message.query.filter_by(room_id=int(room_id)).order_by(Message.id.desc()).limit(50).all()
    emit('room_history', [{'username': m.username, 'content': m.content, 'time': m.created_at.isoformat()} for m in reversed(history)])
    emit('system_message', {'message': f"{user['nickname']} 加入聊天室"}, room=room_id)


@socketio.on('typing')
def typing(data):
    room_id = user_rooms.get(request.sid)
    user = users.get(request.sid, {'nickname': '匿名用户'})
    if room_id:
        emit('user_typing', {'username': user['nickname'], 'typing': bool(data.get('typing'))}, room=room_id, include_self=False)


@socketio.on('send_message')
def send_message(data):
    room_id = user_rooms.get(request.sid)
    if not room_id:
        return

    user = users.get(request.sid, {'uuid': '', 'nickname': '匿名用户'})
    content = html.escape(str(data.get('content', '')))[:500]
    if not content:
        return

    if time.time() - message_rate.get(request.sid, 0) < 1:
        return
    message_rate[request.sid] = time.time()

    db.session.add(Message(room_id=int(room_id), user_uuid=user['uuid'], username=user['nickname'], content=content))
    db.session.commit()

    emit('new_message', {'username': user['nickname'], 'content': content}, room=room_id)


@socketio.on('disconnect')
def disconnect():
    room_id = user_rooms.get(request.sid)
    user = users.get(request.sid)
    if room_id:
        leave_room(room_id)
        if redis_client and user:
            redis_client.srem(f'room:{room_id}:users', user['uuid'])
    users.pop(request.sid, None)
    user_rooms.pop(request.sid, None)
    message_rate.pop(request.sid, None)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
