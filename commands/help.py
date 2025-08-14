from lib.ctx import Context

name="help"

def run(ctx: Context, args):
    ctx.send(f'''                                
基本的な機能のヘルプ
{ctx.prefix}help .. ヘルプを表示します。
{ctx.prefix}test .. 起動しているかを確認します。
{ctx.prefix}lookup <mid> .. 実行した人・ユーザーの情報を取得します。
{ctx.prefix}owner .. グループのオーナー情報を見ます。

面白い機能のヘルプ
{ctx.prefix}omikuji .. おみくじを引きます。

設定関連のヘルプ (グループオーナーのみ)
{ctx.prefix}change_prefix [頭文字] .. 頭文字を変更します。
''')