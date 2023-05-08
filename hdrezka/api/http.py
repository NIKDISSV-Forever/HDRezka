import httpx

__all__ = ('get_response', 'DEFAULT_REQUEST_KWARGS')

DEFAULT_REQUEST_KWARGS = {'headers': {'user-agent': 'Mozilla/5.0'}}


async def get_response(*args, **kwargs):
    for k, v in DEFAULT_REQUEST_KWARGS.items():
        kwargs.setdefault(k, v)
    async with httpx.AsyncClient() as client:
        return await client.request(*args, **kwargs)
