# CHANGELOG

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