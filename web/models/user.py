from flask_login import UserMixin
from web import db
from .dataset import Dataset


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    datasets = db.relationship('Dataset', backref='by', lazy=True)

    def __repr__(self):
        return f'User({self.email})'
