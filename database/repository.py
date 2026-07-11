from database import get_connection


class MessageRepository:
    def save(self, username, content):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO messages(username, content) VALUES (?, ?)',
            (username, content)
        )

        conn.commit()
        conn.close()

    def all(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages')
        data = cursor.fetchall()
        conn.close()
        return data
