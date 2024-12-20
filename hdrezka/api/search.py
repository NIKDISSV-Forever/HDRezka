"""Implementation of search on HDRezka pages (see ..post.page.Page class)"""
from typing import override

from ..post.page import *
from ..url import Request

__all__ = ('Search',)


class Search(Page):
    """AJAX class for HDRezka search"""
    __slots__ = ('_query',)

    def __init__(self, query: str = ''):
        """Preparing query for search"""
        self.query = query.strip()
        super().__init__(self.search_url(self.query))

    @staticmethod
    def search_url(query: str):
        return Request.host_join(f'search/?do=search&subaction=search&q={query}')

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, value):
        """Cast value to str and sets"""
        self._query = value if isinstance(value, str) else str(value)
        self.page = self.search_url(self.query)

    @staticmethod
    @override
    def _concat_paginator(url: str) -> str:
        return f'{url}&page={{0}}'

    def __repr__(self):
        return f"{self.__class__.__qualname__}({f'{self.query!r}' if self.query else ''})"
