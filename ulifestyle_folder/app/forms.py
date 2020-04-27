from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, HiddenField,\
    SelectField, FileField
from wtforms.validators import ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    icon = FileField()
    username = StringField()
    email = StringField()
    gender = RadioField()
    phonenumber = StringField()
    year = SelectField()
    month = SelectField()
    day = SelectField()
    educationlevel = SelectField()
    income = SelectField()
    usergroup = HiddenField(default="user")
    password = PasswordField()
    submit = SubmitField()

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('電郵地址已被註冊')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('用戶名稱已被使用')

    def validate_password(self, password):
        user = User.query.filter_by(password=password.data).first()
        if user is not None:
            raise ValidationError('密碼已被使用')


class LoginForm(FlaskForm):
    email = StringField()
    password = PasswordField()
    submit = SubmitField()
