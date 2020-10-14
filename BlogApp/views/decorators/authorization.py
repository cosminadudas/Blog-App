from functools import wraps
from flask import redirect, session, abort

def admin_required(func):
    @wraps(func)
    def wrapped(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        if  session['username'] != 'admin':
            return abort(403)
        return func(**kwargs)

    return wrapped


def admin_or_owner_required(func):
    @wraps(func)
    def wrapped(**keyword):
        if 'username' not in session:
            return redirect('/login')
        if session["username"] != "admin" and int(keyword['user_id']) != session["id"]:
            return abort(403)
        return func(**keyword)

    return wrapped


def login_required(func):
    @wraps(func)
    def wrapped(**kwargs):
        if 'username' not in session:
            return redirect('/login')
        return func(**kwargs)

    return wrapped
