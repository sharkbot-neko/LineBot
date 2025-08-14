# -*- coding: utf-8 -*-
from linepy import *
import time
import dotenv
import os
import random
import sqlite3
from make_db import make_db

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
        if name == 'help':
            line.sendMessage(receiver, f'''                                
基本的な機能のヘルプ
{prefix}help .. ヘルプを表示します。
{prefix}test .. 起動しているかを確認します。
{prefix}lookup <mid> .. 実行した人・ユーザーの情報を取得します。
{prefix}owner .. グループのオーナー情報を見ます。

面白い機能のヘルプ
{prefix}omikuji .. おみくじを引きます。

設定関連のヘルプ
{prefix}change_prefix [頭文字] .. 頭文字を変更します。
''')

        elif name == 'test':
            line.sendMessage(receiver, 'しっかり起動しています！')

        elif name == 'change_prefix':
            if sender == owner_mid:
                if not args:
                    line.sendMessage(receiver, '頭文字変更の使い方\n!change_prefix [頭文字]')
                else:
                    try:
                        new_prefix = args[0]
                        cur.execute(
                            "INSERT OR REPLACE INTO prefix (group_id, prefix) VALUES (?, ?)",
                            (receiver, new_prefix)
                        )
                        conn.commit()
                        line.sendMessage(receiver, f'頭文字が {new_prefix} に変更されました。')
                    except Exception as e:
                        line.sendMessage(receiver, f'エラーが発生しました')


        elif name == 'owner':
            try:
                target_contact = line.getContact(owner_mid)
                display_name = target_contact.displayName
                mid = target_contact.mid
                created_time = getattr(target_contact, "createdTime", "不明")
                status_message = getattr(target_contact, "statusMessage", "なし")
                picture_url = line.getProfilePictureURL(mid)

                info_text = (
                    f"{display_name} さんの情報\n"
                    f"・MID: {mid}\n"
                    f"・作成時刻: {created_time}\n"
                    f"・ステータスメッセージ: {status_message}\n"
                    f"・プロフィール画像: {picture_url}"
                )

                line.sendMessage(receiver, info_text)
            except Exception as e:
                line.sendMessage(receiver, f"詳細情報の取得に失敗しました: {e}")

        elif name == 'lookup':
            if not args:
                target_contact = contact
            else:
                target = " ".join(args)
                try:
                    if target.startswith("u") and len(target) >= 32:
                        target_contact = line.getContact(target)
                    else:
                        group = line.getGroup(receiver)
                        found = [m for m in group.members if target in m.displayName]
                        if not found:
                            line.sendMessage(receiver, "ユーザーが見つかりません。")
                            return
                        target_contact = found[0]
                except Exception:
                    line.sendMessage(receiver, f"情報を取得できませんでした")
                    return

            try:
                display_name = target_contact.displayName
                mid = target_contact.mid
                created_time = getattr(target_contact, "createdTime", "不明")
                status_message = getattr(target_contact, "statusMessage", "なし")
                picture_url = line.getProfilePictureURL(mid)

                info_text = (
                    f"{display_name} さんの情報\n"
                    f"・MID: {mid}\n"
                    f"・作成時刻: {created_time}\n"
                    f"・ステータスメッセージ: {status_message}\n"
                    f"・プロフィール画像: {picture_url}"
                )

                line.sendMessage(receiver, info_text)
            except Exception as e:
                line.sendMessage(receiver, f"詳細情報の取得に失敗しました")

        elif name == 'omikuji':
            line.sendMessage(receiver, f'今日の運勢は・・？\n{random.choice(["凶", "吉", "小吉", "大吉", "中吉"])}です！')

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