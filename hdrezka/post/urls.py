from __future__ import annotations

import re
from functools import lru_cache
from typing import Iterable, SupportsInt

from .._antiobfuscation import clear_trash

__all__ = ('short_url', 'long_url', 'URLs', 'Quality', 'URL')

_findall_qualities = re.compile(r'\[([^]]+)](\S+)(?:\sor\s|$)').findall
_match_quality_int = re.compile(r'(\d+)[pi]\s*($|\w+)').match
_shorten_url_match = re.compile(r'(?:(?:https?://)?rezka\.ag)?/?(\d+)\D*(?:\.html)?', re.I).match


@lru_cache(1024)
def short_url(url: str) -> str:
    """
    >>> short_url('https://rezka.ag/.../.../90909-any-name.html/')
    '90909-90909'
    >>> short_url('https://rezka.ag/.../.../any-name.html')
    '.../.../any-name'
    >>> short_url('https://rezka.ag/90909-any-name')
    '90909-90909'
    """
    parts = _shorten_url_match(url)
    if parts is None:
        return url
    id = parts.group(1)
    return f'{id}-{id}'


@lru_cache(1024)
def long_url(url: str) -> str:
    """
    >>> long_url('rezka.ag/.../.../99999-any-name')
    'https://rezka.ag/.../.../99999-99999.html'
    >>> long_url('.../.../99999-99999')
    'https://rezka.ag/.../.../99999-99999.html'
    """
    return f'https://rezka.ag/{short_url(url)}.html'


class Quality(str):
    __slots__ = ('_i', 'addon')
    addon: str  # can contain 'ultra'

    def __init__(self, *_, **__):
        _i = _match_quality_int(self)
        if not _i:
            raise ValueError(f'{self!r} is not quality.')
        _i, self.addon = _i.groups()
        self.addon = self.addon.casefold()
        self._i = int(_i)

    def __int__(self):
        """
        returns pixels height
        """
        return self._i

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return super().__le__(other)
        if not (self.addon or other.addon):
            return self._i < int(other)
        return False


class URL(str):
    __slots__ = ('mp4',)

    def __init__(self, *_, **__):
        self.mp4 = self.removesuffix('8').removesuffix(':hls:manifest.m3u')


class URLs:
    def __init__(self, data: str | dict):
        self._data: dict[Quality, URL] = (
            {Quality(q): URL(u) for q, u in _findall_qualities(clear_trash(data))}
            if isinstance(data, str) else data)
        self.qualities: tuple[Quality] = *sorted(self._data),
        self.min = int(self.qualities[0]) if self.qualities else 1

    @property
    def best_url(self) -> URL:
        return [*self[-1]._data.values()][0]

    def __getitem__(self, item: (SupportsInt | str) | (slice | Iterable)):
        isiter = False
        if not isinstance(item, str):
            if isinstance(item, slice):
                item = item.start, item.stop, item.step
            isiter = not not isinstance(item, Iterable) and item
        if isiter:
            result = self
            for part in item:
                if part is not None:
                    result = result[part]
            result = result._data
        elif isinstance(item, int):
            if item < self.min:
                item = self.qualities[item]
                result = {item: self._data[item]}
            else:
                result = {q: v for q, v in self._data.items() if int(q) == item}
        elif isinstance(item, str):
            item = item.casefold()
            result = {q: v for q, v in self._data.items() if q.addon == item}
        else:
            raise TypeError(f'Invalid type {type(item)}')
        return self.__class__(result)

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self._data})"
