import asyncio
import atexit
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

import QuestionAnswer

from TGLogin import GetClient

messageCount = 2659185 + 300

PeerChannelName = "Pornemby 【考研交流群】"


async def main():
    # client = TelegramClient('raynou', api_id, api_hash)
    # client = TelegramClient('kaikai', api_id, api_hash)
    client = GetClient('kaikai')
    await client.start()
    dialogs = await client.get_dialogs()
    print(dialogs)
    PeerChannel = None
    for dialog in dialogs:
        if dialog and dialog.name and PeerChannelName in dialog.name:
            PeerChannel = dialog.entity
            break
    message_id = 0
    messages = await client.get_messages(PeerChannel, limit=1)
    if messages and isinstance(messages, list) and messages[0]:
        messages = messages[0]
    message_id = messages.id
    for index in range(0, messageCount):
        # message = await client.get_messages(PeerChannel(channel_id=1464166236), ids=messageCount - index)
        message = await client.get_messages(PeerChannel, ids=message_id - index)
        # print(message)
        if message and message.message and len(message.message) > 5:
            QuestionAnswer.writeQuestionAnswerJson(message.message)
        # await asyncio.sleep(0.1)
        if message and message.sender and message.sender.username and "bot" in message.sender.username:
            print(message.sender.username)
        if index % 200 == 0:
            QuestionAnswer.writeQuestionAnswerJsonToFile()
        if message and message.id:
            print("当前message_id:{}".format(message.id))
    QuestionAnswer.writeQuestionAnswerJsonToFile()
    print("终于扫描完了以前所有问题")


def exitFunc():
    print("关闭回调")
    QuestionAnswer.writeQuestionAnswerJsonToFile()


atexit.register(exitFunc)
asyncio.run(main())
