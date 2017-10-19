# encoding:utf-8

import os
from flask import Blueprint, send_from_directory, current_app
from flask_restful import Api, Resource

bp = Blueprint('favicon', __name__)
api = Api(bp)


class Favicon(Resource):

    def __init__(self):
        super(Favicon, self).__init__()

    def get(self):
        app = current_app._get_current_object()
        return send_from_directory(app.root_path+'/static', 'favicon.ico')


api.add_resource(Favicon, '/favicon.ico', endpoint='favicon')
