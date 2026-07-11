class OnlineService:
    def __init__(self):
        self.users = {}

    def add_user(self, room_id, username):
        self.users.setdefault(room_id, set()).add(username)

    def remove_user(self, room_id, username):
        if room_id in self.users:
            self.users[room_id].discard(username)

    def count(self, room_id):
        return len(self.users.get(room_id, set()))
