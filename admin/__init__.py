from functools import wraps
from flask import session, abort


def owner_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin = session.get('admin')
        if not admin or admin.get('role') != 'owner':
            abort(403)
        return func(*args, **kwargs)
    return wrapper
