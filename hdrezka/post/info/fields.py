from .._dataclass import frozen_slots_dataclass

__all__ = ('Rating', 'Place', 'Release', 'AgeRating', 'Duration', 'Poster')


@frozen_slots_dataclass
class Rating:
    service: str
    rating: int | float
    votes: int = 0


@frozen_slots_dataclass
class Place:
    name: str
    place: int


@frozen_slots_dataclass
class Release:
    year: int
    day: str


@frozen_slots_dataclass
class AgeRating:
    age: int
    description: str


@frozen_slots_dataclass
class Duration:
    number: int
    units: str


@frozen_slots_dataclass
class Poster:
    full: str
    preview: str
