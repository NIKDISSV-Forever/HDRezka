# [HDRezka](https://rezka.ag/) site API.

# Install

`pip install HDRezka`

# Example

```python
from hdrezka import Search

player = Search('Breaking Bad')[1, 0].player  # page 1 element 0; or just use Player(646)
print(player.post.info, end='\n\n')

translator_id = None  # default
for name, id_ in player.post.translators.name_id.items():
    if 'субтитры' in name.casefold(): translator_id = id_; break

stream = player.get_stream(1, 1, translator_id)  # raise AJAXFail if invalid episode or translator
video = stream.video
print(video.last_url)  # best quality
print(video[video.min].last_url.mp4, end='\n\n')

subtitles = stream.subtitles
print(subtitles.default.url)  # subtitles.ru.url or subtitles['Русский'].url
```

# [Documentation](https://nikdissv-forever.github.io/HDRezka/hdrezka)
