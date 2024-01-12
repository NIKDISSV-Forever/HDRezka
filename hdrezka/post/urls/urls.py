"""All urls for one video"""
from dataclasses import dataclass

from .kind import SubtitleURLs, VideoURLs
from ...api.types import APIResponse


@dataclass(frozen=True, slots=True)
class URLs:
    """All urls for one video class"""
    video: VideoURLs
    subtitles: SubtitleURLs


def urls_from_ajax_response(response: APIResponse) -> URLs:
    """Parse response and return urls"""
    return URLs(VideoURLs(response.get('url', '')),
                SubtitleURLs(response.get('subtitle', ''),
                             response.get('subtitle_lns', {'off': ''}),
                             response.get('subtitle_def', '')))
