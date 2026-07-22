from app import db
from datetime import datetime, UTC


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    user_uuid = db.Column(db.String(64))
    username = db.Column(db.String(32))
    content = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'username': self.username,
            'content': self.content,
            'time': self.created_at.isoformat()
        }