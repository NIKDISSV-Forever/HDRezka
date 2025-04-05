"""API response types"""
__all__ = ('APIResponse', 'TrailerResponse')

from typing import TypedDict


class APIResponse(TypedDict):
    """Structure of the response to any request to the API"""
    success: bool
    message: str
    url: str
    quality: str
    subtitle: str
    subtitle_lns: dict[str, str]
    subtitle_def: str
    thumbnails: str


class TrailerResponse(TypedDict):
    """Structure of the response to trailer iframe request"""
    success: bool
    message: str
    code: str
    title: str
    description: str
    link: str
