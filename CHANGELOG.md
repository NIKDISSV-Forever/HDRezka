# CHANGELOG

## 0.0.2

- Initial version

## 1.0.0

Backward incompatible changes have been made

- ReadMe updated

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
