from lib.ctx import Context
from lib.warns import Warns

name="warns"

def run(ctx: Context, args):
    if not args:
        ctx.line.sendMessage(ctx.receiver, '警告回数チェックの使い方\n!warns [mid]')
        return
    else:
        target = " ".join(args)
    try:
        if target.startswith("u") and len(target) >= 32:
            target_contact = ctx.line.getContact(target)
        else:
            group = ctx.line.getGroup(ctx.receiver)
            found = [m for m in group.members if target in m.displayName]
            if not found:
                ctx.line.sendMessage(ctx.receiver, "ユーザーが見つかりません。")
            return
        target_contact = found[0]
    except Exception:
        ctx.line.sendMessage(ctx.receiver, f"情報を取得できませんでした")
        return
    
    try:
        display_name = target_contact.displayName
        warns = Warns(ctx.cur, ctx.conn).get_warn(ctx.receiver, target_contact.mid)
        ctx.line.sendMessage(ctx.receiver, f"{display_name}の警告回数: {warns}回")
    except:
        return