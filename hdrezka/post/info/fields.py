from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

__all__ = ('Rating', 'Place', 'Release', 'AgeRating', 'Duration', 'Poster')


@dataclass(frozen=True)
class Rating:
    __slots__ = ('service', 'rating', 'votes')
    service: str
    rating: int | float
    votes: int


@dataclass(frozen=True)
class Place:
    __slots__ = ('name', 'place')
    name: str
    place: int


@dataclass(frozen=True)
class Release:
    __slots__ = ('day', 'year')
    year: int
    day: str


@dataclass(frozen=True)
class AgeRating:
    __slots__ = ('age', 'description')
    age: int
    description: str


@dataclass(frozen=True)
class Duration:
    __slots__ = ('number', 'units')
    number: int
    units: str


class Poster(NamedTuple):
    full: str
    preview: str
