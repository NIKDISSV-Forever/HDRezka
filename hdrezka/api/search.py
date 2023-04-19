from typing import Iterator

from ..errors import EmptyPage
from ..post.page import *

__all__ = ('Search',)

_SEARCH_TEMPLATE = 'https://rezka.ag/search/?do=search&subaction=search&q=%s'


class Search(Page):
    """AJAX class for HDRezka search"""
    __slots__ = ('_query',)

    def __init__(self, query: str = ''):
        self.query = query.strip()
        super().__init__(_SEARCH_TEMPLATE % self.query)

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, value):
        self._query = value if isinstance(value, str) else str(value)
        self.page = _SEARCH_TEMPLATE % self.query

    @staticmethod
    def _concat_paginator(url: str) -> str:
        return f'{url}&page={{0}}'

    def __iter__(self) -> Iterator[InlineItem]:
        """
        Returns the generator of all found articles
        """
        page = 1
        while True:
            try:
                yield from self.page_iter(page)
            except EmptyPage:
                return
            page += 1

    def __repr__(self):
        return f"{self.__class__.__qualname__}({f'{self.query!r}' if self.query else ''})"
