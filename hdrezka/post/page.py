from typing import Iterable, Iterator, Sequence, SupportsIndex, TypeVar

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
    def player(self) -> PlayerType:
        """Return a Player Instance"""
        return Player(self.url)


class Page:
    """AJAX class for HDRezka search"""
    __slots__ = ('_page', '_page_format')

    def __init__(self, url: str = 'https://rezka.ag/'):
        self.page = url

    def __iter__(self) -> Iterator[InlineItem]:
        """
        Returns the generator of all found articles
        """
        page = 1
        while True:
            try:
                yield from self.page_iter(page)
            except EmptyPage(page):
                return
            page += 1

    @property
    def page(self) -> str:
        return self._page

    @page.setter
    def page(self, value):
        if not isinstance(value, str):
            value = str(value)
        if not value.startswith('https://'):
            value = f'https://{value}'
        self._page = value
        self._page_format = self._concat_paginator(value.removesuffix('/')).format

    @staticmethod
    def _concat_paginator(url: str):
        return f'{url}/page/{{0}}'

    def page_iter(self, page: PageNumber = 1) -> Iterator[InlineItem] | None:
        page = _range_from_slice(page)
        is_not_iter = not isinstance(page, Iterable)
        if is_not_iter:
            page = page,
        for page in page:
            items = BeautifulSoup(get_response('GET', self._page_format(page)).text
                                  ).find_all(class_='b-content__inline_item')
            if not items:
                if is_not_iter:
                    raise EmptyPage(page)
                return
            yield from (InlineItem(
                (a := (link := i.find(class_='b-content__inline_item-link')).find('a'))['href'],
                a.text,
                link.find('div').text,
                i.find(class_='b-content__inline_item-cover').find('img').get('src', ''))
                for i in items)

    def get_pages(self, page: PageNumber = 1) -> tuple[InlineItem]:
        return *self.page_iter(page),

    def __getitem__(self, item: PageNumber | Sequence[PageNumber | SupportsIndex | slice]
                    ) -> tuple[InlineItem] | InlineItem:
        if isinstance(item, Sequence) and len(item) == 2:
            page, index = item
            return self.get_pages(page)[index]
        return self.get_pages(item)

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.page!r})'
