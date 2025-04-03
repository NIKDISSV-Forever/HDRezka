"""All urls for one video"""
__all__ = ('URLs', 'urls_from_ajax_response')

from typing import NamedTuple

from .kind import SubtitleURLs, VideoURLs
from ...api.types import APIResponse


class URLs(NamedTuple):
    """All urls for one video class"""
    video: VideoURLs
    subtitles: SubtitleURLs


def urls_from_ajax_response(response: APIResponse) -> URLs:
    """Parse response and return urls"""
    return URLs(VideoURLs(response.get('url', '')),
                SubtitleURLs(response.get('subtitle', ''),
                             response.get('subtitle_lns', {'off': ''}),
                             response.get('subtitle_def', '')))
