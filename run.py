#!/usr/bin/python3
import asyncio
import random
import sys
from datetime import time
import re
from telethon import TelegramClient, events

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
from telethon.tl.types import PeerChannel, PeerUser

from TGLogin import GetClient

'''
api信息

App configuration
App api_id:
15457318

App api_hash:
e272cc0355e4f19ae49900d8e578231e

App title:
Telethon
Short name:
Telethon
alphanumeric, 5-32 characters
Available MTProto servers
Test configuration:
149.154.167.40:443
DC 2
Public keys:
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAyMEdY1aR+sCR3ZSJrtztKTKqigvO/vBfqACJLZtS7QMgCGXJ6XIR
yy7mx66W0/sOFa7/1mAZtEoIokDP3ShoqF4fVNb6XeqgQfaUHd8wJpDWHcR2OFwv
plUUI1PLTktZ9uW2WE23b+ixNwJjJGwBDJPQEQFBE+vfmH0JP503wr5INS1poWg/
j25sIWeYPHYeOrFp/eXaqhISP6G+q2IeTaWTXpwZj4LzXq5YOpk4bYEQ6mvRq7D1
aHWfYmlEGepfaYR8Q0YqvvhYtMte3ITnuSJs171+GDqpdKcSwHnd6FudwGO4pcCO
j4WcDuXc2CTHgH8gFTNhp/Y8/SpDOhvn9QIDAQAB
-----END RSA PUBLIC KEY-----
Production configuration:
149.154.167.50:443
DC 2

'''

# api_id = 13197610
# api_hash = 'a21f42d8391234581435652ea1162ca7'

count = 0


async def main():
    # client = TelegramClient('cyounim_sing', api_id, api_hash)
    client = GetClient("cyounim_sing")
    await client.start()

    # 签到
    async def checkSing():
        # 💘粿粿|PornembyBot
        # PornEmby专属机器人，命令输入/start调用键盘，使用功能
        await client.send_message('PronembyTGBot2_bot', "/start")
        # await client.send_message(entity='💘粿粿|PornembyBot', message="/start")
        # 厂妹 发送签到信息
        await client.send_message('EmbyPublicBot', "/checkin")
        # 卷毛鼠 发送签到信息
        await client.send_message("@qweybgbot", "/checkin")
        print("发送签到指令完成")

    await checkSing()
    sys.exit()

asyncio.run(main())
