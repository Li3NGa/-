from services.chat_service import ChatService


def test_add_message():
    service = ChatService()
    result = service.add_message('user', 'hello')
    assert result['content'] == 'hello'
