from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import redis

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins='*')
limiter = Limiter(get_remote_address)

redis_client = None


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'anonymous-chat-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chat.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    limiter.init_app(app)

    redis_url = os.getenv('REDIS_URL')
    global redis_client
    try:
        redis_client = redis.Redis.from_url(redis_url) if redis_url else None
    except Exception:
        redis_client = None

    socketio.init_app(app, message_queue=redis_url)

    from routes.room_routes import room_bp
    from routes.message_routes import message_bp
    from admin.routes import admin_bp

    app.register_blueprint(room_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('rooms.html')

    @app.route('/chat/<int:room_id>')
    def chat(room_id):
        from flask import render_template
        return render_template('index.html', room_id=room_id)

    from events import register_socket_events
    register_socket_events(socketio)

    with app.app_context():
        db.create_all()

    return app


app = create_app()