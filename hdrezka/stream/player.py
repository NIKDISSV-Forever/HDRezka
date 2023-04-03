from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import Any, SupportsInt, TypeVar

from .._bs4 import BeautifulSoup
from ..api.ajax import Ajax
from ..errors import UnknownContentType
from ..post import *

__all__ = ('Player', 'PlayerType')


class PlayerBase:
    __slots__ = ('post',)

    def __init__(self, url_or_cast: Any):
        if isinstance(url_or_cast, PlayerBase):
            self.post = url_or_cast.post
            return
        elif not isinstance(url_or_cast, str):
            url_or_cast = str(url_or_cast)
        self.post = Post(url_or_cast)

    def _translator(self, translator_id: SupportsInt = None):
        if translator_id is None:
            return self.post.translator_id
        translator_id = int(translator_id)
        return self.post.translators.ids[abs(translator_id)] if translator_id <= 0 else translator_id

    def __repr__(self):
        return f"{self.__class__.__qualname__}({short_url(self.post.url)!r})"


class PlayerMovie(PlayerBase):
    __slots__ = ()

    def get_stream(self, translator_id: SupportsInt = None) -> URLs:
        return URLs(Ajax.get_movie(self.post.id, self._translator(translator_id))['url'])


class PlayerSeries(PlayerBase):
    __slots__ = ()

    def get_episodes(self, translator_id: SupportsInt = None) -> defaultdict[int, tuple[int]]:
        episodes = BeautifulSoup(Ajax.get_episodes(self.post.id, self._translator(translator_id))['episodes'])
        result: defaultdict[int, tuple[int]] = defaultdict(tuple)
        for i in episodes.find_all(class_='b-simple_episode__item', attrs=('data-season_id', 'data-episode_id')):
            result[int(i.get('data-season_id'))] += int(i.get('data-episode_id')),
        return result

    def get_stream(self, season: int, episode: int, translator_id: SupportsInt = None) -> URLs:
        return URLs(Ajax.get_stream(
            self.post.id,
            self._translator(translator_id),
            season, episode)['url'])


PlayerType = TypeVar('PlayerType', PlayerBase, PlayerMovie, PlayerSeries)


@lru_cache(512)
def player(url_or_path: Any) -> PlayerType:
    """
    Returns either Player Series if series, or PlayerMovie if movie, otherwise raises UnknownContentType
    """
    p = PlayerBase(url_or_path)
    type = p.post.type
    if type == 'tv_series':
        return PlayerSeries(p)
    if type == 'movie':
        return PlayerMovie(p)
    raise UnknownContentType(type)


Player = player
