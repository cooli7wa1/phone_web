# encoding:utf-8

import os
from flask import Blueprint, current_app, request, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from ..auth import auth

bp = Blueprint('upload', __name__, url_prefix='/upload')
api = Api(bp)

api_reqparse = reqparse.RequestParser()
api_reqparse.add_argument('file', type=FileStorage, required=True,
                          help='No file provided',
                          location='files')


class UploadAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = api_reqparse
        super(UploadAPI, self).__init__()

    def get(self):
        return make_response('''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>   
        ''', 200)

    def post(self):
        file = self.reqparse.parse_args()['file']
        if not file:
            return make_response(jsonify({'message': 'request a file'}), 400)
        filename = secure_filename(file.filename)
        app = current_app._get_current_object()
        upload_fold = app.config['UPLOAD_FOLD']
        file.save(os.path.join(upload_fold, filename))
        return make_response(jsonify({'result': 'upload ok'}), 201)


api.add_resource(UploadAPI, '/', endpoint='upload')
