# HDRezka

#### HDRezka ([rezka.ag](https://rezka.ag)) Python API

```python
from hdrezka import *

player = Search('Avatar')[1, 0].player
print(player.post.info)
print(player.get_stream().best_url)
```

# hdrezka library

<h2>Errors</h2>
<details>
    <summary>hdrezka.errors</summary>

```python
class HDRezkaError(Exception):
    """Any HDRezka exception"""


class UnknownContentType(HDRezkaError, TypeError):
    """Invalid content type"""


class AjaxFail(HDRezkaError):
    """No success response"""


class EmptyPage(HDRezkaError):
    """Asked page is empty (see Page class)"""

```

</details>

<h2>Translators info</h2>
<details>
    <summary>hdrezka.translators</summary>

```python
class Translators:
    __slots__ = ('names', 'ids', 'name_id', 'id_name')
    names: tuple[str]
    ids: tuple[int]
    name_id: dict[str, int]
    id_name: dict[int, str]

    def __init__(self, name_id: dict[str, int]):
        ...
```

</details>

<h2>Stream classes</h2>
<details>
    <summary>hdrezka.stream.player</summary>

```python
PlayerType = PlayerBase | PlayerMovie | PlayerSeries


class PlayerBase:
    def __init__(self, url_or_cast: Self | str):
        ...


class PlayerMovie(PlayerBase):
    def get_stream(self, translator_id: SupportsInt = None) -> URLs:
        ...


class PlayerSeries(PlayerBase):
    def get_episodes(self, translator_id: SupportsInt = None) -> defaultdict[int, tuple[int]]:
        ...

    def get_stream(self, season: int, episode: int, translator_id: SupportsInt = None) -> URLs:
        ...


def player(url_or_path: str) -> PlayerType:
    """
    Returns either Player Series if series, or PlayerMovie if movie, otherwise raises UnknownContentType
    """
    ...


Player = player
```

</details>

<h2>Post classes</h2>
<details>
    <summary>hdrezka.post</summary>

```python
class Post:
    """Stores information about the post"""
    __slots__ = ('url', 'translator_id', 'id', 'name', 'type', 'info', 'translators', 'other_parts_urls')

    def __init__(self, url: str):
        ...
```

</details>

<details>
    <summary>hdrezka.post.page</summary>

```python
PageNumber = Iterable[int] | slice | int


@dataclass(frozen=True)
class InlineItem:
    """Content Inline Item view"""
    url: str
    name: str
    info: str
    poster: str  # image url

    @property
    def player(self) -> PlayerType:
        return Player(self.url)


class Page:
    """Ajax class for HDRezka search"""
    page: str = property(..., ...)

    def __init__(self, url: str = 'https://rezka.ag/'):
        ...

    def __iter__(self) -> Iterator[InlineItem]:
        """
        Returns the generator of all found articles
        """
        ...

    def page_iter(self, page: PageNumber = 1) -> Iterator[InlineItem] | None:
        ...

    def get_pages(self, page: PageNumber = 1) -> tuple[InlineItem]:
        ...

    def __getitem__(self, item: PageNumber | Sequence[PageNumber | SupportsIndex | slice]
                    ) -> tuple[InlineItem] | InlineItem:
        ...
```

</details>

<details>
    <summary>hdrezka.post.urls</summary>

```python
def short_url(url: str) -> str:
    """
    >>> short_url('https://rezka.ag/.../.../90909-any-name.html/')
    '.../.../90909-90909'
    >>> short_url('https://rezka.ag/.../.../any-name.html')
    '.../.../any-name'
    """
    ...


def long_url(url: str) -> str:
    """
    >>> long_url('rezka.ag/.../.../99999-any-name')
    'https://rezka.ag/.../.../99999-99999.html'
    >>> long_url('.../.../99999-99999')
    'https://rezka.ag/.../.../99999-99999.html'
    """
    ...


class Quality(str):
    addon: str  # can contain 'ultra'

    def __int__(self):
        """
        returns pixels height
        """
        ...

    def __lt__(self, other):
        ...


class URL(str):
    mp4: str


class URLs:
    best_url: URL

    def __init__(self, data: str | dict):
        ...

    def __getitem__(self, item: (SupportsInt | str) | (slice | Iterable)):
        ...
```

</details>

<h2>Post Info classes</h2>
<details>
    <summary>hdrezka.post.info</summary>

```python

class PostInfo:
    FILL_FIELDS = ('rating', 'places', 'slogan', 'release', 'country', 'director', 'genre',
                   'quality', 'translator', 'age_rating', 'duration', 'from_', 'characters')
    __slots__ = FILL_FIELDS + ('fields', 'title', 'orig_title', 'poster', 'description')
    translator: str

    def __init__(self, soup: BeautifulSoup):
        ...
```

</details>

<details>
    <summary>hdrezka.post.fields</summary>

```python
@dataclass(frozen=True)
class Rating:
    service: str
    rating: int | float
    votes: int


@dataclass(frozen=True)
class Place:
    name: str
    place: int


@dataclass(frozen=True)
class Release:
    year: int
    day: str


@dataclass(frozen=True)
class AgeRating:
    age: int
    description: str


@dataclass(frozen=True)
class Duration:
    number: int
    units: str


class Poster(NamedTuple):
    full: str
    preview: str
```

</details>

<h2>API classes</h2>
<details>
    <summary>hdrezka.api.ajax</summary>

```python
class Ajax:
    """HDRezka Ajax class"""

    @classmethod
    def get_cdn_series(cls, data: dict[str]):
        ...

    @classmethod
    def get_episodes(cls, id: int | str, translator_id: int | str):
        ...

    @classmethod
    def get_stream(cls, id: int | str, translator_id: int | str, season: int | str, episode: int | str):
        ...

    @classmethod
    def get_movie(cls, id: int | str, translator_id: int | str):
        ...
```

</details>

<details>
    <summary>hdrezka.api.search</summary>

```python
class Search(Page):
    """Ajax class for HDRezka search"""
    query: str = property(..., ...)

    def __init__(self, query: str = ''):
        ...

    def __iter__(self) -> Iterator[InlineItem]:
        """
        Returns the generator of all found articles
        """
        ...
```

</details>