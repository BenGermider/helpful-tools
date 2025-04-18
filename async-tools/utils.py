from asyncio import sleep


async def run_with_retries(func, *args, retries=3, delay=1, **kwargs):
    """
    Runs async func multiple times
    :param func: function to run
    :param args:
    :param retries: num of retries
    :param delay: seconds between runs
    :param kwargs:
    :return: result
    """
    for retry in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if retry < retries:
                await sleep(delay)
            else:
                raise e
