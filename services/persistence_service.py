from database.repository import MessageRepository


class PersistenceService:
    def __init__(self):
        self.repository = MessageRepository()

    def save_message(self, username, content):
        self.repository.save(username, content)
