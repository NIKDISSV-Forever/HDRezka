# CHANGELOG

## 3.0.2

- ### post.urls.kind.VideoURLs
  - `__init__(self, data: str | dict)` now raises `TypeError`
    if `data` isn't of type `str | dict` (see [this issue](https://github.com/NIKDISSV-Forever/HDRezka/issues/1))

## 3.0.1

- Now `__await__` method (need `await ...` expression) instead `ainit` method

## 3.0.0

- **Now a fully asynchronous package.**

- ### post.page.Page
    - Implements `__aiter__` and `__anext__` methods that list all the pages found.
    - Instead of `get_pages`, now only the `get_page` method

## 2.0.1

- Fixed bug with PIP

## 2.0.0

Backward incompatible changes have been made

- #### New submodules `urls.short`, `urls.kind`, `urls.kind.quality`, `urls.kind.subtitles`, `urls.kind.video`
- Optimizations
- `Ajax` renamed to `AJAX` (PEP-8)
- the `get_stream` method now contains the `video` attribute and the `subtitle` attribute

- ### urls
    - New function `urls_from_ajax_response -> URLs`
- ### urls.short
    - `short_url`, `long_url`
- ### urls.kind
    - class `Quality` now in `urls.king.quality` (also in \_\_init__)
- ### urls.kind.video
    - classes `VideoURL`, `VideoURLs`
- ### urls.kind.subtitle
    - classes `SubtitleURL`, `SubtitleURLs`

## 1.1.3

- bugfixes

## 1.1.2

- added pdoc documentation
- now Python **3.10** has become the minimum compatible version.
- removed all `from __future__ import annotations` statements
- used `match...case` statements
- optimization

- new submodule `api.http`
- `get_response` moved to `api.http` submodule

## 1.1.1

- fixed bug with importing `stream.Post`
- fixed `post.urls.url_short` function

## 1.1.0

- `post.urls.short_url` now even shorter

- ### errors
    - `EmptySearchPage` replaced with `EmptyPage`

- #### New submodule `post.page`

- ### post.page
    - new `Page` class that will parse any page rezka.ag on `InlineItem` (new data class)

- ### api.search
    - `Search` now inherited from `Page`

## 1.0.0

Backward incompatible changes have been made

- bs4 now selects lxml (if it available) once at startup
- new submodule `post`, `post.info`, `post.info.fields`
- class `post.Post` created
- class `post.info.PostInfo` created

- ### stream

    - hint typing fixes
    - `Player` now caching


- ##### `urls` submodule now is `post.urls`


- ### post.urls

    - `short_url` and `long_url` functions added (caching)
    - `short_url`, `long_url`, `Quality`, `URL` now in `__all__`


- ### post.info.fields

    - classes `Rating`, `Place`, `Release`, `AgeRating`, `Duration`, `Poster` created

## 0.0.2

- initial version