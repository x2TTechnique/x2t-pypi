from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)


def handler(log: bool = True, timing: bool = False):
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
            start_time = time.perf_counter() if timing else None
            try:
                result = func(*args, **kwargs)
                if timing:
                    elapsed_time = time.perf_counter() - start_time
                    logger.info(
                        f"function {func.__name__} with measured time is {elapsed_time}s.")
                return result
            except Exception as e:
                if log:
                    logger.error(f"An error occurred in {func.__name__}: {e}")
                return {"error": str(e), "status": "failed"}
        return wrapper
    return decorator
