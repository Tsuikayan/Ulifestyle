from datetime import datetime
from flask import Flask, render_template, send_from_directory, redirect, url_for, request, Response
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
bootstrap = Bootstrap()
UPLOAD_FOLDER = 'img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


@app.route('/')
@app.route('/index')
def index():
    return render_template('auth/register.html')


if __name__ == '__main__':
    app.run()
