from flask import flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app.email import send_password_reset_email
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from app.forms import *
from app import app, db
from app.models import User, Post, Tag, Carousel


bootstrap = Bootstrap()
UPLOAD_FOLDER = 'img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


@app.route('/')
@app.route('/index')
def index():
    tags = Tag.query.order_by(Tag.tag).all()
    slides = Carousel.query.order_by(Carousel.id.desc()).all()
    title1 = "title"
    img = "https://www.ulifestyle.com.hk/store/content/video_form/thumbnail/small/202004/9d2538357fe708d454a2c83abc889073.jpg"
    icon = "https://blog.ulifestyle.com.hk/travel_blogger/wp-content/uploads/avatars/40000/800000090/1495357286-bpfull.jpg"
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
    return render_template('home_page/index.html', title="首頁",
                           hk=hk, travel=travel, food=food, beauty=beauty, rank01=rank01, rank02=rank02, rank03=rank03, rank04=rank04, ublog1=ublog1, ublog2=ublog2, ublog3=ublog3,
                           videos=videos, tags=tags, slides=slides)


@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(
            tag=form.tag.data
        )
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('admin/add_tag.html', title="Add Tag", form=form)


@app.route('/edit_carousel', methods=['GET', 'POST'])
def edit_carousel():
    form = CarouselForm()
    if form.validate_on_submit():
        carousel = Carousel(
            title=form.title.data,
            img=form.img.data,
            link=form.link.data
        )
        db.session.add(carousel)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_carousel.html', title="Edit Carousel", form=form)


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
    slides = {
        'link1': 'https://blog.ulifestyle.com.hk/blogger/imkiu/2020/03/%e3%80%90%e9%a6%99%e6%b8%af%e3%80%82%e5%92%96%e5%95%a1%e5%ba%97%e3%80%91mums-not-home-%ef%bd%9c%e8%88%8a%e5%bc%8f%e5%94%90%e6%a8%93%e4%b8%8a%e6%9c%89%e5%80%8b%e5%a4%a9%e9%a6%ac%e8%a1%8c%e7%a9%ba/',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/sliders/images/ul/Mum%E2%80%99s%20Not%20Home-1587009033.jpg',
        'text1': '【飲食】Mum’s Not Home'
    }
    publish = {
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?latest20',
        'title1': '最新發佈',
        'link2': 'https://blog.ulifestyle.com.hk/blogger/hairlessprice/2020/04/hairless%e8%a9%95%e5%83%b9-%e5%a5%bd%e5%94%94%e5%a5%bd%ef%bc%9f-%e5%b0%88%e6%a5%ad%e8%a9%95%e5%83%b9%e5%8e%9f%e5%9b%a0%ef%bc%9f/',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/landing-blog-thumbnails/2020/04/3963566.jpg',
        'text1': 'HAiRLESS評價 好唔好？ 專業評價原因？'
    }
    popular = {
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?hottest20',
        'title1': '人氣文章',
        'link2': 'https://blog.ulifestyle.com.hk/blogger/hangryplanet/?p=3978858',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/landing-blog-thumbnails/2020/04/3978858.jpg',
        'text1': '【絕不失敗】簡單又惹味！自家製辣得過癮雞煲'
    }
    travel = {
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?s&memberType=member&searchChannel=UTRAVEL',
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/cat-travel.jpg',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/line-cat-travel.gif',
        'link2': 'https://blog.ulifestyle.com.hk/blogger/dollyling/2020/04/%e3%80%90%e5%bc%98%e5%a4%a7%e3%80%91%e4%bd%8f%e5%ae%bf%ef%bc%8e%e7%89%b9%e5%88%a5%e6%8e%a8%e8%96%a6%e9%a6%96%e6%ac%a1%e5%87%ba%e9%81%8a%e9%9f%93%e5%9c%8b%ef%bd%9e%e5%85%85%e6%bb%bf%e8%a6%aa%e5%88%87/',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/avatars/6/125935/1452267161-bpfull.jpg',
        'text1': '-【弘大】住宿．特別推薦首次出遊韓國'
    }
    food = {
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?s&memberType=member&searchChannel=UFOOD',
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/cat-food.jpg',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/line-cat-food.gif',
        'link2': 'https://blog.ulifestyle.com.hk/blogger/flyyoursoul/2020/04/iced-baileys-chocolate-%e2%94%82-%e5%87%8d%e7%99%be%e5%88%a9%e6%9c%b1%e5%8f%a4%e5%8a%9b/',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/avatars/12/244549/1543929704-bpfull.jpg',
        'text1': 'Iced Baileys Chocolate│凍百利朱古力'
    }
    beauty = {
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?s&memberType=member&searchChannel=UBEAUTY&page=1&category=1007794&sorting=latest',
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/cat-beauty.jpg',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/line-cat-beauty.gif',
        'link2': 'https://blog.ulifestyle.com.hk/blogger/beautysearch/2020/04/2c%e9%aa%a8%e8%b3%aa%e5%87%8d%e9%bd%a1%e6%b3%95-%ef%bd%a1%e2%82%80%e5%b9%b4%e8%bc%95%e9%96%8b%e5%a7%8b%e5%84%b2%e9%88%a3-%e0%ad%a8%e0%ad%a7bg%e5%bc%b7%e6%95%88%e6%b6%b2%e9%ab%94%e8%86%a0%e5%8e%9f/',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/avatars/2/50589/1401950341-bpfull.jpg',
        'text1': '2C骨質凍齡法 年輕開始儲鈣 BG強效液體膠原鈣'
    }
    blogger = {
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/icon-blog.gif',
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?s=&memberType=invite&page=1&sorting=latest',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/themes/landingblog/images/ul/title-blogger.gif',
        'link2': 'http://blog.ulifestyle.com.hk/travel_blogger/sammie/?p=71288',
        'img1': 'https://blog.ulifestyle.com.hk/travel_blogger/wp-content/uploads/avatars/40000/800000090/1495357286-bpfull.jpg',
        'text1': '【中部北陸】從名古屋出發玩日本中部 利用立山黒部、高山、松本地區周遊券',
        'text2': '沙米旅行手帖 Somewhere Journal'
    }
    rank = {
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/blog-rating-widget/images/ul/icon-rank.gif',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/blog-rating-widget/images/ul/title-rank.gif',
        'rank1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/blog-rating-widget/images/ul/rank-01.gif',
        'rank2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/blog-rating-widget/images/ul/rank-02.gif',
        'rank3': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/blog-rating-widget/images/ul/rank-03.gif',
        'link1': 'https://blog.ulifestyle.com.hk/blogger/hangryplanet/',
        'img1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/avatars/13/274796/1563527163-bpfull.jpg',
        'text1': '出走玩樂日誌',
    }
    comment = {
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/latest-comment-widget/images/ul/icon-msg.gif',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/latest-comment-widget/images/ul/title-msg.gif',
        'link1': 'https://blog.ulifestyle.com.hk/blogger/travelplanahead/?p=3878648/#comment-1091836',
        'img1': 'https://search.ulifestyle.com.hk/fileData/web/data/user/uk_4285832513854257827.jpg',
        'text1': 'CP值超高肥美海鮮市場【新潟寺泊】 【魚のアメ横】',
        'text2': 'Wanna go and enjoy Seafood over there! Pretty nice sunset too..:)'
    }
    tag = {
        'title1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/tag-widget/images/ul/icon-tag.gif',
        'title2': 'https://blog.ulifestyle.com.hk/blogger/wp-content/plugins/tag-widget/images/ul/title-tag.gif',
        'link1': 'https://blog.ulifestyle.com.hk/blogger/?s=%E6%97%A5%E6%9C%AC%E5%A4%A7%E5%88%86%E7%BE%8E%E9%A3%9F%E4%B9%8B%E6%97%852017&scope=tag',
        'link2': 'https://blog.ulifestyle.com.hk/blogger/?s=%28%E7%94%A8%E5%BE%8C%E6%84%9F%29&scope=tag',
        'link3': 'https://blog.ulifestyle.com.hk/blogger/?s=%EF%BC%A0travelplanahead&scope=tag',
        'link4': 'https://blog.ulifestyle.com.hk/blogger/?s=%23%20Skincare&scope=tag',
        'link5': 'https://blog.ulifestyle.com.hk/blogger/?s=#DailySalimHK%20#%20DailySalim%E6%8A%97%E8%8F%8C%E9%99%A4%E8%87%AD%E9%98%B2%E5%A1%B5%E5%99%B4%E9%9C%A7%20#%E6%B6%88%E6%AF%92%E5%99%B4%E9%9C%A7%20#%E6%8A%97%E7%96%AB%20#%E6%AE%BA%E6%BB%8599%%E7%B4%B0%E8%8F%8C%20#%E6%8A%97%E8%8F%8C%E9%99%A4%E8%87%AD%20#%E9%9F%93%E5%9C%8B%E8%A3%BD%E9%80%A0%20#%E5%AE%B6%E5%B1%85%E6%B6%88%E6%AF%92%20#%E9%A0%90%E9%98%B2%E6%84%9F%E6%9F%93%20#%E9%98%B2%E8%AD%B7&scope=tag&page=1&sorting=latest',
        'link6': 'https://blog.ulifestyle.com.hk/blogger/?s=#Ripple%20#%E6%9A%96%E5%AE%AE%E8%96%91%E9%BB%83%E5%A5%B6#%E5%A5%B3%E5%A3%AB%E6%81%A9%E7%89%A9#%E9%BB%83%E9%87%91%E5%A5%B6&scope=tag&page=1&sorting=latest',
        'link7': 'https://blog.ulifestyle.com.hk/blogger/?s=#soakoffgelhk%20#hardgelhk%20#softgelnails%20#hardgelnails%20#gelnailsdesign%20#gelnailhk%20#%E7%BE%8E%E7%94%B2%E8%A8%AD%E8%A8%88%20#%E9%A6%99%E6%B8%AF%E7%BE%8E%E7%94%B2%20#%E8%8D%94%E6%9E%9D%E8%A7%92%E7%BE%8E%E7%94%B2%20#BabooNail%20#%E6%BC%B8%E8%AE%8A%E7%94%B2%20#%E6%9A%88%E6%9F%93%E7%BE%8E%E7%94%B2%20#%E9%9F%93%E5%BC%8F%E7%BE%8E%E7%94%B2%20#beauty%20#Annielittlecake%20#hbgxo%20#hbgxoxo&scope=tag&page=1&sorting=latest',
        'link8': 'https://blog.ulifestyle.com.hk/blogger/?s=%E2%80%AC%20%E2%80%AAbeautyblogger&scope=tag',
        'link9': 'https://blog.ulifestyle.com.hk/blogger/?s=%5BSudio%20X%20Ett%20%5D&scope=tag',
        'link10': 'https://blog.ulifestyle.com.hk/blogger/?s=%26lt%3B%E8%A5%BF%E7%8F%AD%E7%89%99%E6%B5%B7%E9%AE%AE%E9%A3%AF&scope=tag',
        'link11': 'https://blog.ulifestyle.com.hk/blogger/?s=#Colgate%20#%E9%AB%98%E9%9C%B2%E6%BD%94%20#%E6%B0%A8%E5%9F%BA%E9%85%B8%E7%89%99%E8%86%8F%20#%E7%89%99%E9%BD%A6%20#%E6%8A%97%E8%A1%B0%E8%80%81%20#%E5%9B%A0%E7%89%99%E9%BD%A6%E5%95%8F%E9%A1%8C%E5%B0%8E%E8%87%B4%20#Teeth%20#Health%20#Beauty%20#Annielittlecake%20#hbgxo%20#hbgxoxo&scope=tag&page=1&sorting=latest',
        'link12': 'https://blog.ulifestyle.com.hk/blogger/?s=%23digital%20marketing&scope=tag',
        'link13': 'https://blog.ulifestyle.com.hk/blogger/?s=%23SMS%20Cosmetics%20%23NEO%20%23%E8%86%A0%E5%8E%9F%20%23Beauty%20%23Skincare%20%23Annielittlecake%20%23hbgxo%20%23hbgxoxo&scope=tag',
    }
    return render_template('blog.html', title="博客主頁", slides=slides, publish=publish, popular=popular, travel=travel,
                           food=food, beauty=beauty, blogger=blogger, rank=rank, comment=comment, tag=tag)


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
