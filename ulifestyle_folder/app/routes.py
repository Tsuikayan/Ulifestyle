from flask import flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app.email import send_password_reset_email
from werkzeug.urls import url_parse
from flask_bootstrap import Bootstrap
from app.forms import *
from app import app, db
from app.models import User

bootstrap = Bootstrap()
UPLOAD_FOLDER = 'img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="首頁")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            gender=form.gender.data,
            phoneNumber=form.phoneNumber.data,
            year=form.year.data,
            month=form.month.data,
            day=form.day.data,
            educationLevel=form.educationLevel.data,
            income=form.income.data,
            usergroup=form.usergroup.data,
            getinfo=form.getinfo.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜您成為會員!!')
        return redirect(url_for('login'))
    return render_template('register.html', title="會員登記", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title="會員登入", form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', title="博客主頁–U Blog")


@app.route('/hk', methods=['GET', 'POST'])
def hk():
    return render_template('hk.html', title="HK港生活")


@app.route('/travel', methods=['GET', 'POST'])
def travel():
    return render_template('travel.html', title="Travel旅遊")


@app.route('/food', methods=['GET', 'POST'])
def food():
    return render_template('food.html', title="Food美食")


@app.route('/beauty', methods=['GET', 'POST'])
def beauty():
    return render_template('beauty.html', title="Beauty美容")


@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('download.html', title="download")


@app.route('/video', methods=['GET', 'POST'])
def video():
    return render_template('video.html', title="影片頻道")


@app.route('/sky_post', methods=['GET', 'POST'])
def sky_post():
    return render_template('sky_post.html', title="晴報SkyPost")


@app.route('/profile')
def profile():
    return render_template('profile.html', title="個人檔案")


if __name__ == '__main__':
    app.run()
