import asyncio
import atexit

from telethon import TelegramClient
from telethon.tl.types import PeerChannel

import QuestionAnswer

# api_id = 13197610
# api_hash = 'a21f42d8391234581435652ea1162ca7'
api_id = 13595884
api_hash = '03849446e0382cc148d2365d642a2d91'
count = 0

messageCount = 2659185 + 300

PeerChannelName = "Pornemby 【考研交流群】"


async def main():
    # client = TelegramClient('raynou', api_id, api_hash)
    client = TelegramClient('kaikai', api_id, api_hash)
    await client.start()
    message_id = 0
    messages = await client.get_messages(PeerChannelName, limit=1)
    if messages and isinstance(messages, list) and messages[0]:
        messages = messages[0]
    message_id = messages.id
    for index in range(0, messageCount):
        # message = await client.get_messages(PeerChannel(channel_id=1464166236), ids=messageCount - index)
        message = await client.get_messages("Pornemby 【考研交流群】", ids=message_id - index)
        # print(message)
        if message and message.message and len(message.message) > 5:
            QuestionAnswer.writeQuestionAnswerJson(message.message)
        # await asyncio.sleep(0.1)
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
