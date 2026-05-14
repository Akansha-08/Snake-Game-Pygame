import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("database/leaderboard.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score INTEGER
            )
        """)

        self.conn.commit()

    def add_score(self, name, score):
        self.cursor.execute(
            "INSERT INTO leaderboard (name, score) VALUES (?, ?)",
            (name, score)
        )
        self.conn.commit()

    def clear_leaderboard(self):
        self.cursor.execute("DELETE FROM leaderboard")
        self.conn.commit()

    def get_top_scores(self, limit=5):
        self.cursor.execute(
            "SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT ?",
            (limit,)
        )
        return self.cursor.fetchall()