# encoding:utf-8

from flask import Blueprint, current_app, make_response, send_from_directory
from flask_restful import Api, Resource
from ..auth import auth

bp = Blueprint('download', __name__, url_prefix='/download')
api = Api(bp)


class DownloadAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        super(DownloadAPI, self).__init__()

    def get(self, filename):
        app = current_app._get_current_object()
        return send_from_directory(directory=app.config['DOWNLOAD_FOLD'],
                                   filename=filename,
                                   as_attachment=True)


api.add_resource(DownloadAPI, '/<string:filename>', endpoint='download')
