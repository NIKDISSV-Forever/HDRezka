import re

__all__ = ('findall_qualities', 'findall_subtitles', 'shorten_url_match', 'match_quality_int')

findall_qualities = re.compile(r'\[([^]]+)](\S+)(?:\sor\s|$)').findall
findall_subtitles = re.compile(r'\[([^]]+)]([^,]+)(?:,|$)').findall
shorten_url_match = re.compile(r'(?:(?:https?://)?rezka\.ag/)?\D*(\d+)\S*(?:\.html)?/?', re.I).match
match_quality_int = re.compile(r'(\d+)[pi]\s*($|\w+)').match
