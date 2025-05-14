"""General user-friendly interface to HDRezka"""
__all__ = ('Player', 'PlayerBase', 'PlayerMovie', 'PlayerSeries')

from collections import defaultdict
from typing import Any, SupportsInt, Optional

from bs4 import BeautifulSoup

from ._cache import CACHE
from .._bs4 import BUILDER
from ..api.ajax import AJAX
from ..errors import UnknownContentType
from ..post import Post, urls_from_ajax_response, URLs


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
        return self

    async def get_trailer_iframe(self) -> str:
        """Get trailer <iframe> HTML"""
        return (await AJAX.get_trailer_video(self.post.id)).get('code', '')

    def _translator(self, translator_id: Optional[SupportsInt] = None) -> int:
        if translator_id is None:
            return self.post.translator_id
        translator_id = int(translator_id)
        return self.post.translators.ids[abs(translator_id)] if translator_id <= 0 else translator_id

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.post.url!r})'


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
                                 builder=BUILDER)
        result: defaultdict[int, tuple[int, ...]] = defaultdict(tuple)
        for i in episodes.find_all(class_='b-simple_episode__item', attrs=('data-season_id', 'data-episode_id')):
            result[int(i.attrs.get('data-season_id'))] += int(i.attrs.get('data-episode_id', '0')),
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
    cached = CACHE.get(cast.post.url)
    if cached is not None:
        return cached
    await cast
    value: PlayerMovie | PlayerSeries
    match cast.post.type:
        case 'tv_series':
            value = PlayerSeries(cast)
        case 'movie':
            value = PlayerMovie(cast)
        case _ as e:
            raise UnknownContentType(e)
    CACHE.set(cast.post.url, value)
    return value


Player = player  # as if the name of the class
