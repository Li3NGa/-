from flask_socketio import emit, join_room, leave_room

from services.user_service import UserService
from services.room_service import RoomService
from services.chat_service import ChatService

user_service = UserService()
room_service = RoomService()
chat_service = ChatService()

users = {}


def register_socket_events(socketio):

    @socketio.on('connect')
    def handle_connect():
        username = user_service.create_anonymous_user()
        users[username] = {'room': None}
        emit('user_info', {'username': username})

    @socketio.on('join_room')
    def handle_join(data):
        username = data.get('username')
        room_id = data.get('room_id', 'public')

        join_room(room_id)
        users.setdefault(username, {})['room'] = room_id
        room_service.join_room(room_id, username)

        emit('system_message', {
            'message': f'{username} joined {room_id}'
        }, room=room_id)

        emit('room_joined', {'room_id': room_id})

    @socketio.on('leave_room')
    def handle_leave(data):
        username = data.get('username')
        room_id = data.get('room_id', 'public')

        leave_room(room_id)
        room_service.leave_room(room_id, username)

        emit('system_message', {
            'message': f'{username} left {room_id}'
        }, room=room_id)

    @socketio.on('send_message')
    def handle_message(data):
        username = data.get('username')
        room_id = data.get('room_id', 'public')
        content = data.get('content')

        message = chat_service.add_message(username, content)
        emit('new_message', message, room=room_id)

    @socketio.on('get_online_users')
    def online_users(data):
        room_id = data.get('room_id', 'public')
        emit('online_count', {
            'count': room_service.online_count(room_id)
        })
