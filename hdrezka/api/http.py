"""Basic wrapper for all http requests of the package"""
__all__ = ('get_response', 'login_global', 'DEFAULT_CLIENT', 'DEFAULT_REQUEST_KWARGS')

from typing import Any, Optional, TypedDict

import httpx

from ..url import Request


class RequestKwargs(TypedDict):
    """**kwargs for httpx.request"""
    content: Optional[Any]
    data: Optional[Any]
    files: Optional[Any]
    json: Optional[Any]
    params: Optional[Any]
    headers: Optional[Any]
    cookies: Optional[Any]
    auth: Optional[Any]
    follow_redirects: Optional[bool | Any]
    timeout: Optional[Any]
    extensions: Optional[Any]


DEFAULT_CLIENT = httpx.AsyncClient(headers={'User-Agent': 'Mozilla/5.0'})
DEFAULT_REQUEST_KWARGS: RequestKwargs | dict = {}


async def get_response(method: str, url: str | httpx.URL, **kwargs) -> httpx.Response:
    """
    passed **kwargs have more weight than DEFAULT_REQUEST_KWARGS.
    Returns DEFAULT_CLIENT.request(method, url, **kwargs, **DEFAULT_REQUEST_KWARGS)
    """
    for k, v in DEFAULT_REQUEST_KWARGS.items():
        if k not in kwargs:
            kwargs[k] = v
    return await DEFAULT_CLIENT.request(method, url, **kwargs)


async def login_global(email: str, password: str):
    """
    It enters the site using `DEFAULT_CLIENT`.
    Updates the global `HOST` to bypass the blocking, and `DEFAULT_CLIENT` cookies.
    """
    _follow_redirects = DEFAULT_CLIENT.follow_redirects
    DEFAULT_CLIENT.follow_redirects = False
    resp = await get_response('GET', Request.REDIRECT_URL)
    DEFAULT_CLIENT.follow_redirects = _follow_redirects
    url = httpx.URL(resp.headers.get('Location', resp.url))
    ajax_login_url = url.join('/ajax/login/')

    await get_response(
        'POST', ajax_login_url,
        data={'login_name': email, 'login_password': password, 'login_not_save': '0', 'login': 'submit'})
    Request.HOST = f'https://{url.host}'
