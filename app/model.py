#codeing:utf-8

from flask_pymongo import PyMongo

mongo_phone = PyMongo()
mongo_user = PyMongo()

phones_db_fields = ['vendor', 'model', 'tag']


def register_db(app):
    mongo_phone.init_app(app, config_prefix='MONGO_PHONE')
    mongo_user.init_app(app, config_prefix='MONGO_USER')