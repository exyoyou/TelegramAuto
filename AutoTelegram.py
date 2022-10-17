#!/usr/bin/python3
import asyncio
import atexit
import datetime
import os
import random
import re
import subprocess
import sys
import threading

# try:
#     import ddddocr
# except:
#     print("没有安装 ddddocr")

from telethon.errors import ChatWriteForbiddenError, MessageIdInvalidError
from telethon.tl.custom import MessageButton

import TGLogin

if sys.platform == "darwin":
    import playsound as playsound
from telethon import TelegramClient, events

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
from telethon.tl.types import PeerChannel, KeyboardButtonCallback, Channel

import QuestionAnswer

import requests

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

pronembyTitle = 'Pornemby 【考研交流群】'
pinYunEmbyTitle = '品云Emby'

sendContentInt = 100


class AutoTelegram(object):

    def print(self, *args):
        print("{}的打印内容:\n".format(self.name), *args)

    # api_id = 13197610
    # api_hash = 'a21f42d8391234581435652ea1162ca7'

    count = 0
    name = ''
    # pronEmby群的id
    pronEmbyGropChatId = -1001464166236
    # auto 发送到pronemby的消息列表
    sendPronEmbyMessageContent = [
        "大佬们你们好呀！！",
        "大家多说话 红包来的快",
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
        "emby 是我发现的新大陆",
    ]

    sendPinYunEmbyMessageContent = [
        "大佬们你们好呀！！",
        "冒个泡 说我我还存在",
        "大哥们 你们好呀",
        "哥哥们你们好呀",
        "哈咯 大佬们你们好呀",
        "老师们你们好呀",
        "哈哈哈哈哈哈哈哈",
        "我来了 冒个泡呀",
        "哈哈哈哈哈哈",
        "朋友们你们好呀",
        "说句话证明我还在群里",
        "品云666 大爱",
        "品云的大佬 你们好呀",
        "emby 是我发现的新大陆",
    ]

    pronEmbyGropMessageCount = 0
    sendMessageToEmbyGroupIs = False
    pronEmbyGroupObject = None
    sendMessageToPingYunGroupIs = False
    pinYunEmbyMessageCount = 0
    pingyunGroupObject = None

    def playMusic(self):
        def run():
            name = "redComing.mp3"
            # name = "notify.m4a"
            try:
                if sys.platform == "darwin":
                    playsound.playsound(name)
                elif sys.platform == "linux":
                    p = subprocess.Popen('play-audio ' + name, close_fds=True, stdout=subprocess.PIPE,
                                         preexec_fn=os.setsid,
                                         shell=True)  # 播放不影响其他代码操作
                    # os.killpg(p.pid, signal.SIGUSR1)
                    self.print("linux 播放红包声音完成")
            # except subprocess.CalledProcessError as error:
            except Exception as error:
                self.print("播放红包来了声音失败 error:{}".format(error))

        thread = threading.Thread(target=run)
        thread.start()

    async def main(self):
        # client = TelegramClient('cyounim', self.api_id, self.api_hash)name
        # client = TelegramClient(self.name, self.api_id, self.api_hash)
        tg_login = await TGLogin.TgLogin.create(self.name)
        # await client.start()
        client = tg_login.get_client()
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog and dialog.name and pinYunEmbyTitle == dialog.name:
                self.pingyunGroupObject = dialog.entity
                break

        for dialog in dialogs:
            if dialog and dialog.name and pronembyTitle == dialog.name:
                self.pronEmbyGroupObject = dialog.entity
                break

        async def onClickBtn(btn, text, errorCount=3):
            if isinstance(btn, list):
                for btn_s in btn:
                    await onClickBtn(btn_s, text)
            elif isinstance(btn, MessageButton):
                if btn and btn.text and text in btn.text:
                    try:
                        # await asyncio.sleep(0.1)
                        await btn.click()
                        self.print("点击{}按钮成功".format(btn.text))
                    except BaseException as error:
                        if errorCount > 0:
                            self.print("点击{}按钮失败 正在重试：{}".format(btn.text, errorCount))
                            # await onClickBtn(btn, text, errorCount=errorCount - 1)
                        else:
                            self.print("点击{}按钮失败 已经重试多次 还是失败 error:\n{}".format(btn.text, error))

        # 发送问候消息到品云
        async def sendPinYunEmbyGroup():
            if self.sendMessageToPingYunGroupIs and self.pinYunEmbyMessageCount > sendContentInt:
                self.pinYunEmbyMessageCount = 0
                self.sendMessageToPingYunGroupIs = False
                try:
                    content = self.sendPinYunEmbyMessageContent[
                        random.randint(0, len(self.sendPinYunEmbyMessageContent) - 1)]
                    await client.send_message(self.pingyunGroupObject, content)
                    self.print("发送了问候消息：{} 到品云".format(content))
                except Exception as error:
                    self.print("发送消息 品云 错误 {}".format(error))

        async def sendMessageToEmbyGroup():
            if self.sendMessageToEmbyGroupIs and self.pronEmbyGropMessageCount > sendContentInt:
                self.pronEmbyGropMessageCount = 0
                self.sendMessageToEmbyGroupIs = False
                try:
                    content = self.sendPronEmbyMessageContent[
                        random.randint(0, len(self.sendPronEmbyMessageContent) - 1)]
                    await client.send_message(self.pronEmbyGroupObject, content)
                    self.print("发送了问候消息 {} 到pronEmby".format(content))
                    # self.print("暂时不发")
                except():
                    self.print("发送消息 pronemby 错误")

                    # self.print((await client.get_me()).stringify())

        # EmbyGroup 问题的 走这个方法 回答和存储新问题答案
        async def emby_group_question_answer(event, resetSendCount=3):
            message = event.message
            if event.chat_id == self.pronEmbyGropChatId and message and message.sender and message.sender.username and "bot" in message.sender.username:
                if QuestionAnswer.getGetQuestionAnswerMatch(message.message):
                    # await client.send_message(PeerChannel(channel_id=1464166236), "A")
                    # self.print("自动回复 问题：{}".format(message.message))
                    answer, question = QuestionAnswer.GetQuestionAnswer(message.message)
                    if not answer or answer == "":
                        answer = "A"
                    else:
                        self.print("{} \n已经存在本地问题列表中\n答案为:{}".format(question, answer))
                    if message.message.find("A") != -1 or message.message.find("B") != -1 or message.message.find(
                            "C") != -1:
                        try:
                            await asyncio.sleep(1)
                            await client.send_message(event.chat, answer)
                            self.print("{} \n发送了答案：{}".format(message.message, answer))
                        except Exception as error:
                            resetSendCount = resetSendCount - 1
                            if resetSendCount > 0:
                                self.print("发送消息错误{} 正在从新发送 结果{}".format(resetSendCount, answer))
                                await emby_group_question_answer(event, resetSendCount)
                            else:
                                self.print("发送消息错误 已经重试多次依然失败 error{}".format(error))
                        QuestionAnswer.writeQuestionAnswerJson(message.message)

        # await client.send_message('EmbyPublicBot', '/checkin')

        # self.print(botvalue.stringify())
        # await client.send_file('username', '/home/myself/Pictures/holidays.jpg')
        # await client.download_profile_photo('me')
        # messages = await client.get_messages('EmbyPublicBot')
        # self.print(messages)
        # await messages[0].download_media()
        # @client.on(events.NewMessage(from_users="EmbyPublicBot"))

        # gaoxiao123 = await client.get_messages('gaoxiao123', 100)

        # self.print(gaoxiao123)
        # for message in gaoxiao123:
        #     self.print(message)
        #     files = message.file
        #     if files:
        #         self.print(files)
        #         def progress_callback(file, progress):
        #             if (file == progress):
        #                 self.print(files.name + "下载完毕。。。。。。")
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
            self.print("发送签到指令完成")

        # 卷毛鼠 机器人 签到回答
        async def run_qweybgbot(event):
            qweybgbot = "qweybgbot"
            message = event.message
            username = message.chat and message.chat.username or None
            if username != qweybgbot:
                return
            if "请回答下面的问题" in message.message:
                newline_index = message.message.find('\n')
                question_mark_index = message.message.find("?")
                text = message.message[newline_index + 1:question_mark_index]
                text = text[0:text.find("=") - 1]
                text.strip()
                numberAll = re.compile(r"\d+").findall(text)
                buttons = message.buttons
                if isinstance(buttons, list):
                    buttons = buttons[0]
                for button in buttons:
                    isClick = False
                    btn_num = int(button.text)
                    num_1 = int(numberAll[0])
                    num_2 = int(numberAll[1])
                    if btn_num == num_1 + num_2 or btn_num == num_1 - num_2 or btn_num == num_1 * num_2 or (
                            num_2 != 0 and btn_num == num_1 / num_2):
                        isClick = True
                    if isClick:
                        await button.click()
                        break
            elif "回答错误" in message.message:
                await client.send_message("@" + qweybgbot, "/checkin")
            elif "回答正确" in message.message:
                self.print("卷毛鼠签到成功")

        # await checkSing()
        async def new_msg_event_handler(event: events.NewMessage.Event):
            message = event.message
            await run_qweybgbot(event)
            # self.print(message)
            # 判断是否是群组或者频道发送的消息   
            # if event.is_channel:
            #     # to_id = message.to_id.channel_id
            #     # to_id = message.to_id.chat_id
            #     # if 1241168082 == to_id:
            #     # to_id = message.peer_id
            #     self.print('is_channel')
            # if event.is_group:
            #     ## 获取消息的id，
            #     self.print("is_group")
            # if event.chat_id != -1001241168082:
            # self.print(message)

            # self.print(event.chat_id)
            # self.print(message.message)
            if event.chat_id == 1996836328:  # 💘粿粿|PornembyBot 的回复
                # await client.send_read_acknowledge(EntityLike(id=event.chat_id), message)
                todayIsSing = True
                index = message.id - 1
                while True:
                    pornembyBotMessage = await client.get_messages(event.chat, ids=index)
                    index -= 1
                    if pornembyBotMessage:
                        dateDay = pornembyBotMessage.date.day
                        nowDay = datetime.datetime.now().day
                        if dateDay != nowDay:
                            break
                        if pornembyBotMessage.message and "已经签到" in pornembyBotMessage.message:
                            todayIsSing = False
                            break

                if todayIsSing and message.buttons:
                    await onClickBtn(message.buttons, '签到')

                # if message.buttons and message.buttons[0] and message.buttons[0][1]:
                #     await message.buttons[0][1].click()
                #     count += 1
            elif event.chat_id == 1429576125:  # 厂妹 @EmbyPublicBot
                if message.message.find("已经签到") != -1:
                    self.count += 1
                    # self.print(message.message)
                else:
                    if "验证码" in message.message:
                        answer = ""
                        # if ddddocr:
                        #     answer = "AC"
                        # await client.send_message(event.chat_id, answer)
                    elif message.buttons and message.buttons > 0:
                        # self.print("EmbyPublicBot 可以签到")
                        numbers = re.findall(r"\d+", message.message)
                        number = int(numbers[0]) + int(numbers[1])
                        await onClickBtn(message.buttons, str(number))
                    # await client.send_read_acknowledge(event.chat_id, message)
            elif event.chat_id == self.pronEmbyGropChatId:
                # self.print(event)
                self.pronEmbyGropMessageCount += 1
                if QuestionAnswer.getGetQuestionAnswerMatch(message.message):
                    await emby_group_question_answer(event)
                # elif message.reply_markup and message.reply_markup.rows and message.reply_markup.rows[0]:
                #     buttons = message.reply_markup.rows[0].buttons
                #     for btn in buttons:
                #         if btn.text == "点击领取红包奖励":
                #             btn = buttons[0]
                #             await btn.click()
                #             self.print("抢红包点击成功")
                #             playMusic()
                elif "一大波红包来袭中" in message.message:
                    self.playMusic()
                elif "本轮问答活动已经结束" in message.message:
                    QuestionAnswer.writeQuestionAnswerJsonToFile()

                if message.button_count > 0:
                    await onClickBtn(message.buttons, '红包')

                # if self.pronEmbyGropMessageCount >= 100:
                #     self.sendMessageToEmbyGroupIs = True
                await sendMessageToEmbyGroup()
            # if count >= 2:
            #     sys.exit()
            elif message and message.chat and isinstance(message.chat,
                                                         Channel) and message.chat.title == pinYunEmbyTitle:
                self.pinYunEmbyMessageCount += 1  # self.pinYunEmbyMessageCount + 1 
                await sendPinYunEmbyGroup()
                if self.pinYunEmbyMessageCount > sendContentInt * 3 and not self.sendMessageToPingYunGroupIs:
                    self.sendMessageToPingYunGroupIs = True

        # 编辑信息
        async def edit_msg_event_handler(event: events.MessageEdited.Event):
            message = event.message
            await run_qweybgbot(event)

            if event.chat_id == self.pronEmbyGropChatId:
                # self.print(event)
                if re.match(r"问题\d+：", message.message):
                    await emby_group_question_answer(event)

        client.add_event_handler(callback=new_msg_event_handler,
                                 event=events.NewMessage(incoming=True)
                                 # event=events.NewMessage(from_users="EmbyPublicBot")
                                 )

        client.add_event_handler(callback=edit_msg_event_handler,
                                 event=events.MessageEdited(incoming=True)
                                 # event=events.NewMessage(from_users="EmbyPublicBot")
                                 )
        # await checkSing()
        self.print("启动{}成功".format(self.name))
        while 1:
            # with client:
            #     client.loop.run_until_complete(main())
            # await asyncio.sleep(24 * 60 * 60)
            # await checkSing()
            # self.print('sleep')
            await asyncio.sleep(random.randint(60 * 50, 60 * 90))
            self.sendMessageToEmbyGroupIs = True
            self.sendMessageToPingYunGroupIs = True
            await sendPinYunEmbyGroup()
            await sendMessageToEmbyGroup()

    def __init__(self, name):
        # func_suite
        self.print(datetime.datetime.now())
        self.playMusic()
        self.print(datetime.datetime.now())

        def run():
            asyncio.run(self.main())

        # thread = threading.Thread(target=run)
        # thread.start()
        run()

    def __new__(cls, name):
        obj = object.__new__(cls)
        obj.name = name
        return obj


def exitCallback():
    print("退出程序中。。。。。。保存json问题")
    QuestionAnswer.writeQuestionAnswerJsonToFile()


atexit.register(exitCallback)
# AutoTelegram("cyounim")
