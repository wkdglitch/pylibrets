"""Exception classes - Subclassing allows you to check for specific errors."""
import pylibrets


class LoginException(Exception):
    pass

class GetObjectException(Exception):
    pass

class SearchException(Exception):
    pass

class GetMetadataException(Exception):
    pass

class NoLoginException(Exception):
    pass

class RetsException(Exception):
    pass
