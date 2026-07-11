from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    username: str
    content: str
    created_at: datetime = datetime.now()
