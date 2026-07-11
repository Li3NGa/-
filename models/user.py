from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    username: str
    created_at: datetime = datetime.now()
