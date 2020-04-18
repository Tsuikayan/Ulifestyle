from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, logout_user
from flask_bootstrap import Bootstrap

app = Flask(__name__)
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
    return render_template('register.html', title="會員登記")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title="會員登入")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', title="博客主頁–U Blog")


if __name__ == '__main__':
    app.run()
