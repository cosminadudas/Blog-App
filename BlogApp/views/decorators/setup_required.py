from functools import wraps
from flask import redirect
from setup.database_config import DatabaseConfig


def setup_required(database_config: DatabaseConfig):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not database_config.is_configured:
                return redirect('/setup')
            return func(*args, **kwargs)
        return wrapper
    return decorator
