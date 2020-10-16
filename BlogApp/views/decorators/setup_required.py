from functools import wraps
from flask import redirect
from injector import inject
from setup.database_config import DatabaseConfig


def setup_required(funct):
    @wraps(funct)
    @inject
    def wrapper(database_config: DatabaseConfig, *args, **kwargs):
        if not database_config.is_configured:
            return redirect('/setup')
        return funct(*args, **kwargs)
    return wrapper
