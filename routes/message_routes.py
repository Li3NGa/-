from flask import Blueprint, jsonify, request

from services.chat_service import ChatService

message_bp = Blueprint('messages', __name__)
chat_service = ChatService()


@message_bp.route('/api/messages/<room_id>', methods=['GET'])
def room_messages(room_id):
    limit = request.args.get('limit', 100, type=int)

    return jsonify(
        chat_service.get_messages(room_id, limit)
    )
