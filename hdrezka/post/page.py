"""Any HDRezka page"""
__all__ = ('Page',)

from typing import Iterable

from bs4 import BeautifulSoup

from .inline import *
from .._bs4 import BUILDER
from ..api.http import get_response
from ..errors import EmptyPage
from ..url import Request


class Page:
    """AJAX class for HDRezka search"""
    __slots__ = ('_page', '_page_format', '__yields', '__yields_page')

    def __init__(self, url: str = Request.HOST):
        self.__yields: list[InlineItem] = []
        self.__yields_page = 0
        self.page = url

    @property
    def page(self) -> str:
        """Current page"""
        return self._page

    @page.setter
    def page(self, value):
        """Cast value to str and sets"""
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

    @staticmethod
    def _inline_info(years: str, country: str, genre: str):
        year, *finals = years.split('-')
        if finals:
            final, = finals
            year_final = ... if final.strip() == '...' else int(final)
        else:
            year_final = None
        return InlineInfo(int(year), year_final, country.strip(), genre.strip())

    async def get_page(self, page: int | slice | Iterable[int]) -> list[InlineItem]:
        """
        Get items from pages range.
        None for all elements of all pages
        """
        content = (await get_response('GET', self._page_format(page))).text
        items = BeautifulSoup(content, builder=BUILDER
                              ).find_all(class_='b-content__inline_item')
        if not items:
            raise EmptyPage(page)
        return [InlineItem(
            (a := (link := i.find(class_='b-content__inline_item-link')).find('a'))['href'],
            a.text,
            self._inline_info(*link.find('div').text.split(',', 3)),
            i.find(class_='b-content__inline_item-cover').find('img').get('src', ''))
            for i in items]

    def __aiter__(self):
        """Async iterator by pages"""
        self.__yields_page = 0
        self.__yields.clear()
        return self

    async def __anext__(self) -> InlineItem:
        """Returns `InlineItem` object for every title in page"""
        if not self.__yields:
            try:
                self.__yields_page += 1
                self.__yields += await self.get_page(self.__yields_page)
            except EmptyPage:
                raise StopAsyncIteration
        return self.__yields.pop(0)

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.page!r})'
