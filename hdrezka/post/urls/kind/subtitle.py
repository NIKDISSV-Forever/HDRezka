from .._regexes import findall_subtitles
from ..._dataclass import frozen_slots_dataclass

__all__ = ('SubtitleURL', 'SubtitleURLs')


@frozen_slots_dataclass
class SubtitleURL:
    url: str
    # language:
    name: str
    code: str


class SubtitleURLs:
    __slots__ = ('subtitles', 'has_subtitles', 'subtitle_names', 'subtitle_codes', 'default')

    def __init__(self, subtitle: str | bool, subtitle_lns: dict[str, str] | bool, subtitle_def: str | bool):
        self.has_subtitles = not subtitle
        if not subtitle_lns:
            subtitle_lns = {'off': ''}
        self.subtitles: tuple[SubtitleURL] = *(
            SubtitleURL(url, name, subtitle_lns[name]) for name, url in findall_subtitles(subtitle or '')),
        self.subtitles += SubtitleURL('', '', 'off'),
        self.subtitle_names = {}
        self.subtitle_codes = {}
        for subtitle in self.subtitles:
            self.subtitle_names[subtitle.name] = self.subtitle_codes[subtitle.code] = subtitle

        self.default: SubtitleURL | None = self.subtitle_codes.get(subtitle_def)

    def __getitem__(self, item: str) -> SubtitleURL | None:
        return self.subtitle_names.get(item, self.subtitle_codes.get(item))

    def __getattr__(self, item: str) -> SubtitleURL:
        return self.subtitle_codes[item]

    def __bool__(self):
        return self.has_subtitles

    def __repr__(self):
        return f'{self.__class__.__qualname__}<{self.subtitles!r}>'
