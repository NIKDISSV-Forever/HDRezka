from __future__ import annotations

from bs4 import BeautifulSoup

from .api import get_response

__all__ = ('Page',)

from .translators import Translators


class Page:
    """Stores information about the page"""
    __slots__ = ('_soup_inst', 'url', 'translator_id', 'id', 'name', 'type', 'translators', 'other_parts_urls')

    def __init__(self, url: str):
        self.url = url
        _response = get_response('GET', url).text
        self._soup_inst = BeautifulSoup(_response)
        self.type = self._get_type()

        self.translator_id = int(i) if (i := _response.split(
            'sof.tv.' + {'tv_series': 'initCDNSeriesEvents', 'movie': 'initCDNMoviesEvents'}[self.type],
            1)[-1].split(',')[1].strip()).isnumeric() else None
        self.translators = self._get_translators()

        self.id = self._extract_id()
        self.name = self._get_name()
        self.other_parts_urls = self._parts_urls

    def _extract_id(self):
        return int(self._soup_inst.find(id='post_id')['value'])

    def _get_name(self):
        return self._soup_inst.find(class_='b-post__title').get_text().strip()

    def _get_type(self):
        return self._soup_inst.find('meta', property='og:type')['content'].removeprefix('video.')

    def _get_translators(self):
        translators_list = self._soup_inst.find(id='translators-list')
        arr = {child.text.strip(): int(child['data-translator_id']) for child in
               translators_list.find_all(recursive=False) if child.text} if translators_list else {}
        if not arr:
            arr[next((tr.text.split(':', 1)[-1].strip() for tr in self._soup_inst.select('.b-post__info>tr') if
                      tr.text.strip().startswith('В переводе:')), '')] = self.translator_id
        return Translators(arr)

    @property
    def _parts_urls(self) -> tuple[str]:
        self.other_parts_urls = *(
            i.attrs['data-url'] for i in
            self._soup_inst.select('.b-post__partcontent_item[data-url]')),
        return self.other_parts_urls

    def __repr__(self):
        return f'{self.__class__.__qualname__}<{self.name!r}; {self.type!r}>'
