from functools import wraps
from flask import redirect, session

def login_required(func):
    @wraps(func)
    def wrapped(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        return func(**kwargs)

    return wrapped
