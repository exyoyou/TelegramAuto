#!/usr/bin/python3
import asyncio
import os

import TGLogin
from Captcha import TwoCaptcha


async def run():
    tg = await TGLogin.TgLogin.create("kaikai")
    client = tg.get_client()
    message = tg.get_last_message_by_name("卷毛鼠活动机器人")
    print(message)
    if message.media:
        file_name = await client.download_media(message, file=bytes)
        # while not os.path.exists(file_name):
        #     await asyncio.sleep(1)
        # await asyncio.sleep(1)
        # print(file)
        code = TwoCaptcha().get_normal_captcha_code(file_name)
        print(code)


# if message.photo:


asyncio.run(run())
