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
from events import events
import events.RECEIVE_MESSAGE.event

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

def load_commands():
    commands_.clear()
    for cog in os.listdir("commands"):
        if cog.endswith(".py") and not cog.startswith("__"):
            mod_name = cog[:-3]
            module = importlib.import_module(f"commands.{mod_name}")
            importlib.reload(module)
            commands_[module.name] = module.run

load_commands()

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
        
        # メッセージイベント処理
        events.RECEIVE_MESSAGE.event.run(line, op)

        # メッセージからコマンドに変換
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

        # 管理者向けコマンド処理

        if name == "reload":
            if sender == os.environ.get("bot_owner_mid"):
                load_commands()
                line.sendMessage(receiver, "リロードしました。")

        elif name == "load":
            if sender == os.environ.get("bot_owner_mid"):
                load_commands()
                line.sendMessage(receiver, "ロードしました。")

        # コマンド処理

        ctx_ = ctx.Context(line, receiver, contact, group, sender, owner_mid, prefix, cur, conn)

        func = commands_.get(name, None)
        if func:
            func(ctx_, args)

    except Exception as e:
        line.log("[RECEIVE_MESSAGE] ERROR : " + str(e))

# コマンド登録
oepoll.addOpInterrupt(OpType.RECEIVE_MESSAGE, RECEIVE_MESSAGE)

# イベント登録
events.register(oepoll)

while True:
    oepoll.trace()