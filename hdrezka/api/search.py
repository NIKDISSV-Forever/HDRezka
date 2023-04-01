from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence, SupportsIndex, TypeVar

from bs4 import BeautifulSoup

from . import get_response
from ..errors import EmptySearchPage

__all__ = ('Search', 'SearchResult')

from ..stream.player import Player, PlayerType

PageNumber = TypeVar('PageNumber', Iterable[int], slice, int)
T = TypeVar('T')
_SEARCH_TEMPLATE = 'https://rezka.ag/search/?do=search&subaction=search&q=%s&page={0}'


def _range_from_slice(obj: slice | T) -> range | T:
    if isinstance(obj, slice):
        return range(*[i for i in (obj.start, obj.stop, obj.step) if i is not None])
    return obj


@dataclass(frozen=True)
class SearchResult:
    __slots__ = ('url', 'name', 'info', 'poster')  # python 3.8 dataclass has no slots argument
    url: str
    name: str
    info: str
    poster: str  # image url

    @property
    def player(self) -> PlayerType:
        return Player(self.url)


class Search:
    """Ajax class for HDRezka search"""
    __slots__ = ('_query', '_page_format')

    def __init__(self, query: str = ''):
        self.query = query.strip()

    @property
    def query(self) -> str:
        return self.query

    @query.setter
    def query(self, value):
        self._query = value if isinstance(value, str) else str(value)
        self._page_format = (_SEARCH_TEMPLATE % value).format

    def __iter__(self) -> Iterator[SearchResult]:
        """
        Returns the generator of all found articles
        """
        page = 1
        while True:
            try:
                yield from self.page_iter(page)
            except EmptySearchPage:
                return
            page += 1

    def page_iter(self, page: PageNumber = 1) -> Iterator[SearchResult] | None:
        page = _range_from_slice(page)
        is_not_iter = not isinstance(page, Iterable)
        if is_not_iter:
            page = page,
        for page in page:
            items = BeautifulSoup(get_response('GET', self._page_format(page)).text
                                  ).find_all(class_='b-content__inline_item')
            if not items:
                if is_not_iter:
                    raise EmptySearchPage(page)
                return
            yield from (SearchResult(
                (a := (link := i.find(class_='b-content__inline_item-link')).find('a'))['href'],
                a.text,
                link.find('div').text,
                i.find(class_='b-content__inline_item-cover').find('img').get('src', ''))
                for i in items)

    def page(self, page: PageNumber = 1) -> tuple[SearchResult]:
        return *self.page_iter(page),

    def __getitem__(self, item: PageNumber | Sequence[PageNumber, SupportsIndex | slice]
                    ) -> tuple[SearchResult] | SearchResult:
        if isinstance(item, Sequence) and len(item) == 2:
            page, index = item
            return self.page(page)[index]
        return self.page(item)

    def __repr__(self):
        return f"{self.__class__.__qualname__}({f'{self.query!r}' if self.query else ''})"
