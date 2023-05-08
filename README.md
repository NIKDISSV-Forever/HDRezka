# [HDRezka](https://rezka.ag/) site API.

# Install

`pip install HDRezka`

# Example

```python
import asyncio
from hdrezka import Search

async def main():
    player = await (await Search('Breaking Bad').get_page(1))[0].player  # or just use Player(646)
    print(player.post.info, end='\n\n')

    translator_id = None  # default
    for name, id_ in player.post.translators.name_id.items():
        if 'субтитры' in name.casefold(): translator_id = id_; break

    stream = await player.get_stream(1, 1, translator_id)  # raise AJAXFail if invalid episode or translator
    video = stream.video
    print(video.last_url)  # best quality (.m3u8)
    print(video[video.min].last_url.mp4, end='\n\n')  # worst quality (.mp4)

    subtitles = stream.subtitles
    print(subtitles.default.url)  # subtitles.ru.url or subtitles['Русский'].url

if __name__ == '__main__': asyncio.run(main())
```

# [Documentation](https://nikdissv-forever.github.io/HDRezka/hdrezka)
