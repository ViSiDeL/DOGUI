""" session auth checks """

from functools import wraps

from flask import session, redirect, url_for, g
from api.engine_instance import design_engine


class SessionService:
    @staticmethod
    def get_current_user(session_id: str):
        return design_engine.current_users.get(session_id)

    @staticmethod
    def require_user():
        """ return the current user, or None if there isn't one """
        session_id = session.get('session_id')
        if not session_id:
            return None
        return SessionService.get_current_user(session_id)


def login_required(view):
    """ precheck decorator, ensure user is logged in """
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = SessionService.require_user()
        if not user:
            return redirect(url_for('user.login'))
        g.user = user
        return view(*args, **kwargs)
    return wrapped
