import urllib.parse

from bs4 import BeautifulSoup

from ._bs4 import _BUILDER
from .info import PostInfo
from ..api.http import get_response
from ..translators import Translators

__all__ = ('Post',)

from ..url import Request


class Post:
    """Stores information about the post"""
    __slots__ = ('url', 'translator_id', 'id', 'name', 'type', 'info', 'translators', 'other_parts_urls',
                 '_soup_inst')

    def __init__(self, url: str):
        """Need await"""
        if not urllib.parse.urlparse(url).hostname:
            url = Request.host_join(url)
        self.url = url

    def __await__(self):
        """
        Async initialize, prepare attributes.
        Do not call twice!
        """
        _response = yield from get_response('GET', self.url).__await__()
        _response = _response.text
        self._soup_inst = BeautifulSoup(_response, builder=_BUILDER)
        self.type = self._get_type()

        self.translator_id = int(i) if (i := _response.split(
            'sof.tv.' + {'tv_series': 'initCDNSeriesEvents', 'movie': 'initCDNMoviesEvents'}[self.type],
            1)[-1].split(',')[1].strip()).isnumeric() else None
        self.info = self._get_post_info()
        self.translators = self._get_translators()

        self.id = self._extract_id()
        self.name = self._get_name()
        self.other_parts_urls = self._parts_urls

    def _extract_id(self) -> int:
        return int(self._soup_inst.find(id='post_id')['value'])

    def _get_name(self) -> str:
        return self._soup_inst.find(class_='b-post__title').text.strip()

    def _get_type(self) -> str:
        return self._soup_inst.find('meta', property='og:type')['content'].removeprefix('video.')

    def _get_post_info(self) -> PostInfo:
        return PostInfo(self._soup_inst)

    def _get_translators(self) -> Translators:
        translators_list = self._soup_inst.find(id='translators-list')
        arr = {child.text.strip(): int(child['data-translator_id']) for child in
               translators_list.find_all(recursive=False) if child.text} if translators_list else {}
        if not arr:
            arr[self.info.translator] = self.translator_id
        return Translators(arr)

    @property
    def _parts_urls(self) -> tuple[str]:
        self.other_parts_urls = *(
            i.attrs['data-url'] for i in
            self._soup_inst.select('.b-post__partcontent_item[data-url]')),
        return self.other_parts_urls

    def __repr__(self):
        return f'{self.__class__.__qualname__}<{self.name!r}; {self.type!r}>'
