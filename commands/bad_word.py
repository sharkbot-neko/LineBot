from lib.ctx import Context

name="bad_word"

def run(ctx: Context, args):
    if ctx.sender == ctx.owner_mid:
        if not args:
            ctx.line.sendMessage(ctx.receiver, '禁止ワード発言者処罰機能の使い方\n!bad_word [on/off]')
    else:
        try:
            onoff = args[0]
            if onoff == "on":
                ctx.cur.execute("INSERT OR REPLACE INTO badword (group_id) VALUES (?)", (ctx.receiver))
                ctx.conn.commit()
                ctx.line.sendMessage(ctx.receiver, f'禁止ワード発言者処罰機能がonになりました。')
            else:
                ctx.cur.execute("DELETE FROM badword WHERE group_id = ?", (ctx.receiver))
                ctx.conn.commit()
                ctx.line.sendMessage(ctx.receiver, f'禁止ワード発言者処罰機能がoffになりました。')
        except Exception as e:
            ctx.line.sendMessage(ctx.receiver, f'エラーが発生しました')