#!/usr/bin/python3
import asyncio

count = 0


async def run():
    async def test():
        global count
        while True:
            count += 1
            if count >= 5:
                count = 0
                yield True
            await asyncio.sleep(5)
            yield True

    t = test()
    while True:
        if t:
            t.next()


asyncio.run(run())
