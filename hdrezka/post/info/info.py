"""Title page parsing operations"""
__all__ = ('PostInfo',)

from inspect import getdoc

from bs4 import BeautifulSoup, Tag

from ._parser import FieldsParse
from ._utils import get_any_int
from .fields import *


class PostInfo:
    """Class with all available data"""
    __slots__ = ('rating', 'places', 'slogan', 'release', 'country', 'director', 'genre', 'quality',
                 'translator', 'age_rating', 'duration', 'from_', 'characters', '_view', 'fields',
                 'title', 'orig_title', 'poster', 'description', 'duration_s', 'updated_time')
    FILL_FIELDS: tuple[str, ...] = __slots__[:13]
    'indicate autofilled fields'

    def __init__(self, soup: BeautifulSoup):
        """Initialize class from title page BeautifulSoup"""
        self.title = title.text.strip() if (title := soup.find(class_='b-post__title')) else ''
        if duration_s := soup.find('meta', property='og:duration'):
            self.duration_s = int(duration_s.attrs.get('content', 0))
        else:
            self.duration = 0
        if upload_time := soup.find('meta', property='og:updated_time'):
            self.updated_time = int(upload_time.attrs.get('content', 0))
        else:
            self.updated_time = 0
        orig_title = soup.find(class_='b-post__origtitle')
        self.orig_title = orig_title.text.strip() if orig_title else self.title
        poster: Tag | dict[str, str] | None
        if poster := soup.select_one('.b-sidecover>a'):
            poster_href = poster.attrs.get('href', '')
            poster_src = poster.find('img').attrs.get('src', '')
        else:
            poster_href = poster_src = ''

        self.poster = Poster(poster_href, poster_src)
        self.description = desc.text.strip() if (desc := soup.find(class_='b-post__description_text')) else ''
        if post_info := soup.find(class_='b-post__info'):
            self._view = self._form_view(post_info.find_all('tr'))
            raw_fields = post_info.select('tr>td')
            if len(raw_fields) % 2:
                raw_fields.append(raw_fields[-1])
        else:
            raw_fields: list[Tag] = []

        fields = {h2.text.strip().removesuffix(':'): raw_fields[i + 1]
                  for i in range(0, len(raw_fields), 2) if (h2 := raw_fields[i].find('h2')) is not None}
        for field in self.FILL_FIELDS:
            meth = getattr(FieldsParse, f'get_field_{field}', None)
            field_name = '' if meth is None else (getdoc(meth) or '').strip()
            item = fields.get(field_name)
            if not item:
                setattr(self, field, None)
                continue
            if meth is None:
                processed = item
            else:
                processed = meth(item)
            fields[field_name] = processed
            setattr(self, field.removeprefix('_get_field_'), processed)

        rating_b = soup.find(class_='b-post__rating')
        post_rating = Rating(service='HDRezka',
                             rating=float(rating_b.select_one('[itemprop="average"]').text),
                             votes=get_any_int(rating_b.select_one('[itemprop="votes"]').text),
                             url=soup.find('meta', property='og:video').attrs.get('content', -1))
        if self.rating is None:
            self.rating = {}
        self.rating['hdrezka'] = post_rating
        self.fields = fields

    def _form_view(self, table: list[Tag]) -> str:
        return '{0}\n\n{1}\n\n{2}'.format(
            self.title if self.orig_title == self.title else f'{self.title} ({self.orig_title})',
            '\n'.join(tr.text.replace(')', ') ').strip() for tr in table),
            self.description
        )

    def __str__(self):
        """Returns user-friendly string"""
        return self._view

    def __repr__(self):
        return f"""{self.__class__.__qualname__}<{', '.join(
            f'{name}={attr!r}' for name in self.__slots__
            if not name.startswith('_') and (attr := getattr(self, name)))}>"""
