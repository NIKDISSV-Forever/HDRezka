# CHANGELOG

## 1.1.1

- Fixed bug with importing `Post` <sub>stream</sub>
- Fixed `url_short` function <sub>post.urls</sub>

## 1.1.0

- ### errors
    - `EmptySearchPage` replaced with `EmptyPage`

- #### New submodule `post.page`

- ### post.page
    - new `Page` class that will parse any page rezka.ag on `InlineItem` (new data class)

- ### api.search
    - `Search` now inherited from `Page`

- ### post.urls
    - `short_url` now even shorter

## 1.0.0

Backward incompatible changes have been made

- bs4 now selects lxml (if it available) once at startup

- ### stream

    - Hint typing fixes
    - `Player` now caching

- #### New submodule `post`, `post.info`, `post.info.fields`

- ##### `urls` submodule now is `post.urls`

- ### post
    - class `Post` created

- ### post.urls

    - `short_url` and `long_url` functions added (caching)
    - `short_url`, `long_url`, `Quality`, `URL` now in `__all__`

- ### post.info

    - class `PostInfo` created

- ### post.info.fields

    - classes `Rating`, `Place`, `Release`, `AgeRating`, `Duration`, `Poster` created

## 0.0.2

- Initial version