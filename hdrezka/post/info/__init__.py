"""Presentation of title information"""
__all__ = ('PostInfo',)

from typing import NamedTuple

from .fields import *
from .person import *
from ...post.urls.kind.quality import Quality


class PostInfo(NamedTuple):
    """General post information"""
    title: str
    orig_title: str
    poster: Poster
    duration: int
    updated_time: int
    ratings: dict[str, Rating]
    rankings: tuple[Rank, ...]
    slogan: str
    release: Release
    country: tuple[Hyperlink, ...]
    directors: tuple[Person, ...]
    genre: tuple[Hyperlink, ...]
    quality: Quality | None
    translators: tuple[str, ...]
    age_rating: AgeRating
    duration_m: int
    collections: tuple[Hyperlink, ...]
    persons: tuple[Person, ...]
    description: str
