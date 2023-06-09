from .http import get_response
from ..errors import AJAXFail

__all__ = ('AJAX', 'AnyID')

AnyID = int | str


class AJAX:
    """HDRezka AJAX class"""
    __slots__ = ()

    @classmethod
    async def _send_data(cls, action: str, data: dict[str]) -> dict[str]:
        answer: dict = (await get_response('POST', f'https://rezka.ag/ajax/{action}/', data=data)).json()
        if not answer.get('success', True):
            raise AJAXFail(answer.get('message', answer))
        return answer

    @classmethod
    async def get_cdn_series(cls, data: dict[str]):
        return await cls._send_data('get_cdn_series', data)

    @classmethod
    async def get_episodes(cls, id: AnyID, translator_id: AnyID):
        return await cls.get_cdn_series(
            {'action': 'get_episodes',
             'id': id,
             'translator_id': translator_id})

    @classmethod
    async def get_stream(cls, id: AnyID, translator_id: AnyID, season: AnyID, episode: AnyID):
        return await cls.get_cdn_series(
            {'action': 'get_stream',
             'id': id,
             'translator_id': translator_id,
             'season': season,
             'episode': episode}
        )

    @classmethod
    async def get_movie(cls, id: AnyID, translator_id: AnyID):
        return await cls.get_cdn_series(
            {'action': 'get_movie',
             'id': id,
             'translator_id': translator_id}
        )
