"""
[HDRezka](https://rezka.ag/) site API.

# Install

> `pip install HDRezka`

# Example

```python
from hdrezka import *

player = Search('Avatar')[1, 0].player
print(player.post.info)
print(player.get_stream().best_url)
```
"""
from .api import *
from .post import *
from .stream import *
