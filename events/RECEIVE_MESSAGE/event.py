# イベント一覧を書く
import badword

from linepy import LINE
from sqlite3 import Cursor, Connection

def run(line: LINE, op, cur: Cursor, conn: Connection):
    badword.run(line, op, cur, conn)
    return