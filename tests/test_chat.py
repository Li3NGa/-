import unittest

from app import create_app


class ChatTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            from app import db
            db.create_all()

    def test_history_api(self):
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)

    def test_rooms_api(self):
        response = self.client.get('/api/rooms')
        self.assertEqual(response.status_code, 200)

    def test_create_room(self):
        response = self.client.post('/api/rooms/create', json={'name': '测试房间'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()