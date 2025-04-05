# CHANGELOG

## 4.0.1

- Bug fixed: `translator: str` replaced with `translators: tuple[str, ...]` in `post.Post.info`.
  This is not a one translator but enumeration. It is recommended to use `post.Post.translators` instead.

## 4.0.0

**Warning:** This release contains backward incompatible changes. Please carefully review the list of changes before
updating.

- ### Global Changes
    - The internal logic for parsing content information has been reorganized to improve stability and support future
      changes.
    - Added a new type `post.info.fields.Hyperlink` (`NamedTuple` with fields `name: str`, `url: str`), which is now
      used in many `PostInfo` fields instead of simple strings or tuples of strings, providing both a name and a link.
- ### New Features
    - **Franchises:**
        - Added functionality to retrieve information about franchises (related content parts);
          The field `post.Post.oter_parts_urls` used for these purposes earlier is removed.
        - Added the `franchises` field (type `FranchiseInfo`) to the `Post` class, providing access to franchise data (
          previous, next parts, list of all parts, franchise poster).
        - Added related types `FranchiseInfo` and `FranchiseEntry` in `post.info.franchises`.
    - **`post.info.Person`:**
        - New `Person` type, reflecting information about an actor (name, photo, career, date and place of birth,
          height).
    - **Trailers:**
        - Added method
          `PlayerBase.get_trailer_iframe(self) -> str`
          and `api.AJAX.get_trailer_video(cls, id: SupportsInt | str)`
    - **`PostInfo`:**
        - Added `duration` field (type `int`) – total duration in seconds, obtained from page metadata.
        - The `persons` field is now a tuple of `Person` objects.
- ### Backward Incompatible Changes
    - **`api.http`:**
        - The `login_global` function now accepts `email` instead of `name` as the first argument for login.
    - **`post.info.fields`:**
        - Removed the `Duration` type. Use `PostInfo.duration` (seconds) or `PostInfo.duration_m` (minutes).
        - Removed the `Place` type. Use the new `Rank` type.
        - Added the `Rank` type (`NamedTuple` with fields `name: Hyperlink`, `rank: int`), replacing `Place` for
          representing positions in lists/rankings.
        - `Rating` type:
            - The `service` field is now of type `Hyperlink` (contains the name and URL of the rating service) instead
              of `str`.
            - The `url` field has been removed (the information is now contained in `service.url`).
    - **`post.info.PostInfo`:**
        - The `rating` field has been renamed to `ratings`. The value type `dict[str, Rating]` remains the same, but the
          internal structure of `Rating` has changed (see above).
        - The `places` field has been renamed to `rankings` and now returns a tuple of `Rank` objects (
          `tuple[Rank]`).
        - The `duration` field (previously of type `Duration`) has been renamed to `duration_m` and now returns an
          `int` (duration in minutes, as displayed in the table on the site).
        - The `duration_s` field has been removed. Use the new `duration` field (total duration in seconds).
        - The `from_` field has been renamed to `collections` and now returns a tuple of `Hyperlink` objects (
          `tuple[Hyperlink]`).
        - The `characters` field has been renamed to `persons` and now returns a tuple of `Hyperlink` objects (
          `tuple[Hyperlink]`).
        - The `country` field now returns a tuple of `Hyperlink` objects (`tuple[Hyperlink, ...]`).
        - The `genre` field now returns a tuple of `Hyperlink` objects (`tuple[Hyperlink, ...]`).
        - Removed the `fields` field.
    - **`post.Post`:**
        - Removed the `other_parts_urls` field. Use the new `franchises` field to get information about other parts.
    - **`api.AJAX`:**
        - All arguments `id` are renamed` id_`.
    - Some classes and functions that are no longer used are removed.
- ### Improvements
    - **`post.urls.kind.video.VideoURL`**:
        - Asynchronous retrieval of video URL (`await video_url`) has become more reliable: it now returns the original
          URL if the server did not provide a redirect URL.
    - Type and bug fixes.
    - Minor decomposition of code.
    - Other minor improvements and optimizations.

## 3.3.1

- Removed the `follow_redirect=True` argument from `api.http.DEFAULT_CLIENT`;  
  instead of following redirects automatically, the URL is now extracted from the `Location` header where necessary.
- ### post.url.kind.subtitle.SubtitleURLs
    - Fixed a bug in `__init__` that caused incorrect handling when no subtitles were available.
    - Added the method `get(self, item: str) -> SubtitleURL | None`.
    - The `__getitem__(self, item: str)` method now raises a `KeyError` if `item` is not a valid code or name  
      (mirroring dictionary behavior). Use `get` to safely return `None`.
- Minor documentation improvements.

## 3.3.0

- ### api.http
    - Added the `login_global(name: str, password: str)` function.
- ### url
    - Added `Request.REDIRECT_URL`, required for `api.http.login_global`.
    - Updated `Request.HOST`.
- ### post.info.PostInfo
    - Added the `duration_s` attribute – duration in seconds.
    - Added the `updated_time` attribute – last modification date (int).
    - Fixed retrieval of the `poster.full` link.
    - Added the 'hdrezka' key to the `rating` dictionary, containing the rating directly from the site.
    - The keys in the `rating` dictionary are now guaranteed to be in lowercase (e.g., `imdb` instead of `IMDb`).
- ### post.fields
    - Added the `Rating.url` field – a link to the rating page (IMDB, KP, WA, etc.).
- ### post.urls.kind
    - Simplified parsing of video and subtitle links, now without regex.
- ### post.urls.kind.video
    - Each video link (m3u8) in `VideoURLs` is now represented as a tuple with available sources,  
      in case one of them is unavailable.
- Replaced all `dataclasses` with `NamedTuple`.
- Minor documentation improvements.
- Minor optimizations and enhancements.

## 3.2.3

- New `url` module and `url.Request` class for changing the HDRezka host url.
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