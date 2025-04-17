import functools
from asyncio import get_event_loop, Future


async def run_in_executor(fn, *args, **kwargs) -> Future:
    """
    Runs a synchronous function as asynchronous.
    :param fn: sync func
    :param args:
    :param kwargs:
    :return:
    """
    loop = get_event_loop()
    return loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))


# def asyncify(fn):
#     @functools.wraps(fn)
#     async def wrapper(*args, **kwargs):
#         loop = asyncio.get_running_loop()
#         return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))
#     return wrapper