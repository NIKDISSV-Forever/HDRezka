import urllib.parse

__all__ = ('Request',)


class Request:
    """
    Contains global request parameters for HDRezka.
    Change `HOST` here in case the existing host is unavailable.

    See also [hdrezka.api.http.DEFAULT_CLIENT]
    """
    HOST: str = 'https://hdrezka.ag/'

    @classmethod
    def host_join(cls, url: str | None, allow_fragments: bool = True) -> str:
        return urllib.parse.urljoin(cls.HOST, url, allow_fragments=allow_fragments)
