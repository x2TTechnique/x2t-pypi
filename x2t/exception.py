from functools import wraps
import logging

logger = logging.getLogger(__name__)


def handler(log: bool = True):
    """
    A decorator to handle exceptions and log errors if they occur.

    Args:
        log (bool, optional): If True, the error will be logged. 
                              Defaults to True.

    Returns:
        Callable: A decorator that wraps the original function, 
                  catches exceptions, and returns a dictionary 
                  with error details if an exception occurs.

    Example:
        >>> @handler(log=True)
        ... def divide(a, b):
        ...     return a / b
        >>> divide(4, 2)
        2.0
        >>> divide(4, 0)
        {'error': 'division by zero', 'status': 'failed'}
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log:
                    logger.error(f"An error occurred in {func.__name__}: {e}")
                return {"error": str(e), "status": "failed"}
        return wrapper
    return decorator
