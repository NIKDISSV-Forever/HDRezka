"""HDRezka deobfuscation process"""
__all__ = ('clear_trash',)

import re
from binascii import a2b_base64

_sub_trash = re.compile(
    '^#h|//_//|'
    '(?:I[01UV]|[JQ][EF]|X[kl])(?:[A4][=hjk]|[B5][Ae])|'
    '(?:I[Sy]|[JQ]C|Xi)(?:[EMQ][=hjk]|[FNR][Ae])'
).sub


def clear_trash(trash_string: str) -> str:
    """removes base64 trash from string"""
    return a2b_base64(_sub_trash('', trash_string).encode('ASCII') + b'==').decode('ASCII')
