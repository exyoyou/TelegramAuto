#!/usr/bin/python3
import asyncio
import datetime
import os
import random
import re
import signal
import subprocess
import sys
import threading

from telethon.errors import ChatWriteForbiddenError, MessageIdInvalidError
from telethon.tl.custom import MessageButton

if sys.platform == "darwin":
    import playsound as playsound
from telethon import TelegramClient, events

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
from telethon.tl.types import PeerChannel, KeyboardButtonCallback

import QuestionAnswer

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

api_id = 13197610
api_hash = 'a21f42d8391234581435652ea1162ca7'

count = 0

pronEmbyGropChatId = -1001464166236

sendMessageContent = [
    "大佬们你们好呀！！",
    "大家多说话 等待红包吧",
    # "红包红包快快来",
    # "红包快来红包快来",
    "冒个泡 说我我还存在",
    "大哥们 你们好呀",
    "哥哥们你们好呀",
    "哈咯 大佬们你们好呀",
    "老师们你们好呀",
    "哈哈哈哈哈哈哈哈",
    "我来了 冒个泡呀",
    "哈哈哈哈哈哈",
    "狼友们你们好呀",
    "说句话证明我还在群里",
]

pronEmbyGropMessageCount = 0
sendMessageToEmbyGroupIs = False


def playMusic():
    def run():
        name = "redComing.mp3"
        # name = "notify.m4a"
        try:
            if sys.platform == "darwin":
                playsound.playsound(name)
            elif sys.platform == "linux":
                p = subprocess.Popen('play-audio ' + name, close_fds=True, stdout=subprocess.PIPE, preexec_fn=os.setsid,
                                     shell=True)  # 播放不影响其他代码操作
                # os.killpg(p.pid, signal.SIGUSR1)
                print("linux 播放红包声音完成")
        except subprocess.CalledProcessError as error:
            print("播放红包来了声音失败")

    thread = threading.Thread(target=run)
    thread.start()


async def main():
    client = TelegramClient('cyounim', api_id, api_hash)
    await client.start()
    global sendMessageToEmbyGroupIs, sendMessageContent

    async def onClickBtn(btn, text, errorCount=3):
        if isinstance(btn, list):
            for btn_s in btn:
                await onClickBtn(btn_s, text)
        # elif isinstance(btn, KeyboardButtonCallback):
        #     print("这是{}按钮".format("KeyboardButtonCallback"))
        #     if text in btn.text:
        #         # await btn.click()
        #         print("点击{}按钮没有成功 因为不知道怎么回调".format(btn.text))
        elif isinstance(btn, MessageButton):
            if text in btn.text:
                try:
                    await asyncio.sleep(0.4)
                    await btn.click()
                    print("点击{}按钮成功".format(btn.text))
                except MessageIdInvalidError:
                    print("点击按钮失败")
                    if errorCount > 0:
                        await onClickBtn(btn, text, errorCount - 1)

    async def sendMessageToEmbyGroup():
        global pronEmbyGropMessageCount, sendMessageToEmbyGroupIs
        if sendMessageToEmbyGroupIs:
            print("发送了问候消息到pronEmby")
            pronEmbyGropMessageCount = 0
            sendMessageToEmbyGroupIs = False
            try:
                # await client.send_message(PeerChannel(channel_id=1464166236),sendMessageContent[random.randint(0, len(sendMessageContent) - 1)])
                print("暂时不发")
            except():
                print("发送消息错误")

                # print((await client.get_me()).stringify())

    # EmbyGroup 问题的 走这个方法 回答和存储新问题答案
    async def emby_group_question_answer(event):
        message = event.message
        if event.chat_id == pronEmbyGropChatId:
            print(event)
            if re.match(r"问题\d+：", message.message):
                # await client.send_message(PeerChannel(channel_id=1464166236), "A")
                print("自动回复 问题：{}".format(message.message))
                answer = QuestionAnswer.GetQuestionAnswer(message.message)
                if answer and answer != "":
                    if message.message.find("A") != -1 or message.message.find("B") != -1 or message.message.find(
                            "C") != -1:
                        try:
                            await client.send_message(PeerChannel(channel_id=1464166236), answer)
                        except ChatWriteForbiddenError:
                            print("发送消息错误")
                else:
                    if message.message.find("A") != -1 or message.message.find("B") != -1 or message.message.find(
                            "C") != -1:
                        try:
                            await client.send_message(PeerChannel(channel_id=1464166236), "A")
                        except ChatWriteForbiddenError:
                            print("发送消息错误")
                QuestionAnswer.writeQuestionAnswerJson(message.message)

    # await client.send_message('EmbyPublicBot', '/checkin')

    # print(botvalue.stringify())
    # await client.send_file('username', '/home/myself/Pictures/holidays.jpg')
    # await client.download_profile_photo('me')
    # messages = await client.get_messages('EmbyPublicBot')
    # print(messages)
    # await messages[0].download_media()
    # @client.on(events.NewMessage(from_users="EmbyPublicBot"))

    # gaoxiao123 = await client.get_messages('gaoxiao123', 100)

    # print(gaoxiao123)
    # for message in gaoxiao123:
    #     print(message)
    #     files = message.file
    #     if files:
    #         print(files)
    #         def progress_callback(file, progress):
    #             if (file == progress):
    #                 print(files.name + "下载完毕。。。。。。")
    # 
    #         await client.download_media(message=message, file=files.name, progress_callback=progress_callback)

    # 签到
    async def checkSing():
        # 💘粿粿|PornembyBot
        # PornEmby专属机器人，命令输入/start调用键盘，使用功能
        await client.send_message('PronembyTGBot2_bot', "/start")
        # await client.send_message(entity='💘粿粿|PornembyBot', message="/start")

        # 厂妹 发送签到信息
        await client.send_message('EmbyPublicBot', "/checkin")
        print("发送签到指令完成")

    # await checkSing()
    async def new_msg_event_handler(event: events.NewMessage.Event):
        global count, pronEmbyGropMessageCount
        message = event.message
        # 判断是否是群组或者频道发送的消息   
        # if event.is_channel:
        #     # to_id = message.to_id.channel_id
        #     # to_id = message.to_id.chat_id
        #     # if 1241168082 == to_id:
        #     # to_id = message.peer_id
        #     print('is_channel')
        # if event.is_group:
        #     ## 获取消息的id，
        #     print("is_group")
        # if event.chat_id != -1001241168082:
        # print(message)

        # print(event.chat_id)
        # print(message.message)
        if event.chat_id == 1996836328:  # 💘粿粿|PornembyBot 的回复
            await client.send_read_acknowledge(event.chat_id, message)
            if message.buttons:
                await onClickBtn(message.buttons, '签到')

            # if message.buttons and message.buttons[0] and message.buttons[0][1]:
            #     await message.buttons[0][1].click()
            #     count += 1
        elif event.chat_id == 1429576125:  # 厂妹 @EmbyPublicBot
            if message.message.find("你今天已经签到过了") != -1:
                count += 1
                # print(message.message)
            else:
                # print("EmbyPublicBot 可以签到")
                numbers = re.findall(r"\d+", message.message)
                number = int(numbers[0]) + int(numbers[1])
                await onClickBtn(message.buttons, str(number))
                await client.send_read_acknowledge(event.chat_id, message)
        elif event.chat_id == pronEmbyGropChatId:
            # print(event)
            pronEmbyGropMessageCount += 1
            if re.match(r"问题\d+：", message.message):
                await emby_group_question_answer(event)
            # elif message.reply_markup and message.reply_markup.rows and message.reply_markup.rows[0]:
            #     buttons = message.reply_markup.rows[0].buttons
            #     for btn in buttons:
            #         if btn.text == "点击领取红包奖励":
            #             btn = buttons[0]
            #             await btn.click()
            #             print("抢红包点击成功")
            #             playMusic()
            elif "一大波红包来袭中" in message.message:
                playMusic()

            if message.button_count > 0:
                await onClickBtn(message.buttons, '领取红包')

        if pronEmbyGropMessageCount >= 100:
            global sendMessageToEmbyGroupIs
            sendMessageToEmbyGroupIs = True
            await sendMessageToEmbyGroup()
        # if count >= 2:
        #     sys.exit()

    # 编辑信息
    async def edit_msg_event_handler(event: events.MessageEdited.Event):
        message = event.message
        if event.chat_id == pronEmbyGropChatId:
            print(event)
            if re.match(r"问题\d+：", message.message):
                await emby_group_question_answer(event)

            if message.button_count > 0:
                await onClickBtn(message.buttons, '领取红包')

    client.add_event_handler(callback=new_msg_event_handler,
                             event=events.NewMessage(incoming=True)
                             # event=events.NewMessage(from_users="EmbyPublicBot")
                             )

    client.add_event_handler(callback=edit_msg_event_handler,
                             event=events.MessageEdited(incoming=True)
                             # event=events.NewMessage(from_users="EmbyPublicBot")
                             )
    # await checkSing()
    while 1:
        # with client:
        #     client.loop.run_until_complete(main())
        # await asyncio.sleep(24 * 60 * 60)
        # await checkSing()
        # print('sleep')
        await asyncio.sleep(60 * 60)
        await asyncio.sleep(random.randint(1, 400))
        sendMessageToEmbyGroupIs = True
        await sendMessageToEmbyGroup()


print(datetime.datetime.now())
playMusic()
print(datetime.datetime.now())
asyncio.run(main())
