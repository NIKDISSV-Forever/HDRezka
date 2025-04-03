"""Error definitions"""


class HDRezkaError(Exception):
    """Any HDRezka exception"""
    __slots__ = ()


class UnknownContentType(HDRezkaError, TypeError):
    """Invalid content type"""
    __slots__ = ()


class AJAXFail(HDRezkaError):
    """No success response"""
    __slots__ = ()


class EmptyPage(HDRezkaError):
    """Asked page is empty (see Page class)"""
    __slots__ = ()
