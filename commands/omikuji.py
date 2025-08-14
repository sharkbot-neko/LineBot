from lib.ctx import Context
import random

name="omikuji"

def run(ctx: Context, args):
    ctx.send(f'今日の運勢は・・？\n{random.choice(["凶", "吉", "小吉", "大吉", "中吉"])}です！')