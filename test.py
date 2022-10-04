#!/usr/bin/python3
from telethon import TelegramClient

api_id = 13197610
api_hash = 'a21f42d8391234581435652ea1162ca7'

async def main():
    client = TelegramClient('raynou', api_id, api_hash)
    await client.start()
    client.get_messages()
    print("终于扫描完了以前所有问题")


asyncio.run(main())

