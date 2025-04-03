"""High-level structures for representing title data"""
__all__ = ('Rating', 'Place', 'Release', 'AgeRating', 'Duration', 'Poster')

from typing import NamedTuple


class Rating(NamedTuple):
    """Rating for service"""
    service: str
    rating: int | float
    votes: int
    url: str


class Place(NamedTuple):
    """Place of title"""
    name: str
    place: int


class Release(NamedTuple):
    """Release date"""
    year: int
    day: str


class AgeRating(NamedTuple):
    """Age restricts"""
    age: int
    description: str = ''


class Duration(NamedTuple):
    """Duration of title"""
    number: int
    units: str


class Poster(NamedTuple):
    """Poster of title"""
    full: str = ''
    preview: str = ''

    def __bool__(self):
        """Is any poster"""
        return not not (self.full or self.preview)
