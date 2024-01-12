"""high-level representation of video quality"""
from .._regexes import match_quality_int

__all__ = ('Quality',)


class Quality(str):
    """str type add-on to represent video quality"""
    __slots__ = ('_i', 'addon')
    addon: str

    def __init__(self, *_, **__):
        """Sets addon attribute (can contain 'ultra')"""
        _i = match_quality_int(self)
        if not _i:
            raise ValueError(f'{self!r} is not quality.')
        _i, self.addon = _i.groups()
        self.addon = self.addon.casefold()
        self._i = int(_i)

    def __int__(self):
        """
        returns pixels height
        """
        return self._i

    def __lt__(self, other):
        """Is other quality better then self"""
        if not isinstance(other, self.__class__):
            return super().__le__(other)
        if not (self.addon or other.addon):
            return self._i < int(other)
        return False
