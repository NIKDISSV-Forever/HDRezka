# CHANGELOG

## 3.2.3
- New `url` module and `url.Request` class for changing the HDRezka host url
- `stream.player.Player` now connects the url to the default host if only the url path is passed.
- Used Poetry to replace setup.py and requirements.txt.

## 3.2.2

- ### post.urls
    - Added supports of added support for quality in the format `2K`, `4K`, ...
  
## 3.2.1

- ### post.kind.video
    - if **await** `VideoURL` instance, it's follow url redirects and return correct download url.
      _See [issue 5](https://github.com/NIKDISSV-Forever/HDRezka/issues/5)_.
    - Now `VideoURL.mp4` is `property`.
- ### api.http
    - passed `get_response(..., **kwargs)` have more weight than `DEFAULT_REQUEST_KWARGS`.

## 3.2.0

- **Documentation and doc-strings improved.**
- Type-checking improved (_None-safety_ checks)
- #### New submodule `api.types`.

- ### api
    - #### http
        - Added `RequestKwargs(TypedDict)` type-hint.
        - **`DEFAULT_CLINET_KWARGS` replaced with just `DEFAULT_CLIENT`.**
    - #### types
        - Added `APIResponse(TypedDict)` type-hint.
- ### post.fields
    - Added default empty strings.
- ### post.info.PostInfo
    - if `age_rating` rating not found, `AgeRating.age` sets **-1**.
- ### post.urls.king.video.VideoURLs
    - `__getitem__(self, item: str | SupportsInt | Iterable | slice)` updated (see documentations).
- ### stream.player
    - **fixed [issue 1](https://github.com/NIKDISSV-Forever/HDRezka/issues/1)**.
    - fixed [issue 4](https://github.com/NIKDISSV-Forever/HDRezka/issues/4).
    - `PlayerType` everyplace replaced with `PlayerMovie | PlayerSeries`.

## 3.1.2

- ### post.urls
    - Fixed [issue 2](https://github.com/NIKDISSV-Forever/HDRezka/issues/2). _rezka.ag stopped redirecting from links of
      this type:"https://rezka.ag/1-1.html". now returns a 500
      error._

## 3.1.1

- Documentation improved.

## 3.1.0

- ### requirements.txt
    - `bs4` replaced with `beautifulsoup4`.
    - `lxml` now installs on versions < 3.13 (instead of < 3.12).
- ### api.http
    - Added `DEFAULT_REQUEST_KWARGS`.

## 3.0.3

- ### stream.player
    - #### Player Caching
        - fixed `RuntimeError: dictionary changed size during iteration`.
        - removed `sys.getsizeof` (for compatibility with PyPy), used `len` instead.

## 3.0.2

- ### post.urls.kind.VideoURLs
    - `__init__(self, data: str | dict)` now raises `TypeError`
      if `data` isn't of type `str | dict` (see [this issue](https://github.com/NIKDISSV-Forever/HDRezka/issues/1)).

## 3.0.1

- Now `__await__` method (need `await ...` expression) instead `ainit` method.

## 3.0.0

- **Now a fully asynchronous package.**

- ### post.page.Page
    - Implements `__aiter__` and `__anext__` methods that list all the pages found.
    - Instead of `get_pages`, now only the `get_page` method.

## 2.0.1

- Fixed bug with PIP.

## 2.0.0

Backward incompatible changes have been made.

- #### New submodules `urls.short`, `urls.kind`, `urls.kind.quality`, `urls.kind.subtitles`, `urls.kind.video`.
- Optimizations.
- `Ajax` renamed to `AJAX` (PEP-8).
- the `get_stream` method now contains the `video` attribute and the `subtitle` attribute.

- ### urls
    - New function `urls_from_ajax_response -> URLs`.
- ### urls.short
    - `short_url`, `long_url`.
- ### urls.kind
    - class `Quality` now in `urls.king.quality` (also in \_\_init__).
- ### urls.kind.video
    - classes `VideoURL`, `VideoURLs`.
- ### urls.kind.subtitle
    - classes `SubtitleURL`, `SubtitleURLs`.

## 1.1.3

- internal bugfixes.

## 1.1.2

- added pdoc documentation.
- now Python **3.10** has become the minimum compatible version.
- removed all `from __future__ import annotations` statements.
- used `match...case` statements.
- optimization.

- new submodule `api.http`.
- `get_response` moved to `api.http` submodule.

## 1.1.1

- fixed bug with importing `stream.Post`.
- fixed `post.urls.url_short` function.

## 1.1.0

- `post.urls.short_url` now even shorter.

- ### errors
    - `EmptySearchPage` replaced with `EmptyPage`.

- #### New submodule `post.page`

- ### post.page
    - new `Page` class that will parse any page rezka.ag on `InlineItem` (new data class).

- ### api.search
    - `Search` now inherited from `Page`.

## 1.0.0

**Backward incompatible changes have been made.**

- bs4 now selects lxml (if it available) once at startup.
- new submodule `post`, `post.info`, `post.info.fields`.
- class `post.Post` created.
- class `post.info.PostInfo` created.

- ##### `urls` submodule now is `post.urls`.

- ### stream
    - type-hinting fixes.
    - `Player` now caching.

- ### post.urls
    - `short_url` and `long_url` functions added (caching).
    - `short_url`, `long_url`, `Quality`, `URL` now in `__all__`.

- ### post.info.fields
    - classes `Rating`, `Place`, `Release`, `AgeRating`, `Duration`, `Poster` created.

## 0.0.2

- initial version.