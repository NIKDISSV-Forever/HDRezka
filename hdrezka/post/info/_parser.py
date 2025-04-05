"""Module for parsing a Posts"""
__all__ = ()

from bs4 import Tag

from ._utils import *
from .fields import *
from .person import Person
from ..urls import Quality


def ratings(tag: Tag) -> dict[str, Rating]:
    """Рейтинги"""
    result = {}
    for span in tag.select('span.b-post__info_rates'):
        if a := span.find('a'):
            service = a.text
            url = parse_help_href(a['href'])
        else:
            service = span.next_element.text.strip().removesuffix(':')
            url = ''
        match span.attrs.get('class'):
            case ['b-post__info_rates', k, *_]:
                pass
            case [k, 'b-post__info_rates', *_]:
                pass
            case _:
                k = service.casefold()
        rating = float(rating_span.text) if (rating_span := span.find('span')) else 0.
        votes = get_any_int(votes_i.text) if (votes_i := span.find('i')) else 0
        result[k] = Rating(service=Hyperlink(name=service, url=url), rating=rating, votes=votes)
    return result


def rankings(tag: Tag) -> tuple[Rank, ...]:
    """Входит в списки"""
    return *(Rank(hyperlink(a), get_any_int(a.next_element.next_element)) for a in tag.find_all('a')),


def slogan(tag: Tag) -> str:
    """Слоган"""
    return tag.get_text(strip=True)


def release(tag: Tag) -> Release:
    """Дата выхода"""
    return Release(day='' if tag.next_element is None else tag.next_element.text.strip(),
                   year=0 if (a := tag.find('a')) is None else int(a.text.split(maxsplit=1)[0]))


def country(tag: Tag) -> tuple[Hyperlink, ...]:
    """Страна"""
    return *map(hyperlink, tag.find_all('a')),


def director(tag: Tag) -> str:
    """Режиссер"""
    return tag.get_text(strip=True)


def genre(tag: Tag) -> tuple[Hyperlink, ...]:
    """Жанр"""
    return *map(hyperlink, tag.find_all('a')),


def quality(tag: Tag):
    """В качестве"""
    return Quality(tag.text.strip())


def translator(tag: Tag) -> str:
    """В переводе"""
    return tag.get_text(strip=True)


def age_rating(tag: Tag) -> AgeRating:
    """Возраст"""
    return (AgeRating(0) if (span := tag.find('span')) is None else
            AgeRating(get_any_int(span.text), span.next_element.get_text(strip=True) if span.next_element else ''))


def duration_m(tag: Tag) -> int:  # duration in minutes
    """Время"""
    return int(tag.text.split(' ', 1)[0])


def collections(tag: Tag) -> tuple[Hyperlink, ...]:
    """Из серии"""
    return *map(hyperlink, tag.find_all('a')),


def persons(tag: Tag) -> tuple[Person, ...]:
    """В ролях актеры"""
    return *(Person(a.attrs.get('href', ''), name=a.text) for a in tag.find_all('a')),
