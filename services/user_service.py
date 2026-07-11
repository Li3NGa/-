from utils.nickname import generate_nickname


class UserService:
    def create_anonymous_user(self):
        return generate_nickname()
