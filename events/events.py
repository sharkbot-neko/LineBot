from linepy import *

# ここにフォルダ一覧を書く
from NOTIFIED_INVITE_INTO_GROUP import event

def register(oepoll: OEPoll):
    oepoll.addOpInterrupt(OpType.NOTIFIED_INVITE_INTO_GROUP, event.run)