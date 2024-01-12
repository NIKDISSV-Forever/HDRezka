"""API response types"""
from typing import TypedDict

__all__ = ('APIResponse',)


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
