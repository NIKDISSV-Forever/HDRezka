from httpx import request as _request

__all__ = ('get_response', 'DEFAULT_REQUEST_KWARGS')

DEFAULT_REQUEST_KWARGS = {'headers': {'user-agent': 'Mozilla/5.0'}}


def get_response(*args, **kwargs):
    for k, v in DEFAULT_REQUEST_KWARGS.items():
        kwargs.setdefault(k, v)
    return _request(*args, **kwargs)
