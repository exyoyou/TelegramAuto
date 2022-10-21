#!/usr/bin/python3
import asyncio

import requests

import TGLogin


class AotoBot:
    def getContent(self, content):
        if (not isinstance(content, str)):
            return
        if len(content) < 0:
            return
        req = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + content, )
        json = req.json()
        # print(json)
        return json["content"]


# async def test():
#     tg_login = await TGLogin.TgLogin.create("kaikai_1")
#     message = tg_login.get_last_message_by_name("品云Emby")
#     content = AotoBot().getContent(message.message)
#     print(content)
# 
# 
# asyncio.run(test())
