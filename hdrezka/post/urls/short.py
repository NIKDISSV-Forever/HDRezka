from functools import lru_cache

from ._regexes import shorten_url_match

__all__ = ('short_url', 'long_url')


@lru_cache(1024)
def short_url(url: str) -> str:
    """
    Returns string rezka.ag post with format "{id}-{id}" (valid path)
    """
    parts = shorten_url_match(url)
    if parts is None:
        return url
    id = parts.group(1)
    return f'{id}-{id}'


@lru_cache(1024)
def long_url(url: str) -> str:
    """
    Returns full url of rezka.ag post
    """
    return f'https://rezka.ag/{short_url(url)}.html'
