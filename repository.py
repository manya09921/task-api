import sqlite3


class SQLiteTaskRepository:
    """Handles all task storage using SQLite. Same methods will later
    be implemented by PostgresTaskRepository — routes never change."""

    def __init__(self, db_file="tasks.db"):
        self.db_file = db_file
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        cur.execute("SELECT COUNT(*) FROM tasks")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Buy groceries", False),
                    ("Finish assignment", False),
                    ("Read a book", True),
                ],
            )
        conn.commit()
        conn.close()

    def list_all(self):
        conn = self._get_connection()
        rows = conn.execute("SELECT * FROM tasks").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get(self, task_id: int):
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def create(self, title: str):
        conn = self._get_connection()
        cur = conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)", (title, False)
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return {"id": new_id, "title": title, "done": False}

    def update(self, task_id: int, title: str, done: bool):
        conn = self._get_connection()
        cur = conn.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (title, done, task_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            conn.close()
            return None
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        return dict(row)

    def delete(self, task_id: int) -> bool:
        conn = self._get_connection()
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return cur.rowcount > 0