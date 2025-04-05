"""Inline item datatypes"""
__all__ = ('InlineItem', 'InlineInfo')

from types import EllipsisType
from typing import NamedTuple


class InlineInfo(NamedTuple):
    """Info about inline item (bottom)"""
    year: int
    year_final: int | EllipsisType | None
    'If the film is equal to None, if ongoing, equal `...`'
    country: str
    genre: str


class InlineItem(NamedTuple):
    """Content Inline Item view"""
    url: str
    name: str
    info: InlineInfo
    poster: str
    'Image url'

    @property
    async def player(self):
        """Return a Player Instance"""
        from .. import Player
        return await Player(self.url)
