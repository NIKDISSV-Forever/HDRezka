"""Some internal utils"""
__all__ = ('get_any_int', 'parse_help_href')

import re
from base64 import b64decode
from typing import Any
from urllib.parse import unquote

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
