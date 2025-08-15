from lib.ctx import Context
from lib.warns import Warns

name="warn"

def run(ctx: Context, args):
    if ctx.sender == ctx.owner_mid:
        if not args:
            ctx.line.sendMessage(ctx.receiver, '警告の使い方\n!warn [mid]')
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
            Warns(ctx.cur, ctx.conn).add_warn(ctx.receiver, target_contact.mid)
            ctx.line.sendMessage(ctx.receiver, f"{display_name}を警告しました。")
        except:
            return