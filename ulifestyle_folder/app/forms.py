from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    email = StringField('註冊電郵地址*：', validators=[DataRequired(), Email()])
    username = StringField('會員名稱*：', validators=[DataRequired()])
    password = PasswordField('設定密碼*：', validators=[DataRequired()])
    password2 = PasswordField('再輸入密碼*：', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('註冊')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('電郵地址已被註冊')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('用戶名稱已被使用')


class LoginForm(FlaskForm):
    username = StringField('用戶名：', validators=[DataRequired()])
    password = PasswordField('密碼：', validators=[DataRequired()])
    remember_me = BooleanField('保持登入')
    submit = SubmitField('登入')
