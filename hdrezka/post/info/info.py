"""Title page parsing operations"""
__all__ = ('PostInfo',)

from inspect import getdoc

from bs4 import BeautifulSoup, Tag

from . import _parser
from ._utils import get_any_int, page_poster
from .fields import *


class PostInfo:
    """Class with all available data"""
    __slots__ = ('ratings', 'rankings', 'slogan', 'release', 'country', 'director', 'genre', 'quality',
                 'translator', 'age_rating', 'duration_m', 'collections', 'persons', '_view', 'fields',
                 'title', 'orig_title', 'poster', 'description', 'duration', 'updated_time')
    FILL_FIELDS: tuple[str, ...] = __slots__[:13]
    'indicate autofilled fields'

    def __init__(self, soup: BeautifulSoup, *, url: str = None):
        """Initialize class from title page BeautifulSoup"""
        self.title = title.text.strip() if (title := soup.find(class_='b-post__title')) else ''
        self.duration = int(d.attrs.get('content', 0)) if (d := soup.select_one('meta[property="og:duration"]')) else 0
        if upload_time := soup.find('meta', property='og:updated_time'):
            self.updated_time = int(upload_time.attrs.get('content', 0))
        else:
            self.updated_time = 0
        orig_title = soup.find(class_='b-post__origtitle')
        self.orig_title = orig_title.text.strip() if orig_title else self.title

        self.poster = page_poster(soup)

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
            func = getattr(_parser, field, None)
            field_name = getdoc(func) or field.title()
            item = fields.get(field_name)
            if not item:
                setattr(self, field, None)
                continue
            processed = func(item) if func else item
            fields[field_name] = processed
            setattr(self, field, processed)

        rating_b = soup.find(class_='b-post__rating')
        if url is None:
            url = soup.find('meta', property='og:video').attrs.get('content', '')
        post_rating = Rating(service=Hyperlink(name='HDRezka', url=url),
                             rating=float(rating_b.select_one('[itemprop="average"]').text),
                             votes=get_any_int(rating_b.select_one('[itemprop="votes"]').text))
        if self.ratings is None:
            self.ratings = {}
        self.ratings['hdrezka'] = post_rating
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
