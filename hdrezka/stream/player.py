from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import Any, SupportsInt, TypeVar
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .urls import URLs
from ..api.ajax import Ajax
from ..errors import UnknownContentType
from ..page import Page

__all__ = ('Player', 'PlayerType')


@lru_cache
def _short_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.hostname.casefold() == 'rezka.ag':
        return url
    return parsed.path.strip('/').removesuffix('.html')


class PlayerBase:
    __slots__ = ('page',)

    def __init__(self, url_or_cast: Any):
        if isinstance(url_or_cast, PlayerBase):
            self.page = url_or_cast.page
            return
        elif not isinstance(url_or_cast, str):
            url_or_cast = str(url_or_cast)
        l_url_or_path = url_or_cast.casefold().strip('/')
        if not l_url_or_path.startswith('https://rezka.ag/'):
            url_or_cast = urljoin('https://rezka.ag/', url_or_cast)
        if not l_url_or_path.endswith('.html'):
            url_or_cast = f'{url_or_cast}.html'
        self.page = Page(url_or_cast)

    def _translator(self, translator_id: SupportsInt = None):
        if translator_id is None:
            return self.page.translator_id
        translator_id = int(translator_id)
        return self.page.translators.ids[abs(translator_id)] if translator_id <= 0 else translator_id

    def __repr__(self):
        return f"{self.__class__.__qualname__}({_short_url(self.page.url)!r})"


class PlayerSeries(PlayerBase):
    __slots__ = ()

    def get_episodes(self, translator_id: SupportsInt = None) -> dict[int, tuple[int]]:
        episodes = BeautifulSoup(Ajax.get_episodes(self.page.id, self._translator(translator_id))['episodes'])
        result = defaultdict(tuple)
        for i in episodes.find_all(class_='b-simple_episode__item', attrs=('data-season_id', 'data-episode_id')):
            result[int(i.get('data-season_id'))] += int(i.get('data-episode_id')),
        return result

    def get_stream(self, season: int, episode: int, translator_id: SupportsInt = None) -> URLs:
        return URLs(Ajax.get_stream(
            self.page.id,
            self._translator(translator_id),
            season, episode)['url'])


class PlayerMovie(PlayerBase):
    __slots__ = ()

    def get_stream(self, translator_id: SupportsInt = None) -> URLs:
        return URLs(Ajax.get_movie(self.page.id, self._translator(translator_id))['url'])


PlayerType = TypeVar('PlayerType', PlayerBase, PlayerMovie, PlayerSeries)


@lru_cache
def player(url_or_path: str) -> PlayerType:
    p = PlayerBase(url_or_path)
    type = p.page.type
    if type == 'tv_series':
        return PlayerSeries(p)
    if type == 'movie':
        return PlayerMovie(p)
    raise UnknownContentType(type)


Player = player
