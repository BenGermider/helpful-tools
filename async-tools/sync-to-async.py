import functools
from typing import Callable, Coroutine, Any
from asyncio import Future, get_running_loop


async def run_in_executor(fn: callable, *args, **kwargs) -> Future:
    """
    Runs a synchronous function as asynchronous.
    :param fn: sync func
    :param args:
    :param kwargs:
    :return:
    """
    loop = get_running_loop()
    return loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))


def asyncify(fn: callable) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    Returns a synchronous function as a coroutine.
    :param fn: sync function
    :return: coroutine of sync function
    """
    @functools.wraps(fn)  # Delivers fn attributes to new async fn.
    async def wrapper(*args, **kwargs):
        loop = get_running_loop()
        return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))
    return wrapper
