r"""
# HDRezka site API

# Install

`pip install HDRezka`

# Example

```python
import asyncio
import os

from hdrezka import Search
from hdrezka.api.http import login_global


async def main():
    await login_global(os.environ['LOGIN_NAME'], os.environ['LOGIN_PASSWORD'])
    player = await (await Search('Breaking Bad').get_page(1))[0].player
    # or use url (await Player('series/thriller/646-vo-vse-tyazhkie-2008.html'))
    print(player.post.info, end='\n\n')

    translator_id = None  # default
    for name, id_ in player.post.translators.name_id.items():
        if 'субтитры' in name.casefold(): translator_id = id_; break

    stream = await player.get_stream(1, 1, translator_id)  # raise AJAXFail if invalid episode or translator
    video = stream.video
    print(await video.last_url[-1])  # best quality (.m3u8) (last source)
    # source - is not a finished link, await will return the link after the redirect
    print(await video[video.min].last_url[0].mp4, end='\n\n')  # worst quality (.mp4) (first source)

    subtitles = stream.subtitles
    print(subtitles.default.url)  # subtitles.ru.url or subtitles['Русский'].url


if __name__ == '__main__': asyncio.run(main())
```

# Bypass Blocking

## Custom HOST

```python
from hdrezka.url import Request

Request.HOST = 'https://hdrezka.club/'
```

> If the specified domain is protected by Cloudflare, successful response retrieval from the server cannot be guaranteed
> and may be inconsistent. See [this file](https://github.com/NIKDISSV-Forever/HDRezka/blob/main/mirrors.txt).

# Proxies

> pip install httpx[socks]
>
> tor

```python
import httpx

import hdrezka.api.http

hdrezka.api.http.DEFAULT_CLIENT = httpx.AsyncClient(
    headers={'User-Agent': 'Mozilla/5.0'},
    follow_redirects=True,
    proxy='socks5://localhost:9050'
)
```

## Log In (recommended for now)

Create an account on HDRezka.

If registration is temporarily disabled, try logging in via social media and resetting your password (so that you have
one at all).

Call `hdrezka.api.http.login_global` - this function will send a request to `hdrezka.api.http.Request.REDIRECT_URL`,
which will redirect to an active mirror. The function will then store the retrieved mirror globally in `Request.HOST`
and save the cookies in `hdrezka.api.http.DEFAULT_CLIENT`.

```python
import os

from hdrezka.api.http import login_global


async def main():
    await login_global(os.environ['LOGIN_NAME'], os.environ['LOGIN_PASSWORD'])
```

This method will also help if HDRezka considers your IP suspicious, suggests changing your VPN (proxy),
and returns a 403 error.
"""
__author__ = 'nikdissv'

from .api import *
from .post import *
from .stream import *
