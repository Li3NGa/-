from datetime import datetime


class ChatService:
    def __init__(self):
        self.messages = []

    def add_message(self, username, content):
        message = {
            'username': username,
            'content': content,
            'time': datetime.now().isoformat()
        }
        self.messages.append(message)
        return message

    def get_messages(self):
        return self.messages
