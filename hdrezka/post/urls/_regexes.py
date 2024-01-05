import re

__all__ = ('findall_qualities', 'findall_subtitles', 'match_quality_int')

findall_qualities = re.compile(r'\[([^]]+)](\S+)(?:\sor\s|$)').findall
findall_subtitles = re.compile(r'\[([^]]+)]([^,]+)(?:,|$)').findall
match_quality_int = re.compile(r'(\d+)[pi]\s*($|\w+)').match
