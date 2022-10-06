#!/usr/bin/python3
import asyncio
import re

from telethon import TelegramClient

import QuestionAnswer

api_id = 13197610
api_hash = 'a21f42d8391234581435652ea1162ca7'
str = """
我问题19:《桔梗谣》是哪里的民歌？

A:菲律宾
B:阿富汗
C:日本
D:朝鲜

答案为：D

桔梗谣是朝鲜族民歌。 “道拉基”是朝鲜族人民喜爱吃的一种野菜，叫“桔梗”，所以这首民歌叫《桔梗谣》，又名《道拉基》。
"""


async def main():
    # client = TelegramClient('raynou', api_id, api_hash)
    # await client.start()
    # client.get_messages()
    # print("终于扫描完了以前所有问题")
    str1 = str.strip()
    # compile = re.compile(r"问题\d+(:|：)")
    # match = compile.match(str1)
    # print(match)
    compile = re.compile(r"答案为(:|：)")
    search_re = compile.search(str)
    answer_index_str = str1[search_re.regs[1][0]:search_re.regs[1][1]]
    answer_index = str1.find(answer_index_str)
    answer = str1[answer_index + 2:str1.find("\n", answer_index + 2)]
    print(search_re)


asyncio.run(main())
