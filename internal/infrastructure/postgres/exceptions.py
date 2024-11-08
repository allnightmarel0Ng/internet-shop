class NoResultFound(Exception):
    """Raised when a query returns no result."""
    pass


class MultipleResultsFound(Exception):
    """Raised when a query returns more than one result."""
    pass
