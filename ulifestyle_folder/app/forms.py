from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields import html5
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import user
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import user, author_query


class RegistrationForm(FlaskForm):
    email = html5.EmailField('註冊電郵地址*：', validators=[DataRequired(), Email()])
    username = StringField('會員名稱*：', validators=[DataRequired()])
    gender = RadioField('性別*：', choices=[("Male", "男"), ("Female", "女")], default="Male", coerce=str)
    phoneNumber = StringField('聯絡電話：')
    year = SelectField(choices=[(0, '年份'),
                                (2020, '2020'),
                                (2019, '2019'),
                                (2018, '2018'),
                                (2017, '2017'),
                                (2016, '2016'),
                                (2015, '2015'),
                                (2014, '2014'),
                                (2013, '2013'),
                                (2012, '2012'),
                                (2011, '2011'),
                                (2010, '2010'),
                                (2009, '2009'),
                                (2008, '2008'),
                                (2007, '2007'),
                                (2006, '2006'),
                                (2005, '2005'),
                                (2004, '2004'),
                                (2003, '2003'),
                                (2002, '2002'),
                                (2001, '2001'),
                                (2000, '2000'),
                                (1999, '1999'),
                                (1998, '1998'),
                                (1997, '1997'),
                                (1996, '1996'),
                                (1995, '1995'),
                                (1994, '1994'),
                                (1993, '1993'),
                                (1992, '1992'),
                                (1991, '1991'),
                                (1990, '1990'),
                                (1989, '1989'),
                                (1988, '1988'),
                                (1987, '1987'),
                                (1986, '1986'),
                                (1985, '1985'),
                                (1984, '1984'),
                                (1983, '1983'),
                                (1982, '1982'),
                                (1981, '1981'),
                                (1980, '1980'),
                                (1979, '1979'),
                                (1978, '1978'),
                                (1977, '1977'),
                                (1976, '1976'),
                                (1975, '1975'),
                                (1974, '1974'),
                                (1973, '1973'),
                                (1972, '1972'),
                                (1971, '1971'),
                                (1970, '1970'),
                                (1969, '1969'),
                                (1968, '1968'),
                                (1967, '1967'),
                                (1966, '1966'),
                                (1965, '1965'),
                                (1964, '1964'),
                                (1963, '1963'),
                                (1962, '1962'),
                                (1961, '1961'),
                                (1960, '1960'),
                                (1959, '1959'),
                                (1958, '1958'),
                                (1957, '1957'),
                                (1956, '1956'),
                                (1955, '1955'),
                                (1954, '1954'),
                                (1953, '1953'),
                                (1952, '1952'),
                                (1951, '1951'),
                                (1950, '1950'),
                                (1949, '1949'),
                                (1948, '1948'),
                                (1947, '1947'),
                                (1946, '1946'),
                                (1945, '1945'),
                                (1944, '1944'),
                                (1943, '1943'),
                                (1942, '1942'),
                                (1941, '1941'),
                                (1940, '1940'),
                                (1939, '1939'),
                                (1938, '1938'),
                                (1937, '1937'),
                                (1936, '1936'),
                                (1935, '1935'),
                                (1934, '1934'),
                                (1933, '1933'),
                                (1932, '1932'),
                                (1931, '1931'),
                                (1930, '1930'),
                                (1929, '1929'),
                                (1928, '1928'),
                                (1927, '1927'),
                                (1926, '1926'),
                                (1925, '1925'),
                                (1924, '1924'),
                                (1923, '1923'),
                                (1922, '1922'),
                                (1921, '1921'),
                                (1920, '1920')],
                       coerce=int)
    month = SelectField(choices=[(0, '月份'),
                                 (1, '1'),
                                 (2, '2'),
                                 (3, '3'),
                                 (4, '4'),
                                 (5, '5'),
                                 (6, '6'),
                                 (7, '7'),
                                 (8, '8'),
                                 (9, '9'),
                                 (10, '10'),
                                 (11, '11'),
                                 (12, '12')],
                        coerce=int, default='', validators=[DataRequired()])
    day = SelectField(choices=[(0, '日期'),
                               (1, '1'),
                               (2, '2'),
                               (3, '3'),
                               (4, '4'),
                               (5, '5'),
                               (6, '6'),
                               (7, '7'),
                               (8, '8'),
                               (9, '9'),
                               (10, '10'),
                               (11, '11'),
                               (12, '12'),
                               (13, '13'),
                               (14, '14'),
                               (15, '15'),
                               (16, '16'),
                               (17, '17'),
                               (18, '18'),
                               (19, '19'),
                               (20, '20'),
                               (21, '21'),
                               (22, '22'),
                               (23, '23'),
                               (24, '24'),
                               (25, '25'),
                               (26, '26'),
                               (27, '27'),
                               (28, '28'),
                               (29, '29'),
                               (30, '30'),
                               (31, '31')],
                      coerce=int, default='', validators=[DataRequired()])
    educationLevel = SelectField('教育程度：',
                                 choices=[('', '請選擇'),
                                          ('中四或以下', '中四或以下'),
                                          ('中五至中七或DSE', '中五至中七或DSE'),
                                          ('文憑或證書課程', '文憑或證書課程'),
                                          ('高級文憑或副學士', '高級文憑或副學士'),
                                          ('學士', '學士'),
                                          ('碩士或以上', '碩士或以上')],
                                 default='')
    income = SelectField('每月收入：',
                         choices=[('', '請選擇'),
                                  ('$10,000 或以下', '$10,000 或以下'),
                                  ('$10,001 - $20,000', '$10,001 - $20,000'),
                                  ('$20,001 - $30,000', '$20,001 - $30,000'),
                                  ('$30,001 - $40,000', '$30,001 - $40,000'),
                                  ('$40,001 - $50,000', '$40,001 - $50,000'),
                                  ('$50,001 - $60,000', '$50,001 - $60,000'),
                                  ('$60,001 或以上', '$60,001 或以上')])
    usergroup = SelectField(choices=[('admin', 'admin'),
                                     ('author', 'author'),
                                     ('normalUser', 'normalUser')],
                            default='normalUser')
    password = PasswordField('設定密碼*：', validators=[DataRequired()])
    password2 = PasswordField('再輸入密碼*：', validators=[DataRequired(), EqualTo('password', message='確認密碼不一致')])
    getinfo = BooleanField('本人同意收取香港經濟日報集團所發出的推廣資訊', default=True)
    submit = SubmitField('註冊')

    def validate_username(self, username):
        users = user.query.filter_by(username=username.data).first()
        if users is not None:
            raise ValidationError('用戶名稱已被使用')

    def validate_email(self, email):
        users = user.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('電郵地址已被註冊')


class LoginForm(FlaskForm):
    username = StringField('用戶名：', validators=[DataRequired()])
    password = PasswordField('密碼：', validators=[DataRequired()])
    remember_me = BooleanField('保持登入')
    submit = SubmitField('登入')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('電郵地址*：', validators=[DataRequired(message="請輸入電郵地址"), Email(message="請輸入正確電郵格式")])
    submit = SubmitField('完成')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('密碼：', validators=[DataRequired()])
    password2 = PasswordField('再輸入密碼*：', validators=[DataRequired(), EqualTo('password', message='確認密碼不一致')])
    submit = SubmitField('重設密碼')


class EditProfileForm(FlaskForm):
    password = PasswordField('更改密碼：', validators=[DataRequired()])
    password2 = PasswordField('再輸入密碼*：', validators=[DataRequired(), EqualTo('password', message='確認密碼不一致')])
    submit = SubmitField('提交')

    def __init__(self, original_password_hash, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_password = original_password_hash

    def validate_password(self, password_hash):
        if password_hash.data != self.original_password:
            pw = user.query.filter_by(password_hash=self.password.data).first()
            if pw is not None:
                raise ValidationError('Please use a different password.')


class PostForm(FlaskForm):
    title = StringField('標題')
    author = QuerySelectField('作者', query_factory=author_query, allow_blank=True, get_label="username")
    body1 = StringField('主旨')
    body2 = TextAreaField('內文')
    theme = StringField('主題')
    tag = StringField('標籤')
    type = SelectField(choices=[('video', 'video影片'), ('article', 'article文章')])
    submit = SubmitField('發佈')


class AuthorForm(FlaskForm):
    username = StringField('Author Name')
    usergroup = SelectField('usergroup', choices=[('author', 'Author')])
    submit = SubmitField('Submit')


class TagForm(FlaskForm):
    tag = StringField('Add tag：', validators=[DataRequired()])
    submit = SubmitField('完成')


class CarouselForm(FlaskForm):
    title = StringField('Title：', validators=[DataRequired()])
    img = StringField('Cover：', validators=[DataRequired()])
    link = StringField('Link：', validators=[DataRequired()])
    submit = SubmitField('完成')

