"""High-level representation of video quality"""
__all__ = ('Quality',)

import re

_match_quality_int = re.compile(r'(\d+)([piK])\s*($|\w+)').match


class Quality(str):
    """str type add-on to represent video quality"""
    __slots__ = ('_i', 'addon', 'units')
    addon: str

    def __init__(self, *_, **__):
        """Sets addon attribute (can contain 'ultra')"""
        _i = _match_quality_int(self)
        if not _i:
            raise ValueError(f'{self!r} is unknown quality.')
        _i, units, self.addon = _i.groups()
        if units == 'K':
            _i += '000'
            units = 'p'
        self.addon = self.addon.casefold()
        self._i = int(_i)
        self.units = units

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
