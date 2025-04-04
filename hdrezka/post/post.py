"""General post module"""
__all__ = ('Post',)

import urllib.parse

from bs4 import BeautifulSoup

from .info import PostInfo
from .info.franchises import FranchiseInfo
from .._bs4 import BUILDER
from ..api.http import get_response
from ..translators import Translators
from ..url import Request


class Post:
    """Stores information about the post"""
    __slots__ = ('url', 'translator_id', 'id', 'name', 'type', 'info', 'translators', 'franchises')

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
        response = yield from get_response('GET', self.url).__await__()
        soup = BeautifulSoup(response.text, builder=BUILDER)
        self.type = soup.find('meta', property='og:type')['content'].removeprefix('video.')
        self.translator_id = self._get_translator_id(soup)
        self.info = PostInfo(soup, url=self.url)
        self.translators = self._get_translators(soup)

        self.id = int(soup.find(id='post_id')['value'])
        self.name = soup.find(class_='b-post__title').text.strip()
        franchises_url = soup.find(class_='b-post__franchise_link_title')
        self.franchises = FranchiseInfo(url=franchises_url and franchises_url.attrs.get('href'), soup=soup)

    def _get_translator_id(self, soup: BeautifulSoup) -> int | None:
        """self.type must exist"""
        init_cdn_obj = 'sof.tv.%s' % {'tv_series': 'initCDNSeriesEvents', 'movie': 'initCDNMoviesEvents'}[self.type]
        for script in soup.find_all(lambda tag: tag.name == 'script' and not tag.attrs and tag.string):
            s = script.string
            obj_i = s.find(init_cdn_obj)
            if obj_i != -1:
                s = s[obj_i + len(init_cdn_obj):].split(',', 2)[1].strip()
                if s.isnumeric():
                    return int(s)
        return None

    def _get_translators(self, soup: BeautifulSoup) -> Translators:
        translators_list = soup.find(id='translators-list')
        arr = {child.text.strip(): int(child['data-translator_id']) for child in
               translators_list.find_all(recursive=False) if child.text} if translators_list else {}
        if not arr:
            arr[self.info.translator] = self.translator_id
        return Translators(arr)

    def _get_franchises(self, _soup_inst: BeautifulSoup) -> tuple[str]:
        franchises = *(
            i.attrs['data-url'] for i in
            _soup_inst.select('.b-post__partcontent_item[data-url]')),
        return franchises

    def __repr__(self):
        return f'{self.__class__.__qualname__}<{self.name!r}; {self.type!r}>'
