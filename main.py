# -*- coding: utf-8 -*-
from linepy import *
import time
import dotenv
import os
import random
import sqlite3
from make_db import make_db
from lib import ctx, db
import importlib

dotenv.load_dotenv()

line = LINE(os.environ.get("email"), os.environ.get("password"))
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))
line.log("Timeline Token : " + str(line.tl.channelAccessToken))

oepoll = OEPoll(line)

cooldown_command = {}

make_db()

dbname = 'SAVE.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# いろいろ一覧
commands_ = {}

for cog in os.listdir("commands"):
    if cog.endswith(".py") and not cog.startswith("__"):
        mod_name = cog[:-3]
        imp = importlib.import_module(f"commands.{mod_name}")
        commands_[imp.name] = imp.run

def get_prefix(group_id):
    cur.execute("SELECT prefix FROM prefix WHERE group_id = ?", (group_id,))
    row = cur.fetchone()
    return row[0] if row else "!"

def RECEIVE_MESSAGE(op):
    msg = op.message
    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from

    try:
        if msg.contentType != 0:
            return
        if msg.toType != 2:
            return
        if not isinstance(text, str):
            return
        
        prefix = get_prefix(receiver)

        if not text.startswith(prefix):
            return

        commands = text.removeprefix(prefix)
        name = commands.split(" ")[0].lower()
        args = commands.split(" ")[1:] if len(commands.split(" ")) > 1 else []

        cooldown_key = f"{sender}:{name}"
        current_time = time.time()
        last_message_time = cooldown_command.get(cooldown_key, 0)
        if current_time - last_message_time < 5:
            return
        cooldown_command[cooldown_key] = current_time

        contact = line.getContact(sender)
        group = line.getGroup(receiver)
        owner_mid = group.creator.mid

        # ===== コマンド =====

        ctx_ = ctx.Context(line, receiver, contact, group, sender, owner_mid, prefix, cur, conn)

        func = commands_.get(name, None)
        if func:
            func(ctx_, args)

    except Exception as e:
        line.log("[RECEIVE_MESSAGE] ERROR : " + str(e))

def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        group_id=op.param1
        line.acceptGroupInvitation(group_id)
    except Exception as e:
        line.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))

oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})

while True:
    oepoll.trace()