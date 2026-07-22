from flask_socketio import emit, join_room, leave_room
from flask import request
from app import db, redis_client
from models.user import User
from models.room import Room
from models.message import Message
from utils.nickname import generate_nickname
import uuid
import html
import time

users = {}
user_rooms = {}
message_rate = {}


def register_socket_events(socketio):

    @socketio.on('connect')
    def handle_connect():
        user_uuid = str(uuid.uuid4())
        nickname = generate_nickname()
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
            from models.room import RoomMember
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