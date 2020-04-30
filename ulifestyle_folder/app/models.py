from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    educationLevel = db.Column(db.String(30), nullable=True)
    income = db.Column(db.String(30), nullable=True)
    usergroup = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(30), nullable=False)
    getinfo = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
