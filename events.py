from flask_socketio import send


def register_socket_events(socketio):
    @socketio.on('message')
    def handle_message(message):
        send(message, broadcast=True)
