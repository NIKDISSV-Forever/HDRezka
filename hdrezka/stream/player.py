"""General user-friendly interface to HDRezka"""
from collections import defaultdict
from typing import Any, SupportsInt, Optional

from bs4 import BeautifulSoup

from ..api.ajax import AJAX
from ..errors import UnknownContentType
from ..post import *

__all__ = ('Player', 'PlayerBase', 'PlayerMovie', 'PlayerSeries')


class _CacheStorage:
    __slots__ = ('max_size', '__storage')

    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.__storage: dict[str, PlayerMovie | PlayerSeries] = {}

    def get(self, key):
        return self.__storage.get(key)

    def set(self, key, value):
        self.__storage[key] = value
        for k in (*self.__storage.keys(),):
            if len(self.__storage) <= self.max_size:
                break
            del self.__storage[k]


__CACHE = _CacheStorage()


class PlayerBase:
    """Base type of Player"""
    __slots__ = ('post',)

    def __init__(self, url_or_cast: Any):
        """Need await"""
        if isinstance(url_or_cast, PlayerBase):
            self.post: Post = url_or_cast.post
            return
        elif not isinstance(url_or_cast, str):
            url_or_cast = str(url_or_cast)
        self.post = Post(url_or_cast)

    def __await__(self):
        """
        Initialize `self.post`
        Do not call twice!
        """
        yield from self.post.__await__()

    def _translator(self, translator_id: Optional[SupportsInt] = None) -> int:
        if translator_id is None:
            return self.post.translator_id
        translator_id = int(translator_id)
        return self.post.translators.ids[abs(translator_id)] if translator_id <= 0 else translator_id

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.post.url!r})"


class PlayerMovie(PlayerBase):
    """Movies Player Type"""
    __slots__ = ()

    async def get_stream(self, translator_id: Optional[SupportsInt] = None) -> URLs:
        """Returns movie stream `URLs`"""
        return urls_from_ajax_response(await AJAX.get_movie(self.post.id, self._translator(translator_id)))


class PlayerSeries(PlayerBase):
    __slots__ = ()

    async def get_episodes(self, translator_id: Optional[SupportsInt] = None) -> defaultdict[int, tuple[int, ...]]:
        """Returns available episodes"""
        episodes = BeautifulSoup((await AJAX.get_episodes(self.post.id, self._translator(translator_id)))['episodes'],
                                 features=['html', 'fast'])
        result: defaultdict[int, tuple[int, ...]] = defaultdict(tuple)
        for i in episodes.find_all(class_='b-simple_episode__item', attrs=('data-season_id', 'data-episode_id')):
            result[int(i.get('data-season_id'))] += int(i.get('data-episode_id')),
        return result

    async def get_stream(self, season: int, episode: int, translator_id: Optional[SupportsInt] = None) -> URLs:
        """Returns episode stream `URLs`"""
        return urls_from_ajax_response(
            await AJAX.get_stream(self.post.id, self._translator(translator_id), season, episode))


async def player(url_or_path: Any) -> PlayerMovie | PlayerSeries:
    """
    Returns either Player Series if series, or PlayerMovie if movie, otherwise raises UnknownContentType
    """
    cast = PlayerBase(url_or_path)
    cached = __CACHE.get(cast.post.url)
    if cached is not None:
        return cached
    await cast
    type = cast.post.type
    value: PlayerMovie | PlayerSeries
    match type:
        case 'tv_series':
            value = PlayerSeries(cast)
        case 'movie':
            value = PlayerMovie(cast)
        case _:
            raise UnknownContentType(type)
    __CACHE.set(cast.post.url, value)
    return value


Player = player  # as if the name of the class
