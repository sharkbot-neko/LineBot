from lib.ctx import Context

name="change_prefix"

def run(ctx: Context, args):
    if ctx.sender == ctx.owner_mid:
        if not args:
            ctx.line.sendMessage(ctx.receiver, '頭文字変更の使い方\n!change_prefix [頭文字]')
            return
        try:
            new_prefix = args[0]
            ctx.cur.execute("INSERT OR REPLACE INTO prefix (group_id, prefix) VALUES (?, ?)", (ctx.receiver, new_prefix))
            ctx.conn.commit()
            ctx.line.sendMessage(ctx.receiver, f'頭文字が {new_prefix} に変更されました。')
        except Exception as e:
            ctx.line.sendMessage(ctx.receiver, f'エラーが発生しました')