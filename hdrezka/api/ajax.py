"""Sending AJAX requests"""
__all__ = ('AJAX',)

from typing import SupportsInt

import httpx

from .http import get_response
from ..api.types import *
from ..errors import AJAXFail
from ..url import Request


class AJAX:
    """Class with methods for sending AJAX requests to the API"""
    __slots__ = ()

    @classmethod
    def _check(cls, resp: httpx.Response):
        answer = resp.json()
        if not answer.get('success', True):
            raise AJAXFail(answer.get('message', answer))
        return answer

    @classmethod
    async def _send_data(cls, action: str, **kwargs):
        return cls._check(await get_response('POST', Request.host_join(f'ajax/{action}/'), **kwargs))

    @classmethod
    async def get_cdn_series(cls, data: dict[str, SupportsInt | str]):
        """Request series for one translation"""
        return await cls._send_data('get_cdn_series', data=data)

    @classmethod
    async def get_episodes(cls, id_: SupportsInt | str, translator_id: SupportsInt | str):
        """Request episodes"""
        return await cls.get_cdn_series(
            {'action': 'get_episodes',
             'id': id_,
             'translator_id': translator_id}
        )

    @classmethod
    async def get_stream(cls, id_: SupportsInt | str, translator_id: SupportsInt | str,
                         season: SupportsInt | str, episode: SupportsInt | str) -> APIResponse:
        """Request stream urls"""
        return await cls.get_cdn_series(
            {'action': 'get_stream',
             'id': id_,
             'translator_id': translator_id,
             'season': season,
             'episode': episode}
        )

    @classmethod
    async def get_movie(cls, id_: SupportsInt | str, translator_id: SupportsInt | str):
        """Request movie urls"""
        return await cls.get_cdn_series(
            {'action': 'get_movie',
             'id': id_, 'translator_id': translator_id}
        )

    @classmethod
    async def get_trailer_video(cls, id_: SupportsInt | str) -> TrailerResponse:
        """Request trailer video iframe"""
        return cls._check(await get_response('POST', Request.host_join('engine/ajax/gettrailervideo.php'),
                                             data={'id': id_}))
