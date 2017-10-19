# codeing:utf8

from flask import Blueprint, render_template, make_response, flash, redirect, url_for, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from wtforms import Form, StringField, validators
from ..auth import auth
from ..model import mongo_phone, phones_db_fields

bp = Blueprint('phones', __name__, url_prefix='/phones')
api = Api(bp)

phones_out_fields = {
    'model': fields.String,
    'uri': fields.Url('phones.phone', absolute=True)
}

phone_out_fields = {
    'model': fields.String,
    'tag': fields.String,
    'date_creation': fields.String,
}


class PhonesForm(Form):
    model = StringField('model', [validators.Required()])
    tag = StringField('tag', [validators.Required()])


class PhoneForm(PhonesForm):
    method = StringField('method', [validators.Required()])


class PhoneListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        super(PhoneListAPI, self).__init__()

    def get(self, username):
        entries = [phone for phone in mongo_phone.db.phones.find({'vendor':username})]
        return make_response(render_template('show_entries.html', entries=marshal(entries, phones_out_fields)))

    def post(self, username):
        form = PhonesForm(request.form)
        if form.validate():
            phone = {}
            for k, v in form.data.items():
                if k in phones_db_fields:
                    phone[k] = v
            phone['vendor'] = username
            if mongo_phone.db.phones.find_one({'vendor':phone['vendor'], 'model':phone['model']}):
                flash('This model already exist')
                return redirect(url_for('phones.phones'))
            mongo_phone.db.phones.insert_one(phone)
            flash('Add success')
            return redirect(url_for('phones.phones'))
        for k, m in form.errors.items():
            flash('{key}: {message}'.format(key=k, message=m[0]))
        return redirect(url_for('phones.phones'))


class PhoneAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        super(PhoneAPI, self).__init__()

    def get(self, username, model):
        entry = mongo_phone.db.phones.find_one_or_404({'vendor': username, 'model': model})
        return make_response(render_template('show_entry.html', entry=marshal(entry, phone_out_fields)))

    def post(self, username, model):
        phone = mongo_phone.db.phones.find_one_or_404({'vendor': username, 'model': model})
        form = PhoneForm(request.form)
        if not form.validate():
            for k, m in form.errors.items():
                flash('{key}: {message}'.format(key=k, message=m[0]))
            return redirect(url_for('phones.phone', model=model))
        if form.method.data == 'DELETE':
            mongo_phone.db.phones.delete_one({'vendor': username, 'model': model})
            flash('Delete success')
            return redirect(url_for('phones.phones'))
        else:
            for k, v in form.data.items():
                if k in phones_db_fields:
                    phone[k] = v
            mongo_phone.db.phones.update_one({'vendor': username, 'model': model}, {"$set": phone})
            flash('Update success')
            return redirect(url_for('phones.phone', model=model))


api.add_resource(PhoneListAPI, '/', endpoint='phones')
api.add_resource(PhoneAPI, '/<string:model>', endpoint='phone')
