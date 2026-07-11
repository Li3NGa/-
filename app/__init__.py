from flask import Flask
from flask_socketio import SocketIO
from config import Config

socketio = SocketIO(cors_allowed_origins='*')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    socketio.init_app(app)

    from routes import register_routes
    register_routes(app)

    from events import register_socket_events
    register_socket_events(socketio)

    return app
