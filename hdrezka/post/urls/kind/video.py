"""high-level representation of video"""
from typing import Iterable, SupportsInt

from .quality import Quality
from .._regexes import findall_qualities
from ...._deobfuscation import clear_trash
from ....api.http import get_response

__all__ = ('VideoURL', 'VideoURLs')


class VideoURL(str):
    """str type add-on to represent video"""
    __slots__ = ()

    def __await__(self):
        """Follow redirects in url and return correct video url"""
        return self.__class__((yield from get_response("GET", self, follow_redirects=True).__await__()).url)

    @property
    def mp4(self) -> str:
        """url without ':hls:manifest.m3u8'"""
        return str(self.removesuffix('8').removesuffix(':hls:manifest.m3u'))


class VideoURLs:
    """Class representing video urls"""
    __slots__ = ('raw_data', 'qualities', 'min')

    def __init__(self, data: str | dict):
        """
        :param data:
            type str if raw url from AJAX request
            else type dict[Quality, VideoURLs]
            if not str and not dict raises TypeError
        """
        if isinstance(data, str):
            self.raw_data: dict[Quality, VideoURL] = {
                Quality(q): VideoURL(u) for q, u in findall_qualities(clear_trash(data))}
        elif isinstance(data, dict):
            self.raw_data = data
        else:
            raise TypeError(f'got {data!r} (type {type(data)}) but expected type {str | dict}')
        self.qualities: tuple[Quality, ...] = *sorted(self.raw_data),
        self.min = int(self.qualities[0]) if self.qualities else 1

    @property
    def last_url(self):
        """Best quality url"""
        return self[-1].raw_data.popitem()[1]

    def __getitem__(self, item: str | SupportsInt | Iterable | slice):
        """
        >>> self[1080]['ultra']
        {'1080p Ultra': '...'}
        >>> self[360:1080, 2160]
        {'360p': '...', '480p': '...', '720p': '...', '2160p': '...'}
        >>> self[720, 1080]
        {'720p': '...', '1080p': '...', '1080p Ultra': '...'}
        """
        if isinstance(item, str):
            item = item.casefold()
            result = {q: v for q, v in self.raw_data.items() if q.addon == item}
        elif isinstance(item, slice):
            supported = {*range(*item.indices(int(self.qualities[-1]) + 1))}
            result = {q: v for q, v in self.raw_data.items() if int(q) in supported}
        elif isinstance(item, Iterable) and item:
            result = {}
            for part in item:
                if part is not None:
                    result |= self[part].raw_data
        elif isinstance(item, int):
            if item < self.min:
                item = self.qualities[item]
                result = {item: self.raw_data[item]}
            else:
                result = {q: v for q, v in self.raw_data.items() if int(q) == item}
        else:
            raise TypeError(f'Invalid type {type(item)}')
        return self.__class__(result)

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.raw_data})"
