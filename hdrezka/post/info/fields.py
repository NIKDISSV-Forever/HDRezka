"""high-level structures for representing title data"""
from dataclasses import dataclass

__all__ = ('Rating', 'Place', 'Release', 'AgeRating', 'Duration', 'Poster')


@dataclass(frozen=True, slots=True)
class Rating:
    """Rating for service"""
    service: str
    rating: int | float
    votes: int


@dataclass(frozen=True, slots=True)
class Place:
    """Place of title"""
    name: str
    place: int


@dataclass(frozen=True, slots=True)
class Release:
    """Release date"""
    year: int
    day: str


@dataclass(frozen=True, slots=True)
class AgeRating:
    """Age restricts"""
    age: int
    description: str = ''


@dataclass(frozen=True, slots=True)
class Duration:
    """Duration of title"""
    number: int
    units: str


@dataclass(frozen=True, slots=True)
class Poster:
    """Poster of title"""
    full: str = ''
    preview: str = ''

    def __bool__(self):
        """Is any poster"""
        return not not (self.full or self.preview)
