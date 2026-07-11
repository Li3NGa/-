class RoomService:
    def __init__(self):
        self.rooms = {}

    def join_room(self, room_id, username):
        if room_id not in self.rooms:
            self.rooms[room_id] = []

        self.rooms[room_id].append(username)
        return self.rooms[room_id]

    def leave_room(self, room_id, username):
        if room_id in self.rooms and username in self.rooms[room_id]:
            self.rooms[room_id].remove(username)

        return self.rooms.get(room_id, [])

    def online_count(self, room_id):
        return len(self.rooms.get(room_id, []))
