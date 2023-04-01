# HDRezka

#### HDRezka ([rezka.ag](https://rezka.ag)) Python API

```python
from hdrezka import *

player = Search('Avatar')[1, 0].player
print(player.get_stream().best_url)
```

# hdrezka.api

## hdrezka.api.ajax

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

## hdrezka.api.search

```python
PageNumber = Iterable[int] | slice | int


@dataclass(frozen=True, slots=True)
class SearchResult:
    url: str
    name: str
    info: str
    poster: str  # image url

    @property
    def player(self) -> PlayerType:
        return Player(self.url)


class Search:
    """Ajax class for HDRezka search"""
    query = property(..., ...)

    def __init__(self, query: str = ''):
        ...

    def __iter__(self) -> Iterator[SearchResult]:
        """
        Returns the generator of all found articles
        """
        ...

    def page_iter(self, page: PageNumber = 1) -> Iterator[SearchResult] | None:
        ...

    def page(self, page: PageNumber = 1) -> tuple[SearchResult]:
        ...

    def __getitem__(self, item: PageNumber | Sequence[PageNumber, SupportsIndex | slice]
                    ) -> tuple[SearchResult] | SearchResult:
        ...
```

# hdrezka.stream

## hdrezka.stream.urls

```python
class Quality(str):
    addon: str  # = 'ultra' if in quality

    def __int__(self):
        """Return size in pixels"""
        ...

    def __lt__(self, other):
        ...


class URL(str):
    mp4: str


class URLs:
    def __init__(self, data: str | dict):
        ...

    def __getitem__(self, item: (SupportsInt | str) | (slice | Iterable)):
        ...

    @property
    def best_url(self) -> URL:
        ...
```

## hdrezka.stream.player

```python
class PlayerBase:
    def __init__(self, url_or_cast: Self | Any):
        ...


class PlayerSeries(PlayerBase):
    def get_episodes(self, translator_id: SupportsInt = 0) -> dict[int, tuple[int]]:
        ...

    def get_stream(self, season: int, episode: int, translator_id: SupportsInt = 0) -> URLs:
        ...


class PlayerMovie(PlayerBase):
    def get_stream(self, translator_id: int | str = 0) -> URLs:
        ...


PlayerType = TypeVar('PlayerType', PlayerBase, PlayerMovie, PlayerSeries)


def Player(url_or_path: str) -> PlayerType:
    ...
```
