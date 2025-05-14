"""Module for parsing a Posts"""
__all__ = ('get_post_info',)

from bs4 import BeautifulSoup

from . import *
from ..info import PostInfo
from ..info.fields import *
from ..info.person import Person
from ..urls import Quality


def get_post_info(soup: BeautifulSoup, *, url: str | None = None) -> PostInfo:
    """Parse post info table from page soup"""
    if url is None:
        url = attr(soup.find('meta', property='og:video'), 'content', default='')
    title = text(soup.find('h1', itemprop='name'))
    tables = {i.find('h2').next_element.text: i.select_one('td:not(:has(h2))') for i in soup.select('tr:has(td>h2)')}
    get = lambda _k: tables.get(_k, empty_tag)
    ratings = {}
    for span in get('Рейтинги').select('span'):
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
        rating = float(text(span.find('span'), 0.))
        votes = get_any_int(text(span.find('i'), 0))
        ratings[k] = Rating(service=Hyperlink(name=service, url=url), rating=rating, votes=votes)
    rating_b = soup.find(class_='b-post__rating')
    ratings['hdrezka'] = Rating(service=Hyperlink(name='HDRezka', url=url),
                                rating=float(rating_b.find(itemprop='average').text),
                                votes=get_any_int(rating_b.find(itemprop='votes').text))
    release_tag = get('Дата выхода')
    return PostInfo(
        title=title,
        orig_title=text(soup.find(itemprop='alternativeHeadline'), title),
        poster=sidecover(soup),
        description=text(soup.find(class_='b-post__description_text')),
        duration=int(attr(soup.find('meta', property='og:duration'), 'content', default=0)),
        updated_time=int(attr(soup.find('meta', property='og:updated_time'), 'content', default=0)),
        ratings=ratings,
        rankings=(*(Rank(hyperlink(a), get_any_int(a.next_element.next_element))
                    for a in get('Входит в списки').select('a')),),
        slogan=text(get('Слоган')).removeprefix('«').removesuffix('»'),
        release=Release(day=text(release_tag.next_element),
                        year=int(text(release_tag.find('a'), '0').split(' ', 1)[0])),
        country=hyperlinks(get('Страна')),
        directors=(*(Person(a.attrs.get('href', ''), name=a.text) for a in get('Режиссер').select('a')),),
        genre=hyperlinks(get('Жанр')),
        quality=Quality(t) if (t := text(get('В качестве'))) else None,
        translators=(*map(str.strip, text(get('В переводе')).split(',')),),
        age_rating=(AgeRating(0) if (span := get('Возраст').find('span')) is None else
                    AgeRating(get_any_int(span.text), text(span.next_element.next_element))),
        duration_m=int(text(get('Время')).split(' ', 1)[0]),
        collections=hyperlinks(get('Из серии')),
        persons=(*(Person(a.attrs.get('href', ''), name=a.text) for a in soup.select('[itemprop="actor"]>a')),),
    )
