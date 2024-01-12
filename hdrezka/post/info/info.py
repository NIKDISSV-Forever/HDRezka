"""title page parsing operations"""
import re
from inspect import getdoc
from typing import Any

from bs4 import BeautifulSoup, Tag

from .fields import *
from ..urls import Quality

__all__ = ('PostInfo',)
_find_any_digit = re.compile(r'\d+').findall


def _get_int(value: Any, /, default: int = 0) -> int:
    if not isinstance(value, str):
        value = str(value)
    if digits := _find_any_digit(value):
        return int(''.join(digits))
    return default


class PostInfo:
    """Class with all available data"""
    __slots__ = ('rating', 'places', 'slogan', 'release', 'country', 'director', 'genre',
                 'quality', 'translator', 'age_rating', 'duration', 'from_', 'characters',
                 '_view', 'fields', 'title', 'orig_title', 'poster', 'description')
    FILL_FIELDS: tuple[str, ...] = __slots__[:13]

    def __init__(self, soup: BeautifulSoup):
        """Initialize class from title page BeautifulSoup"""
        title = soup.find(class_='b-post__title')
        if title is None:
            self.title = ''
        else:
            self.title = title.text.strip()
        orig_title = soup.find(class_='b-post__origtitle')
        self.orig_title = orig_title.text.strip() if orig_title else self.title
        poster: Tag | None | dict[str, str] = soup.select_one('.b-sidecover>a img')
        if poster is None:
            poster_href = poster_src = ''
        else:
            match m := poster.get('href', ''):
                case None:
                    poster_href = ''
                case [poster_href, *_]:
                    pass
                case str(poster_href):
                    pass
                case _:
                    poster_href = str(m)
            match m := poster.get('src', ''):
                case None:
                    poster_src = ''
                case [poster_src, *_]:
                    pass
                case str(poster_src):
                    pass
                case _:
                    poster_src = str(m)
        self.poster = Poster(poster_href, poster_src)
        description = soup.find(class_='b-post__description_text')
        if description is None:
            self.description = ''
        else:
            self.description = description.text.strip()
        post_info: Tag | None = soup.find(class_='b-post__info')
        if post_info is None:
            raw_fields: list[Tag] = []
        else:
            self._view = self._form_view(post_info.find_all('tr'))
            raw_fields = post_info.select('tr>td')
            if len(raw_fields) % 2:
                raw_fields.append(raw_fields[-1])

        fields = {h2.text.strip().removesuffix(':'): raw_fields[i + 1]
                  for i in range(0, len(raw_fields), 2) if (h2 := raw_fields[i].find('h2')) is not None}
        for field in self.FILL_FIELDS:
            meth = getattr(self, f'_get_field_{field}', None)
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
        self.fields = fields

    @staticmethod
    def _get_field_rating(tag: Tag) -> dict[str, Rating]:
        """Рейтинги"""
        result = {}
        for span in tag.select('span.b-post__info_rates'):
            classes = span.get('class')
            if classes is None:
                classes = []
            elif isinstance(classes, str):
                classes = [classes]
            classes.remove('b-post__info_rates')
            a = span.find('a')
            service = '' if a is None else a.text
            votes_i = span.find('i')
            if votes_i:
                votes = _get_int(votes_i.text)
            else:
                votes = -1
            rating_span = span.find('span')
            if rating_span is None:
                rating = 0.
            else:
                rating = float(rating_span.text)
            result[classes[0] if classes else service] = Rating(
                service=service, rating=rating, votes=votes)
        return result

    @staticmethod
    def _get_field_places(tag: Tag) -> tuple[Place, ...]:
        """Входит в списки"""
        return *(Place(a.text, _get_int(a.next_element.next_element)) for a in tag.find_all('a')),

    @staticmethod
    def _get_field_slogan(tag: Tag) -> str:
        """Слоган"""
        return tag.get_text(strip=True)

    @staticmethod
    def _get_field_release(tag: Tag) -> Release:
        """Дата выхода"""
        return Release(day='' if tag.next_element is None else tag.next_element.text.strip(),
                       year=0 if (a := tag.find('a')) is None else _get_int(a.text))

    @staticmethod
    def _get_field_country(tag: Tag) -> tuple[str, ...]:
        """Страна"""
        return *map(str.strip, tag.text.split(',')),

    @staticmethod
    def _get_field_director(tag: Tag) -> str:
        """Режиссер"""
        return tag.get_text(strip=True)

    @staticmethod
    def _get_field_genre(tag: Tag) -> tuple[str, ...]:
        """Жанр"""
        return *map(str.strip, tag.text.split(',')),

    @staticmethod
    def _get_field_quality(tag: Tag):
        """В качестве"""
        return Quality(tag.text.strip())

    @staticmethod
    def _get_field_translator(tag: Tag) -> str:
        """В переводе"""
        return tag.get_text(strip=True)

    @staticmethod
    def _get_field_age_rating(tag: Tag) -> AgeRating:
        """Возраст"""
        span = tag.find('span')
        if span is None:
            return AgeRating(-1)
        return AgeRating(_get_int(span.text),
                         '' if span.next_element is None else span.next_element.get_text(strip=True))

    @staticmethod
    def _get_field_duration(tag: Tag) -> Duration:
        """Время"""
        d, u = tag.text.split(' ', 1)
        return Duration(int(d), u)

    @staticmethod
    def _get_field_from_(tag: Tag) -> tuple[str]:
        """Из серии"""
        return *(a.text for a in tag.find_all('a')),

    @staticmethod
    def _get_field_characters(tag: Tag) -> tuple[str, ...]:
        """В ролях актеры"""
        return *(span.text for span in tag.select('span[itemprop="name"]')),

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
