from linepy import *

from sqlite3 import Cursor, Connection

class Warns:
    def __init__(self, cur: Cursor, conn: Connection):
        self.cur = cur
        self.conn = conn

    def add_warn(self, groupid: str, mid: str):
        self.cur.execute("""
            INSERT INTO warns (group_id, id, score)
            VALUES (?, ?, 1)
            ON CONFLICT(group_id, id) DO UPDATE SET
                score = score + 1
        """, (groupid, mid))
        self.conn.commit()

    def get_warn(self, groupid: str, mid: str) -> int:
        self.cur.execute("SELECT score FROM warns WHERE group_id=? AND id=?", (groupid, mid))
        row = self.cur.fetchone()
        return row[0] if row else 0

    def reset_warn(self, groupid: str, mid: str):
        self.cur.execute("UPDATE warns SET score = 0 WHERE group_id=? AND id=?", (groupid, mid))
        self.conn.commit()