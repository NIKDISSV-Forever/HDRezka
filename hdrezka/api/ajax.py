from __future__ import annotations

from . import get_response
from ..errors import AjaxFail

__all__ = ('Ajax',)


class Ajax:
    """HDRezka Ajax class"""
    __slots__ = ()

    @classmethod
    def _send_data(cls, action: str, data: dict[str]) -> dict:
        answer: dict = get_response('POST', f'https://rezka.ag/ajax/{action}/', data=data).json()
        if not answer.get('success', True):
            raise AjaxFail(answer.get('message', answer))
        return answer

    @classmethod
    def get_cdn_series(cls, data: dict[str]):
        return cls._send_data('get_cdn_series', data)

    @classmethod
    def get_episodes(cls, id: int | str, translator_id: int | str):
        return cls.get_cdn_series(
            {'action': 'get_episodes',
             'id': id,
             'translator_id': translator_id})

    @classmethod
    def get_stream(cls, id: int | str, translator_id: int | str, season: int | str, episode: int | str):
        return cls.get_cdn_series(
            {'action': 'get_stream',
             'id': id,
             'translator_id': translator_id,
             'season': season,
             'episode': episode}
        )

    @classmethod
    def get_movie(cls, id: int | str, translator_id: int | str):
        return cls.get_cdn_series(
            {'action': 'get_movie',
             'id': id,
             'translator_id': translator_id}
        )
