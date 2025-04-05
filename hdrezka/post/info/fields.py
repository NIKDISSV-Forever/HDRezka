"""High-level structures for representing title data"""
__all__ = ('Hyperlink', 'Rating', 'Rank', 'Release', 'AgeRating', 'Poster', 'Birthplace')

from typing import NamedTuple


class Hyperlink(NamedTuple):
    """Hyperlink representation"""
    name: str = ''
    url: str = ''

    def __str__(self):
        return self.name


class Rating(NamedTuple):
    """Rating for service"""
    service: Hyperlink
    rating: int | float
    votes: int


class Rank(NamedTuple):
    """Rank of title"""
    name: Hyperlink
    rank: int


class Release(NamedTuple):
    """Release date"""
    day: str
    year: int


class AgeRating(NamedTuple):
    """Age restricts"""
    age: int
    description: str = ''


class Poster(NamedTuple):
    """Poster of title"""
    full: str = ''
    preview: str = ''

    def __bool__(self):
        """Is any poster"""
        return not not (self.full or self.preview)


class Birthplace(NamedTuple):
    """Birthplace information"""
    country: str
    city: str | None = None
    subcountry: str | None = None
    state: str | None = None
