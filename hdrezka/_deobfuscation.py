import re
from binascii import a2b_base64

__all__ = ('clear_trash',)

_sub_trash = re.compile(
    '#h|//_//|'
    '(?:I[01UV]|[JQ][EF]|X[kl])(?:[A4][=hjk]|[B5][Ae])|'
    '(?:I[Sy]|[JQ]C|Xi)(?:[EMQ][=hjk]|[FNR][Ae])'
).sub


def clear_trash(trash_string: str) -> str:
    return a2b_base64(_sub_trash('', trash_string).encode('ASCII') + b'==').decode('ASCII')
