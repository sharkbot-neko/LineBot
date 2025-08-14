from lib.ctx import Context

name="owner"

def run(ctx: Context, args):
    try:
        target_contact = ctx.line.getContact(ctx.owner_mid)
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
        ctx.line.sendMessage(ctx.receiver, f"詳細情報の取得に失敗しました: {e}")