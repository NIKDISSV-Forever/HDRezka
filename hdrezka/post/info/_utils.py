"""Some internal utils"""
__all__ = ('get_any_int', 'parse_help_href', 'hyperlink', 'page_poster')

import re
from base64 import b64decode
from typing import Any
from urllib.parse import unquote

from bs4 import Tag, BeautifulSoup

from .fields import Hyperlink, Poster

_find_any_digit = re.compile(r'\d+').findall


def get_any_int(value: Any, /, default: int = 0) -> int:
    """Convert Any to int"""
    if not isinstance(value, str):
        value = str(value)
    if digits := _find_any_digit(value):
        return int(''.join(digits))
    return default


def parse_help_href(href: str) -> str:
    """Returns encoded in base64 url"""
    return unquote(b64decode(href.removeprefix('/help/').removesuffix('/')).decode())


def hyperlink(tag: Tag) -> Hyperlink:
    """Returns Hyperlink from tag"""
    return Hyperlink(tag.text, tag.attrs.get('href', ''))


def page_poster(soup: BeautifulSoup | Tag) -> Poster:
    """Returns big and small Poster"""
    if poster := soup.select_one('.b-sidecover>a'):
        return Poster(poster.attrs.get('href', ''), poster.find('img').attrs.get('src', ''))
    return Poster()
