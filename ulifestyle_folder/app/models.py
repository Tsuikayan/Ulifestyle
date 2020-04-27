from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
from app import app, db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(25), unique=True, nullable=False, index=True)
    gender = db.Column(db.String(1), nullable=True)
    phonenumber = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    educationlevel = db.Column(db.Integer, nullable=True)
    income = db.Column(db.Integer, nullable=True)
    usergroup = db.Column(db.String, nullable=False)
    password = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
