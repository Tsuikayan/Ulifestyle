from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
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


@app.route('/register_test', methods=['GET', 'POST'])
def register_test():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_test'))
    return render_template('register_test.html', title="會員登記", form=form)


@app.route('/login_test', methods=['GET', 'POST'])
def login_test():
    form = LoginForm()
    return render_template('login_test.html', title="會員登入", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', title="博客主頁–U Blog")


if __name__ == '__main__':
    app.run()
