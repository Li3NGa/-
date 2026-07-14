from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    room_id: int
    username: str
    content: str
    created_at: datetime = datetime.now()

    def to_dict(self):
        return {
            'room_id': self.room_id,
            'username': self.username,
            'content': self.content,
            'time': self.created_at.isoformat()
        }
