# codeing:utf8

from flask import session, redirect, url_for, flash
from functools import wraps


class Auth:

    def login_required(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Please login first')
                return redirect(url_for('login.login'))
            username = session.get('username')
            return func(username, *args, **kwargs)
        return decorated

auth = Auth()



