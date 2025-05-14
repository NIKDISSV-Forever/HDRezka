"""Franchises information parsing module"""
__all__ = ('FranchiseInfo', 'FranchiseEntry')

from typing import NamedTuple

from bs4 import Tag, BeautifulSoup

from .fields import Hyperlink
from .._utils import hyperlink, get_any_int, poster_and_soup


class FranchiseEntry(NamedTuple):
    """ Franchise entry information """
    title: Hyperlink
    year: int
    rating: float | None = None


class FranchiseInfo:
    """ Franchise information class """
    __slots__ = ('url', '_entries', '_keys', '_current', '_poster')

    def __init__(self, url: str | None = None, soup: BeautifulSoup | Tag | None = None):
        """await needed"""
        self._entries: dict[int, FranchiseEntry] = {}
        self._keys: tuple[int, ...] = ()
        self._poster: str | None = None
        self._current: int | None = None
        self.url = url
        if soup is not None:
            self._setup_from_soup(soup)

    def __await__(self):
        if not (ps := (yield from poster_and_soup(self.url).__await__())):
            return self
        soup, self._poster = ps
        if not self.entries:
            self._setup_from_soup(soup)
        return self

    @property
    def entries(self) -> dict[int, FranchiseEntry]:
        """franchise entries (without current)"""
        return self._entries

    @entries.setter
    def entries(self, entries: dict[int, FranchiseEntry]):
        self._entries = entries
        self._keys = *entries.keys(),

    @property
    def poster(self):
        """wide poster, need await self first"""
        return self._poster

    @property
    def current(self):
        """Current position"""
        return self._current

    @property
    def previous(self):
        """Previous position"""
        return None if self._current == 1 else self.entries[self._current - 1]

    @property
    def next(self):
        """Next position"""
        return None if self._current == len(self.entries) - 1 else self.entries[self._current + 1]

    def _setup_from_soup(self, soup: BeautifulSoup | Tag):
        content = soup.select('.b-post__partcontent_item')[::-1]
        entries = {}
        for entry in content:
            n = int(entry.find(class_='num').text.strip())
            if 'current' in entry.attrs.get('class', ()):
                self._current = n
                continue
            entries[n] = FranchiseEntry(title=hyperlink(entry.select_one('.title>a')),
                                        year=get_any_int(entry.find(class_='year')),
                                        rating=None if (r := entry.find(class_='rating').text) == '—' else float(r))
        self.entries = entries

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, item: int | slice) -> FranchiseEntry | tuple[FranchiseEntry] | tuple:
        if isinstance(item, int):
            return self.entries[self._keys[item]]
        if isinstance(item, slice):
            return *(self.entries[k] for k in self._keys[item]),
        raise TypeError(f'Expected int or slice; got {type(item).__name__} ({item!r})')

    def __str__(self):
        return f"{self.__class__.__qualname__}({repr(self.url) if self.url else ''})"
