"""Person information module"""
import re
from datetime import datetime

from bs4 import BeautifulSoup

from ._utils import page_poster
from .fields import Birthplace
from ..._bs4 import BUILDER
from ...api.http import get_response

_URL_ID_RE = re.compile(r'(?:(?:$|/)person/)?(\d+)-([^-]+)-([^/]+)')


class Person:
    """Person information. Need await object to fetch all else information will extract from url only."""
    __slots__ = ('image', 'name', 'name_transcription', 'id', 'career', 'birthday', 'birthplace', 'height', 'url')

    def __init__(self, url: str, *, name: str = None):
        """need await"""
        self.url = url
        if m := _URL_ID_RE.search(url):
            id_, first, last = m.groups()
            self.id = int(id_)
            self.name_transcription = f'{first.capitalize()} {last.capitalize()}'
            self.name = name if name is not None else self.name_transcription
        else:
            self.name = self.name_transcription = '' if name is None else name
            self.id = None

    def __await__(self):
        if not self.url:
            return
        response = yield from get_response('GET', self.url).__await__()
        soup = BeautifulSoup(response.content, builder=BUILDER)
        self.image = page_poster(soup)
        if name := soup.select_one('[itemprop="name"]'):
            self.name = name.text
        if name := soup.select_one('[itemprop="alternativeHeadline"]'):
            self.name_transcription = name.text
        table = soup.select_one('.b-post__info')
        self.career = *(i.text for i in table.select('[itemprop="jobTitle"]')),
        date = table.select_one('[itemprop="birthDate"]').attrs.get('datetime')
        self.birthday = datetime.strptime(date, '%Y-%m-%d').date()
        sel = table.select('td.l + td:not(:has(*))')
        if not sel:
            return
        birthplace, *height = sel
        self.height = float(height[0].text.strip().removesuffix('м')) if height else None
        match [i.strip() for i in birthplace.text.split(',')]:
            case [city, state, subcountry, country]:
                self.birthplace = Birthplace(country=country, city=city, subcountry=subcountry, state=state)
            case [city, state, country]:
                self.birthplace = Birthplace(country=country, city=city, state=state)
            case [city, country]:
                self.birthplace: Birthplace = Birthplace(country=country, city=city)
            case [country]:
                self.birthplace = Birthplace(country=country)

    def __repr__(self):
        return f"Person({repr(self.url) if self.url else ''}, name={repr(self.name) if self.name else ''})"
