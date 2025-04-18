import asyncio

class Scheduler:

    def __init__(self, timeout: int):
        self._timeout = timeout
        self._running = True

    async def task(self):
        raise NotImplemented

    async def stop(self):
        self._running = False

    async def schedule(self):
        while self._running:
            await self.task()
            await asyncio.sleep(self._timeout)

