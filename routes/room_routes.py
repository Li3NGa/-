from flask import Blueprint, request, jsonify
from models.room import Room
from app import db, limiter

room_bp = Blueprint('rooms', __name__)


@room_bp.route('/api/rooms', methods=['GET'])
def list_rooms():
    rooms = Room.query.order_by(Room.id.desc()).all()
    return jsonify([r.to_dict() for r in rooms])


@room_bp.route('/api/rooms/create', methods=['POST'])
@limiter.limit('10 per minute')
def create_room():
    data = request.json or {}

    room = Room(
        name=data.get('name', '匿名聊天室'),
        description=data.get('description', ''),
        password=data.get('password', ''),
        creator=data.get('creator', '匿名用户')
    )

    db.session.add(room)
    db.session.commit()

    return jsonify(room.to_dict())