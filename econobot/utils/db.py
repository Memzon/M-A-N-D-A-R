import sqlite3
import threading


class Database:
    """Basit ve thread-safe SQLite tabanlı ekonomi veritabanı."""

    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.RLock()
        self._setup()

    def _setup(self):
        with self.lock:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER NOT NULL DEFAULT 0,
                    chests_opened INTEGER NOT NULL DEFAULT 0,
                    speed_wins INTEGER NOT NULL DEFAULT 0,
                    total_earned INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            self.conn.commit()

    def _ensure_user(self, user_id: int):
        self.conn.execute(
            "INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)", (user_id,)
        )

    def get_balance(self, user_id: int) -> int:
        with self.lock:
            self._ensure_user(user_id)
            self.conn.commit()
            cur = self.conn.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            return cur.fetchone()[0]

    def add_balance(self, user_id: int, amount: int, *, chest: bool = False, speed: bool = False):
        with self.lock:
            self._ensure_user(user_id)
            self.conn.execute(
                "UPDATE users SET balance = balance + ?, total_earned = total_earned + ? WHERE user_id=?",
                (amount, max(amount, 0), user_id),
            )
            if chest:
                self.conn.execute(
                    "UPDATE users SET chests_opened = chests_opened + 1 WHERE user_id=?", (user_id,)
                )
            if speed:
                self.conn.execute(
                    "UPDATE users SET speed_wins = speed_wins + 1 WHERE user_id=?", (user_id,)
                )
            self.conn.commit()

    def set_balance(self, user_id: int, amount: int):
        with self.lock:
            self._ensure_user(user_id)
            self.conn.execute("UPDATE users SET balance=? WHERE user_id=?", (amount, user_id))
            self.conn.commit()

    def leaderboard(self, limit: int = 10):
        with self.lock:
            cur = self.conn.execute(
                "SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,)
            )
            return cur.fetchall()

    def stats(self, user_id: int):
        with self.lock:
            self._ensure_user(user_id)
            self.conn.commit()
            cur = self.conn.execute(
                "SELECT balance, chests_opened, speed_wins, total_earned FROM users WHERE user_id=?",
                (user_id,),
            )
            return cur.fetchone()
