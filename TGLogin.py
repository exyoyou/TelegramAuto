import asyncio
import json
from dataclasses import dataclass

import requests
from telethon import TelegramClient

api_id = 13197610
api_hash = 'a21f42d8391234581435652ea1162ca7'
ipGetApiUrl = "http://ip-api.com/json/"
rule = json.loads(requests.get(ipGetApiUrl).content)
if rule["countryCode"] in "HK":
    api_id = 13595884
    api_hash = '03849446e0382cc148d2365d642a2d91'


@dataclass
class TgLogin:
    _session_name = ""
    _client = None
    _dialogs = None

    @classmethod
    async def create(cls, session_name=""):
        obj = cls()
        obj._session_name = session_name
        obj._client = TelegramClient(session_name, api_id=api_id, api_hash=api_hash)
        try:
            await obj._client.start()
        except BaseException as e:
            return await TgLogin.create(session_name + "_1")
        obj._dialogs = await obj._client.get_dialogs()
        return obj

    def get_client(self):
        return self._client

    async def update_dialos(self):
        self._dialogs = await self._client.get_dialogs()

    # 获取某个名字消息的最后一条消息
    def get_last_message_by_name(self, name, ):
        for dialog in self._dialogs:
            if name == dialog.name:
                return dialog.message
