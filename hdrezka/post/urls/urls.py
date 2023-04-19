from .kind import SubtitleURLs, VideoURLs
from .._dataclass import frozen_slots_dataclass


@frozen_slots_dataclass
class URLs:
    video: VideoURLs
    subtitles: SubtitleURLs


def urls_from_ajax_response(response: dict[str]) -> URLs:
    return URLs(VideoURLs(response.get('url', '')),
                SubtitleURLs(response.get('subtitle', False),
                             response.get('subtitle_lns', False), response.get('subtitle_def', False)))
