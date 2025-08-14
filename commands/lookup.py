from lib.ctx import Context
import random

name="lookup"

def run(ctx: Context, args: list[str]):
    if not args:
        target_contact = ctx.contact
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
        mid = target_contact.mid
        created_time = getattr(target_contact, "createdTime", "不明")
        status_message = getattr(target_contact, "statusMessage", "なし")
        picture_url = ctx.line.getProfilePictureURL(mid)

        info_text = (
            f"{display_name} さんの情報\n"
            f"・MID: {mid}\n"
            f"・作成時刻: {created_time}\n"
            f"・ステータスメッセージ: {status_message}\n"
            f"・プロフィール画像: {picture_url}"
        )

        ctx.line.sendMessage(ctx.receiver, info_text)
    except Exception as e:
        ctx.line.sendMessage(ctx.receiver, f"詳細情報の取得に失敗しました")