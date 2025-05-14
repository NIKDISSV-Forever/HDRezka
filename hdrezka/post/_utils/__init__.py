"""Some internal utils"""
__all__ = ('get_any_int', 'parse_help_href', 'hyperlink', 'text', 'attr',
           'hyperlinks', 'empty_tag', 'poster_and_soup', 'sidecover')

import re
from base64 import b64decode
from typing import Any
from urllib.parse import unquote

from bs4 import Tag, BeautifulSoup

from ..info.fields import *
from ..._bs4 import BUILDER
from ...api.http import get_response

empty_tag = BeautifulSoup('<div></div>', builder=BUILDER).find('div')
_find_any_digit = re.compile(r'\d+').findall
_empty_href = Hyperlink()
_empty_poster = Poster()


def text(tag: Tag | None, default: Any = ''):
    """Get tag text"""
    if tag is None:
        return default
    return tag.text.strip()


def attr(tag: Tag | None, name: str, *, default=None):
    """Get tag attribute"""
    if tag is None:
        return default
    return tag.attrs.get(name, default)


def hyperlinks(tag: Tag) -> tuple[Hyperlink, ...]:
    """Get tag hyperlinks"""
    return *map(hyperlink, tag.find_all('a')),


def get_any_int(value: Any, /, default: int = 0) -> int:
    """Convert Any to int"""
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        value = str(value)
    if digits := _find_any_digit(value):
        return int(''.join(digits))
    return default


def parse_help_href(href: str) -> str:
    """Returns encoded in base64 url"""
    return unquote(b64decode(href.removeprefix('/help/').removesuffix('/')).decode())


def hyperlink(tag: Tag | None) -> Hyperlink:
    """Returns Hyperlink from tag"""
    if not tag:
        return _empty_href
    return Hyperlink(tag.text, tag.attrs.get('href', ''))


def sidecover(tag: BeautifulSoup) -> Poster:
    """Returns sidecover Poster"""
    return (Poster(attr(poster.find('a'), 'href', default=''), attr(poster.find('img'), 'src', default=''))
            if (poster := tag.find(class_='b-sidecover')) else _empty_poster)


async def poster_and_soup(url: str) -> tuple[BeautifulSoup, Poster] | None:
    """Returns soup and poster from url"""
    if not url:
        return None
    soup = BeautifulSoup((await get_response('GET', url)).content, builder=BUILDER)
    return soup, sidecover(soup)
