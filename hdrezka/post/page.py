from typing import Iterable, TypeVar

from ._dataclass import frozen_slots_dataclass
from .._bs4 import BeautifulSoup
from ..api.http import get_response
from ..errors import EmptyPage
from ..stream.player import *

__all__ = ('Page', 'PageNumber', 'InlineItem')

T = TypeVar('T')
PageNumber = TypeVar('PageNumber', int, slice, Iterable[int])


def _range_from_slice(obj: slice | T) -> range | T:
    if isinstance(obj, slice):
        return range(*[i for i in (obj.start, obj.stop, obj.step) if i is not None])
    return obj


@frozen_slots_dataclass
class InlineItem:
    """Content Inline Item view"""
    url: str
    name: str
    info: str
    poster: str
    'Image url'

    @property
    async def player(self) -> PlayerType:
        """Return a Player Instance"""
        return await Player(self.url)


class Page:
    """AJAX class for HDRezka search"""
    __slots__ = ('_page', '_page_format', '__yields', '__yields_page')

    def __init__(self, url: str = 'https://rezka.ag/'):
        self.__yields = []
        self.__yields_page = 0
        self.page = url

    @property
    def page(self) -> str:
        return self._page

    @page.setter
    def page(self, value):
        if not isinstance(value, str):
            value = str(value)
        # noinspection HttpUrlsUsage
        if not (value.startswith('https://') or value.startswith('http://')):
            value = f'https://{value}'
        self._page = value
        self._page_format = self._concat_paginator(value.removesuffix('/')).format

    @staticmethod
    def _concat_paginator(url: str) -> str:
        return f'{url}/page/{{0}}'

    def __aiter__(self):
        self.__yields_page = 0
        self.__yields.clear()
        return self

    async def __anext__(self) -> InlineItem:
        if not self.__yields:
            try:
                self.__yields_page += 1
                self.__yields += await self.get_page(self.__yields_page)
            except EmptyPage:
                raise StopAsyncIteration
        return self.__yields.pop(0)

    async def get_page(self, page: PageNumber) -> list[InlineItem]:
        """
        Get items from pages range.
        None for all elements of all pages
        """
        items = BeautifulSoup((await get_response('GET', self._page_format(page))).text
                              ).find_all(class_='b-content__inline_item')
        if not items:
            raise EmptyPage(page)
        return [InlineItem(
            (a := (link := i.find(class_='b-content__inline_item-link')).find('a'))['href'],
            a.text,
            link.find('div').text,
            i.find(class_='b-content__inline_item-cover').find('img').get('src', ''))
            for i in items]

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.page!r})'
