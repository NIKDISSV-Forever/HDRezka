from dataclasses import dataclass

from .._regexes import findall_subtitles

__all__ = ('SubtitleURL', 'SubtitleURLs')


@dataclass(frozen=True, slots=True)
class SubtitleURL:
    """
    url: str
        .vtt file url

    Language attributes:
    name: str
    code: str
    """
    url: str
    # language:
    name: str
    code: str


class SubtitleURLs:
    """Class representing subtitle urls"""
    __slots__ = ('subtitles', 'has_subtitles', 'subtitle_names', 'subtitle_codes', 'default')

    def __init__(self, subtitle: str, subtitle_lns: dict[str, str], subtitle_def: str):
        """
        :param subtitle: is subtitles exists
        :param subtitle_lns: languages {code: name, ...}
        :param subtitle_def: default subtitle code
        """
        self.has_subtitles = not subtitle
        self.subtitles: tuple[SubtitleURL, ...] = *(
            SubtitleURL(url, name, subtitle_lns[name]) for name, url in findall_subtitles(subtitle or '')),
        self.subtitles += SubtitleURL('', '', 'off'),
        self.subtitle_names = {}
        self.subtitle_codes = {}
        for subtitle_item in self.subtitles:
            self.subtitle_names[subtitle_item.name] = self.subtitle_codes[subtitle_item.code] = subtitle_item

        self.default: SubtitleURL | None = self.subtitle_codes.get(subtitle_def)

    def __getitem__(self, item: str) -> SubtitleURL | None:
        """Returns subtitle url by name"""
        return self.subtitle_names.get(item, self.subtitle_codes.get(item))

    def __getattr__(self, item: str) -> SubtitleURL:
        """Returns subtitle url by code"""
        return self.subtitle_codes[item]

    def __bool__(self):
        """Is subtitles exists"""
        return self.has_subtitles

    def __repr__(self):
        return f'{self.__class__.__qualname__}<{self.subtitles!r}>'
