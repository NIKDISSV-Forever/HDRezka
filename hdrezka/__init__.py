"""
# [HDRezka](https://rezka.ag/) site API.

# Install

`pip install HDRezka`

# Example

```python
from hdrezka import *

player = Search('Avatar')[1, 0].player
print(player.post.info)
print(player.get_stream().best_url)
```

# [GitHub](https://github.com/NIKDISSV-Forever/HDRezka)
"""
from .api import *
from .post import *
from .stream import *
