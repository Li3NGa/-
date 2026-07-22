from flask import Blueprint, jsonify, request
from models.message import Message

message_bp = Blueprint('messages', __name__)


@message_bp.route('/api/messages/<int:room_id>', methods=['GET'])
def room_messages(room_id):
    limit = request.args.get('limit', 100, type=int)

    messages = Message.query.filter_by(room_id=room_id).order_by(Message.id.desc()).limit(limit).all()
    return jsonify([m.to_dict() for m in reversed(messages)])


@message_bp.route('/api/history', methods=['GET'])
def history():
    limit = request.args.get('limit', 100, type=int)

    messages = Message.query.order_by(Message.id.desc()).limit(limit).all()
    return jsonify([m.to_dict() for m in reversed(messages)])