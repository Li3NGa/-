from services.user_service import UserService


def test_create_user():
    service = UserService()
    user = service.create_anonymous_user()
    assert user
