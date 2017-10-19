# encoding:utf-8

import os
from flask import Blueprint, redirect, render_template, session, flash, make_response, request
from flask_restful import Api, Resource, url_for
from wtforms import Form, StringField, PasswordField, validators
from ..model import mongo_user

bp = Blueprint('login', __name__)
api = Api(bp)


class UserForm(Form):
    username = StringField('vendor', [validators.Required()])
    password = PasswordField('model', [validators.Required()])


class Login(Resource):

    def __init__(self):
        super(Login, self).__init__()

    def post(self):
        form = UserForm(request.form)
        if not form.validate():
            for k, m in form.errors.items():
                flash('{key}: {message}'.format(key=k, message=m[0]))
            return make_response(render_template('login.html'))
        username = form.data['username']
        password = form.data['password']
        doc = mongo_user.db.user.find_one({'username':username})
        if not doc:
            error = 'No such username'
            return make_response(render_template('login.html', error=error))
        if doc['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('phones.phones'))
        else:
            error = 'Username or Password error'
            return make_response(render_template('login.html', error=error))

    def get(self):
        return make_response(render_template('login.html', error=None))


class Logout(Resource):

    def __init__(self):
        super(Logout, self).__init__()

    def get(self):
        session.pop('logged_in', None)
        session.pop('username', None)
        flash('You were logged out')
        return redirect(url_for('login.login'))



api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
