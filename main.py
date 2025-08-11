# -*- coding: utf-8 -*-
from linepy import *
import time
import dotenv
import os
import importlib

dotenv.load_dotenv()

line = LINE(os.environ.get("email"), os.environ.get("password"))
#line = LINE('AUTHTOKEN')

line.log("Auth Token : " + str(line.authToken))
line.log("Timeline Token : " + str(line.tl.channelAccessToken))

# Initialize OEPoll with LINE instance
oepoll = OEPoll(line)

cooldown_command = {}

# Receive messages from OEPoll
def RECEIVE_MESSAGE(op):
    '''
        This is sample for implement BOT in LINE group
        Invite your BOT to group, then BOT will auto accept your invitation
        Command availabe :
        > hi
        > /author
    '''
    msg = op.message
    
    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    
    try:
        # Check content only text message
        if msg.contentType == 0:
            # Check only group chat
            if msg.toType == 2:
                # Chat checked request
                line.sendChatChecked(receiver, msg_id)
                # Get sender contact
                contact = line.getContact(sender)

                if not isinstance(text, str):
                    return
                
                if not text.startswith("!"):
                    return
                
                commands = text.removeprefix("!")

                name = commands.split(" ")[0].lower()
                args = commands.split(" ")[1:] if len(commands) == 1 else []

                current_time = time.time()
                last_message_time = cooldown_command.get(sender, 0)
                if current_time - last_message_time < 5:
                    return
                cooldown_command[sender] = current_time

                # Command list
                if name == 'help':
                    line.sendMessage(receiver, '''                                
基本的なヘルプ
!help .. ヘルプを表示します。
!test .. 起動しているかを確認します。

検索のヘルプ
!lookup .. 実行した人・ユーザーの情報を取得します。
''')
                elif text.lower() == 'getargs':
                    line.sendMessage(receiver, '引数リスト:\n' + '\n'.join(args))

                elif text.lower() == 'test':
                    line.sendMessage(receiver, 'しっかり起動しています！')

                elif text.lower() == 'lookup':
                    line.sendMessage(receiver, f'{contact.displayName}さんの情報\nID: {contact.mid}\n作成時刻: {contact.createdTime}')

                else:
                    line.sendMessage(receiver, 'コマンドが見つかりません。\n!helpと入力してコマンド名を確認してください。')
    except Exception as e:
        line.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
    
# Auto join if BOT invited to group
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        group_id=op.param1
        # Accept group invitation
        line.acceptGroupInvitation(group_id)
    except Exception as e:
        line.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))

# Add function to OEPoll
oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})

while True:
    oepoll.trace()