import unittest

from app import app


class ChatTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_history_api(self):
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)

    def test_admin_api(self):
        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
