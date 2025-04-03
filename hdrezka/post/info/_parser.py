"""Module for parsing a Posts"""
__all__ = ('FieldsParse',)

from bs4 import Tag

from ._utils import *
from .fields import *
from ..urls import Quality


class FieldsParse:
    """Class contains staticmethod for parsing fields"""

    @staticmethod
    def get_field_rating(tag: Tag) -> dict[str, Rating]:
        """Рейтинги"""
        result = {}
        for span in tag.select('span.b-post__info_rates'):
            if a := span.find('a'):
                service = a.text
                url = parse_help_href(a['href'])
            else:
                service = url = ''
            match span.attrs.get('class'):
                case ['b-post__info_rates', k, *_]:
                    pass
                case [k, 'b-post__info_rates', *_]:
                    pass
                case _:
                    k = service.casefold()
            rating = float(rating_span.text) if (rating_span := span.find('span')) else 0.
            votes = get_any_int(votes_i.text) if (votes_i := span.find('i')) else 0
            result[k] = Rating(service=service, rating=rating, votes=votes, url=url)
        return result

    @staticmethod
    def get_field_places(tag: Tag) -> tuple[Place, ...]:
        """Входит в списки"""
        return *(Place(a.text, get_any_int(a.next_element.next_element)) for a in tag.find_all('a')),

    @staticmethod
    def get_field_slogan(tag: Tag) -> str:
        """Слоган"""
        return tag.get_text(strip=True)

    @staticmethod
    def get_field_release(tag: Tag) -> Release:
        """Дата выхода"""
        return Release(day='' if tag.next_element is None else tag.next_element.text.strip(),
                       year=0 if (a := tag.find('a')) is None else get_any_int(a.text))

    @staticmethod
    def get_field_country(tag: Tag) -> tuple[str, ...]:
        """Страна"""
        return *map(str.strip, tag.text.split(',')),

    @staticmethod
    def get_field_director(tag: Tag) -> str:
        """Режиссер"""
        return tag.get_text(strip=True)

    @staticmethod
    def get_field_genre(tag: Tag) -> tuple[str, ...]:
        """Жанр"""
        return *map(str.strip, tag.text.split(',')),

    @staticmethod
    def get_field_quality(tag: Tag):
        """В качестве"""
        return Quality(tag.text.strip())

    @staticmethod
    def get_field_translator(tag: Tag) -> str:
        """В переводе"""
        return tag.get_text(strip=True)

    @staticmethod
    def get_field_age_rating(tag: Tag) -> AgeRating:
        """Возраст"""
        return (AgeRating(0) if (span := tag.find('span')) is None else
                AgeRating(get_any_int(span.text), span.next_element.get_text(strip=True) if span.next_element else ''))

    @staticmethod
    def get_field_duration(tag: Tag) -> Duration:
        """Время"""
        d, u = tag.text.split(' ', 1)
        return Duration(int(d), u)

    @staticmethod
    def get_field_from_(tag: Tag) -> tuple[str]:
        """Из серии"""
        return *(a.text for a in tag.find_all('a')),

    @staticmethod
    def get_field_characters(tag: Tag) -> tuple[str, ...]:
        """В ролях актеры"""
        return *(span.text for span in tag.select('span[itemprop="name"]')),
