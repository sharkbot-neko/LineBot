from linepy import LINE

from files.bad_word import BADWORDS

from sqlite3 import Cursor, Connection
import time

cooldown = {}

def run(line: LINE, op, cur: Cursor, conn: Connection):
    try:
        msg = op.message
        text = msg.text
        msg_id = msg.id
        receiver = msg.to
        sender = msg._from

        if sender == line.profile.mid:
            return

        if msg.contentType != 0:
            return
        if msg.toType != 2:
            return

        cur.execute("SELECT group_id FROM badword WHERE group_id = ?", (receiver,))
        row = cur.fetchone()
        if row:
            for b in BADWORDS:
                if b in text:

                    cooldown_key = f"{sender}"
                    current_time = time.time()
                    last_message_time = cooldown.get(cooldown_key, 0)
                    if current_time - last_message_time < 5:
                        return
                    cooldown[cooldown_key] = current_time

                    line.sendMessage(receiver, f'禁止ワードを発言しないでください！')
                    return
            
            return
        else:
            return
    except Exception as e:
        print(f"禁止ワードエラー: {e}")