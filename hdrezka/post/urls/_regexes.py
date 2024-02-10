import re

from typing import Callable

__all__ = ('findall_qualities', 'findall_subtitles', 'match_quality_int')

findall_qualities = re.compile(r'\[([^]]+)](\S+)(?:\sor\s|$)').findall
findall_subtitles: Callable[[str], list[tuple[str, str]]] = re.compile(r'\[([^]]+)]([^,]+)(?:,|$)').findall
match_quality_int = re.compile(r'(\d+)([piK])\s*($|\w+)').match
