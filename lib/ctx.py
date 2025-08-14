from linepy import *

from sqlite3 import Cursor, Connection

class Context:
    def __init__(self, line: LINE, receiver, contact, group, sender, owner_mid, prefix: str, cur: Cursor, conn: Connection):
        self.line = line
        self.receiver = receiver
        self.contact = contact
        self.group = group
        self.owner_mid = owner_mid
        self.prefix = prefix
        self.sender = sender
        self.cur = cur
        self.conn = conn
        pass

    def send(self, message: str):
        self.line.sendMessage(self.receiver, message)

    def commit(self):
        self.conn.commit()