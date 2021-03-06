from datetime import datetime
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
from app import app, db, login


class user(UserMixin, db.Model):
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
        return '<user {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return user.query.get(id)


@login.user_loader
def load_user(id):
    return user.query.get(int(id))


class author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    usergroup = db.Column(db.String(30), default='author', nullable=False)

    def __repr__(self):
        return '<author {}>'.format(self.username)


def author_query():
    return author.query


class hkpost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    body2 = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)
    theme = db.Column(db.String(10), nullable=True)
    tag = db.Column(db.String(10), nullable=True)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<hkpost {}>'.format(self.title)


class foodpost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    body2 = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)
    theme = db.Column(db.String(10), nullable=True)
    tag = db.Column(db.String(10), nullable=True)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<foodpost {}>'.format(self.title)


class travelpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    body2 = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)
    theme = db.Column(db.String(10), nullable=True)
    tag = db.Column(db.String(10), nullable=True)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<travelpost {}>'.format(self.title)


class beautypost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    body2 = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)
    theme = db.Column(db.String(10), nullable=True)
    tag = db.Column(db.String(10), nullable=True)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<beautypost {}>'.format(self.title)


class hkvideopost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    video = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)

    def __repr__(self):
        return '<hkvideopost {}>'.format(self.title)


class foodvideopost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    video = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)

    def __repr__(self):
        return '<foodvideopost {}>'.format(self.title)


class travelvideopost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    video = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)

    def __repr__(self):
        return '<travelvideopost {}>'.format(self.title)


class beautyvideopost(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.ForeignKey(author.username), nullable=True)
    body1 = db.Column(db.String(100), nullable=True)
    video = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=True)

    def __repr__(self):
        return '<beautyvideopost {}>'.format(self.title)


class tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<tag {}>'.format(self.tag)


class carousel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    img = db.Column(db.String(200), index=True)
    link = db.Column(db.String(200), index=True)

    def _repr_(self):
        return '< Carousel{}>'.format(self.title)


class mediaapp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mediatype = db.Column(db.String(20))
    hyperlink = db.Column(db.String)
    side = db.Column(db.String(10), nullable=True)

    def _repr_(self):
        return '< mediaapp{}>'.format(self.mediatype)


class contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contype = db.Column(db.String(10))
    conway = db.Column(db.String(30))
    phoneno = db.Column(db.Integer)
    email = db.Column(db.String)
    address = db.Column(db.String)

    def _repr_(self):
        return '< contact{}>'.format(self.contype)


class hkmenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<hkmenu {}>'.format(self.name)


class travelmenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<travelmenu {}>'.format(self.name)


class foodmenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<foodmenu {}>'.format(self.name)


class beautymenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<beautymenu {}>'.format(self.name)