"""Global request settings"""
__all__ = ('Request',)

from urllib.parse import urljoin


class Request:
    """
    Contains global request parameters for HDRezka.
    Change `HOST` here in case the existing host is unavailable.

    See also [hdrezka.api.http.DEFAULT_CLIENT]
    """
    HOST: str = 'https://hdrezka.me/'
    REDIRECT_URL: str = 'https://rhs.to/'
    'Used in `hdrezka.api.http.login_global`'

    @classmethod
    def host_join(cls, url: str | None, allow_fragments: bool = True) -> str:
        """urljoin with `cls.HOST`"""
        return urljoin(cls.HOST, url, allow_fragments=allow_fragments)
