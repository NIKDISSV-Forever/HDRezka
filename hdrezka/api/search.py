"""Implementation of search on HDRezka pages (see ..post.page.Page class)"""
__all__ = ('Search',)

from typing import override

from ..post.page import *
from ..url import Request


class Search(Page):
    """AJAX class for HDRezka search"""
    __slots__ = ('_query',)

    def __init__(self, query: str = ''):
        """Preparing query for search"""
        self.query = query.strip()
        super().__init__(self.search_url(self.query))

    @staticmethod
    def search_url(query: str):
        """Returns current query search url"""
        return Request.host_join(f'search/?do=search&subaction=search&q={query}')

    @property
    def query(self) -> str:
        """Current search query"""
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
        return f"{self.__class__.__qualname__}({repr(self.query) if self.query else ''})"
