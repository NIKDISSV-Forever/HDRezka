"""Primitive cache storage"""
__all__ = ('CACHE',)


class _CacheStorage:
    __slots__ = ('max_size', '__storage', 'get')

    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.__storage: dict = {}
        self.get = self.__storage.get

    def set(self, key, value):
        """Store some cache"""
        self.__storage[key] = value
        for k in (*self.__storage.keys(),):
            if len(self.__storage) <= self.max_size:
                break
            del self.__storage[k]


CACHE = _CacheStorage()
