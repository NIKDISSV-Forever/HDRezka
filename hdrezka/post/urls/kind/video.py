from typing import Iterable, SupportsInt

from .quality import Quality
from .._regexes import findall_qualities
from ...._antiobfuscation import clear_trash

__all__ = ('VideoURL', 'VideoURLs')


class VideoURL(str):
    __slots__ = ('mp4',)

    def __init__(self, *_, **__):
        self.mp4 = self.removesuffix('8').removesuffix(':hls:manifest.m3u')


class VideoURLs:
    __slots__ = ('raw_data', 'qualities', 'min')

    def __init__(self, data: str | dict):
        self.raw_data: dict[Quality, VideoURL] = (
            {Quality(q): VideoURL(u) for q, u in findall_qualities(clear_trash(data))}
            if isinstance(data, str) else data)
        self.qualities: tuple[Quality] = *sorted(self.raw_data),
        self.min = int(self.qualities[0]) if self.qualities else 1

    @property
    def last_url(self) -> VideoURL:
        return self[-1].raw_data.popitem()[1]

    def __getitem__(self, item: str | SupportsInt | Iterable | slice):
        isiter = False
        if not isinstance(item, str):
            if isinstance(item, slice):
                item = item.start, item.stop, item.step
            isiter = isinstance(item, Iterable) and item
        if isiter:
            result = self
            for part in item:
                if part is not None:
                    result = result[part]
            result = result.raw_data
        elif isinstance(item, int):
            if item < self.min:
                item = self.qualities[item]
                result = {item: self.raw_data[item]}
            else:
                result = {q: v for q, v in self.raw_data.items() if int(q) == item}
        elif isinstance(item, str):
            item = item.casefold()
            result = {q: v for q, v in self.raw_data.items() if q.addon == item}
        else:
            raise TypeError(f'Invalid type {type(item)}')
        return self.__class__(result)

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.raw_data})"
