"""Translators definition module"""
__all__ = ('Translators',)


class Translators:
    """Translators info"""
    __slots__ = ('names', 'ids', 'name_id', 'id_name')

    def __init__(self, name_id: dict[str, int]):
        self.names = *name_id,
        self.ids = *name_id.values(),
        self.id_name: dict[int, str] = {v: k for k, v in name_id.items()}
        self.name_id = name_id

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.name_id!r})'
