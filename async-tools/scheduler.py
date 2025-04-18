import asyncio

class Scheduler:

    def __init__(self, timeout: int):
        self._timeout = timeout

    async def task(self):
        raise NotImplemented

    async def schedule(self):
        while True:
            await self.task()
            await asyncio.sleep(self._timeout)
