from app import db
from datetime import datetime, UTC


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    nickname = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))