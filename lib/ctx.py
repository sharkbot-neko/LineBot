from linepy import *

class Context:
    def __init__(self, line: LINE, receiver, contact, group, prefix: str):
        self.line = line
        self.receiver = receiver
        self.contact = contact
        self.group = group
        self.prefix = prefix
        pass

    def send(self, message: str):
        self.line.sendMessage(self.receiver, message)