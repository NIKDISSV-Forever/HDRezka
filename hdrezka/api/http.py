import httpx

__all__ = ('get_response', 'DEFAULT_CLIENT_KWARGS', 'DEFAULT_REQUEST_KWARGS')

DEFAULT_CLIENT_KWARGS = {'headers': {'user-agent': 'Mozilla/5.0'}, 'follow_redirects': True}
DEFAULT_REQUEST_KWARGS = {}


async def get_response(*args, **kwargs):
    async with httpx.AsyncClient(**DEFAULT_CLIENT_KWARGS) as client:
        return await client.request(*args, **kwargs, **DEFAULT_REQUEST_KWARGS)
