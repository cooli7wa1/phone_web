#coding:utf-8

from flask import Blueprint, redirect
from flask_restful import Api, Resource, url_for

bp = Blueprint('root', __name__)
api = Api(bp)


class Root(Resource):

    def __init__(self):
        super(Root, self).__init__()

    def get(self):
        return redirect(url_for('phones.phones'))

api.add_resource(Root, '/', endpoint='root')
