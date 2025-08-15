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

モデレーション機能のヘルプ (グループオーナーのみ)
{ctx.prefix}warn [mid] .. 警告をします。
{ctx.prefix}warns [mid] .. 警告回数を取得します。
{ctx.prefix}reset_warn [mid] .. 警告をリセットします。

設定関連のヘルプ (グループオーナーのみ)
{ctx.prefix}change_prefix [頭文字] .. 頭文字を変更します。
{ctx.prefix}bad_ward [on/off] .. 禁止ワード発言者を処罰するかを設定します。
''')