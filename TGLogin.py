import json

import requests
from telethon import TelegramClient

api_id = 13197610
api_hash = 'a21f42d8391234581435652ea1162ca7'
ipGetApiUrl = "http://ip-api.com/json/"
rule = json.loads(requests.get(ipGetApiUrl).content)
if rule["countryCode"] in "HK":
    api_id = 13595884
    api_hash = '03849446e0382cc148d2365d642a2d91'


def GetClient(sessionName):
    return TelegramClient(sessionName, api_id, api_hash)


    