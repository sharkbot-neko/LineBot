from linepy import *

def run(line: LINE, op):
    try:
        group_id=op.param1
        line.acceptGroupInvitation(group_id)
    except Exception as e:
        line.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))