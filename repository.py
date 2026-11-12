from database import get_connection

class UserRepository:
    def get_by_email(self, email):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    def get_by_id(self, user_id):
        with get_connection() as conn:
            return conn.execute(
                "SELECT id, name, email, balance FROM users WHERE id = ?", (user_id,)
            ).fetchone()

    def create(self, name, email, password_hash):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users(name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash)
            )
            return cursor.lastrowid

class TransactionRepository:
    def for_user(self, user_id):
        with get_connection() as conn:
            return conn.execute("""
                SELECT t.*, s.name AS sender_name, r.name AS receiver_name
                FROM transactions t
                JOIN users s ON s.id = t.sender_id
                JOIN users r ON r.id = t.receiver_id
                WHERE t.sender_id = ? OR t.receiver_id = ?
                ORDER BY t.created_at DESC, t.id DESC
            """, (user_id, user_id)).fetchall()
