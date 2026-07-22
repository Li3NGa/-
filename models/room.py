from datetime import datetime, UTC
from app import db


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), default='')
    password = db.Column(db.String(128), default='')
    creator = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creator': self.creator,
            'created_at': self.created_at.isoformat()
        }


class RoomMember(db.Model):
    __tablename__ = 'room_members'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    user_uuid = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), default='member')
