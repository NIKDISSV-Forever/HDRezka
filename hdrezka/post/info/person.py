"""Person information module"""
__all__ = ('Person',)

import re
from datetime import datetime

from .fields import Birthplace

_URL_ID_RE = re.compile(r'(?:(?:$|/)person/)?(\d+)-([^-]+)-([^/]+)')


class Person:
    """Person information. Need await object to fetch all else information will extract from url only."""
    __slots__ = ('image', 'name', 'name_transcription', 'id', 'career', 'birthday', 'birthplace', 'height', 'url')

    def __init__(self, url: str, *, name: str | None = None):
        """need await"""
        self.url = url
        self.height: float | None = None
        self.birthplace: Birthplace | None = None
        if m := _URL_ID_RE.search(url):
            id_, first, last = m.groups()
            self.id: int | None = int(id_)
            self.name_transcription = f'{first.capitalize()} {last.capitalize()}'
        else:
            self.name_transcription = ''
            self.id = None
        self.name = self.name_transcription if name is None else name

    def __await__(self):
        from .._utils import poster_and_soup
        if not (ps := (yield from poster_and_soup(self.url).__await__())):
            return self
        soup, self.image = ps
        if name := soup.select_one('[itemprop="name"]'):
            self.name = name.text
        if name := soup.select_one('[itemprop="alternativeHeadline"]'):
            self.name_transcription = name.text
        table = soup.select_one('.b-post__info')
        self.career = *(i.text for i in table.select('[itemprop="jobTitle"]')),
        date = table.select_one('[itemprop="birthDate"]').attrs.get('datetime')
        self.birthday = datetime.strptime(date, '%Y-%m-%d').date()
        sel = table.select('td.l+td:not(:has(*))')
        if not sel:
            return self
        birthplace, *height = sel
        self.height = float(height[0].text.strip().removesuffix('м')) if height else None
        match [i.strip() for i in birthplace.text.split(',')]:
            case [city, state, subcountry, country]:
                self.birthplace = Birthplace(country=country, city=city, subcountry=subcountry, state=state)
            case [city, state, country]:
                self.birthplace = Birthplace(country=country, city=city, state=state)
            case [city, country]:
                self.birthplace = Birthplace(country=country, city=city)
            case [country]:
                self.birthplace = Birthplace(country=country)
        return self

    def __repr__(self):
        return f"Person({f'{self.url!r}, ' if self.url else ''}{f'name={self.name!r}' if self.name else ''})"
