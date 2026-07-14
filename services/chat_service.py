from datetime import datetime


class ChatService:
    def __init__(self):
        self.messages = {}

    def add_message(self, room_id, username, content):
        message = {
            'room_id': room_id,
            'username': username,
            'content': content,
            'time': datetime.now().isoformat()
        }

        if room_id not in self.messages:
            self.messages[room_id] = []

        self.messages[room_id].append(message)
        return message

    def get_messages(self, room_id, limit=100):
        return self.messages.get(room_id, [])[-limit:]
