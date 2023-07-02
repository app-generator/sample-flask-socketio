# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps import db
from flask_socketio import emit


class Sales(db.Model):

    __tablename__ = 'Sales'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64))
    amount = db.Column(db.String(64))
    status = db.Column(db.Enum('Completed', 'Not Completed'), default='Not Completed')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, key, value)

    def __repr__(self):
        return str(self.product)

    def save(self):
        db.session.add(self)
        db.session.commit()
