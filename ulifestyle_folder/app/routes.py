from flask import flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app.email import send_password_reset_email
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from app.forms import *
from app import app, db
from app.models import User, Post


bootstrap = Bootstrap()
UPLOAD_FOLDER = 'img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


@app.route('/')
@app.route('/index')
def index():
    title1 = "title"
    img = "https://www.ulifestyle.com.hk/store/content/video_form/thumbnail/small/202004/9d2538357fe708d454a2c83abc889073.jpg"
    icon = "https://blog.ulifestyle.com.hk/travel_blogger/wp-content/uploads/avatars/40000/800000090/1495357286-bpfull.jpg"
    slides1 = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    slides2 = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    slides3 = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    slides4 = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    slides5 = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    videos = {
        'link1': '#',
        'img1': img,
        'title1': title1,
        'time1': '03:32'
    }
    hk = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    travel = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    food = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    beauty = {
        'link1': '#',
        'img1': img,
        'title1': title1
    }
    rank01 = {
        'link1': '#',
        'title1': title1
    }
    rank02 = {
        'link1': '#',
        'title1': title1
    }
    rank03 = {
        'link1': '#',
        'title1': title1
    }
    rank04 = {
        'link1': '#',
        'title1': title1
    }
    ublog1 = {
        'index1': '#',
        'icon1': icon,
        'link1': '#',
        'title1': title1,
        'name1': '沙米旅行手帖 Somewhere Journ'
    }
    ublog2 = {
        'index1': '#',
        'icon1': icon,
        'link1': '#',
        'title1': title1,
        'name1': '林公子生活遊記'
    }
    ublog3 = {
        'icon1': icon,
        'link1': '#',
        'comment1': 'S O L D 。 O U T'
    }
    return render_template('home_page/index.html', title="首頁", slides1=slides1, slides2=slides2, slides3=slides3,
                           slides4=slides4, slides5=slides5,
                           hk=hk, travel=travel, food=food, beauty=beauty, rank01=rank01, rank02=rank02, rank03=rank03, rank04=rank04, ublog1=ublog1, ublog2=ublog2, ublog3=ublog3,
                           videos=videos)


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
        return redirect(url_for('login'))
    return render_template('auth/register.html', title="會員登記", form=form)


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
    return render_template('auth/login.html', title="會員登入", form=form)


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
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', title="重設密碼", form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('login'))
    return render_template('auth/reset_password_request.html',
                           title='忘記密碼', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    return render_template('blog.html', title="博客主頁")


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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    return render_template('profile.html', title="個人檔案", form=form)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if(form.type.data == "article"):
          post = Post(
              author=current_user.username,
              theme=form.theme.data,
              title=form.title.data,
              body1=form.body1.data,
              body2=form.body2.data,
              tag=form.tag.data,
              site=form.site.data,
              type=form.type.data)
        else:
          videoFile = request.files['video']
          videoFile.save("uploads/" + secure_filename(videoFile.filename))
          post = Post(
              author=current_user.username,
              title=form.title.data,
              body1="uploads/" + secure_filename(videoFile.filename),
              body2=form.body2.data,
              site=form.site.data,
              type=form.type.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('admin/add_post.html', title="新增貼文", form=form)


if __name__ == '__main__':
    app.run()
