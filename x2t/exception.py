import logging

from functools import wraps


logger = logging.getLogger(__name__)


def handler(log: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log:
                    logger.error(f"An error occurred in {func.__name__}")
                return {"error": str(e), "status": "failed"}
        return wrapper
    return decorator
