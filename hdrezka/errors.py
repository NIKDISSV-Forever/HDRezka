class HDRezkaError(Exception):
    """Any HDRezka exception"""
    __slots__ = ()


class UnknownContentType(HDRezkaError, TypeError):
    """Invalid content type"""
    __slots__ = ()


class AjaxFail(HDRezkaError):
    """No success response"""
    __slots__ = ()


class EmptySearchPage(HDRezkaError):
    """Empty search page"""
    __slots__ = ()
