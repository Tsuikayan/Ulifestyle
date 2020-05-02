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
    slides = {
        'link1': 'https://hk.ulifestyle.com.hk/activity/detail/117043/',
        'img1': 'https://hk.ulifestyle.com.hk/cms/images/slider_photo/1220x686/202004/20200427113052-2-20200424164238-0-20200324190230-0-whatsapp-image-2020-03-24-at-18-50-10.jpeg',
        'title1': '【減價優惠】Sanrio全線分店推出春季限時大減價！卡通精品/文具/家品低至半價',

        'link2': 'https://travel.ulifestyle.com.hk/news/detail/31632/',
        'img2': 'https://travel.ulifestyle.com.hk/cms/theme_photo/20200427112315_1_banner1.png',
        'title2': '沖繩無居所失業男赴便利店買煙 店員收款感奇怪報警男子被捕',

        'link3': 'https://food.ulifestyle.com.hk/restaurant/news/detail/2625855',
        'img3': 'https://www.ulifestyle.com.hk/store/content/slider/1587961902_774250.jpg',
        'title3': '台灣超市推出歐美人氣甜品　Oreo＋Chips Ahoy／M&amp;M＋Snickers二合一雪糕',

        'link4': 'https://bit.ly/34zCL6W',
        'img4': 'https://beauty.ulifestyle.com.hk/cms/images/upload/homeslider/original/20200415114927__2c7da70679929f459946e1877dbd0447.jpg',
        'title4': '【轉季必讀】2020 春夏新品/穿搭/護膚/美甲/編髮提案！',

        'link5': 'https://blog.ulifestyle.com.hk/blogger/90travelcatp/?p=3962185',
        'img5': 'https://www.ulifestyle.com.hk/store/content/slider/1587961832_166587.jpg',
        'title5': '只需3種材料！在家製香滑雪糕',
    }
    videos = {
        'link1': 'https://www.ulifestyle.com.hk/video/1009',
        'img1': 'https://www.ulifestyle.com.hk/store/content/video_form/thumbnail/small/202004/9d2538357fe708d454a2c83abc889073.jpg',
        'title1': '【星級髮型師解答】潮濕天氣下頭髮容易出油/扁塌？ 告別油頭從5個日常習慣做起',
        'time1': '03:32',

        'link2': 'https://www.ulifestyle.com.hk/video/1013',
        'img2': 'https://www.ulifestyle.com.hk/store/content/video_form/thumbnail/small/202004/05836df3aad2d90989c53e3e09a3dd2c.png',
        'title2': '三餸一湯系列！新手零失敗小菜食譜 電飯煲沙薑雞／蒜蓉牛油煮大蝦／芝士韓式炸雞翼／合掌瓜栗子湯',
        'time2': '01:29',

        'link3': 'https://www.ulifestyle.com.hk/video/594',
        'img3': 'https://www.ulifestyle.com.hk/store/content/video_form/thumbnail/small/201909/9572693fef845ca7d41098135ca98cc5.jpg',
        'title3': '【隨時贏精彩禮遇！】即時免費下載，睇盡最Hit生活資訊！',
        'time3': '00:36',
    }
    hk = {
        'link1': 'https://hk.ulifestyle.com.hk/activity/detail/116891/買口罩-oxyair-mask-hk口罩4月15日起開賣-手機app每日2次抽籤發售-附教學',
        'img1': 'https://hk.ulifestyle.com.hk/cms/images/event/300x200/202004/20200401142415_0_90924817-126544275614156-8982620320842121216-n.jpg',
        'title1': '【買口罩】Oxyair Mask HK口罩4月15日起開賣 手機App每日2次抽籤發售(附教學)',
    }
    travel = {
        'link1': 'https://travel.ulifestyle.com.hk/news/detail/31706/日本派每人10萬日圓補助金',
        'img1': 'https://travel.ulifestyle.com.hk/cms/news_photo/300x200/20200430150725__340503_s.jpg',
        'title1': '日本派每人10萬日圓補助金　黑幫霸氣拒領：平時已為社會添麻煩',
    }
    food = {
        'link1': 'https://food.ulifestyle.com.hk/restaurant/news/detail/2619728/kfc優惠4月2020-KFC全新推出椒麻脆辣雞-著數折扣券-外賣速遞優惠碼-手機app限定coupon一覽',
        'img1': 'https://resource01-proxy.ulifestyle.com.hk/res/v3/image/content/2615000/2619728/s2_300.jpg',
        'title1': '【kfc優惠4月2020】KFC全新推出椒麻脆辣雞！著數折扣券／外賣速遞優惠碼／手機app限定coupon一覽',
    }
    beauty = {
        'link1': 'https://beauty.ulifestyle.com.hk/shopping/sale/18418/名牌網購-farfetch低至半價-精選20款百搭手袋-全部港幣-4000以下',
        'img1': 'https://beauty.ulifestyle.com.hk/cms/images/upload/news/thumbnail/20200416190036__8fa14cdd754f91cc6554c9e71929cce7.jpg',
        'title1': '【名牌網購】FARFETCH低至半價！精選20款百搭手袋！全部港幣$4000以下！',
    }
    rank01 = {
        'link1': 'https://hk.ulifestyle.com.hk/topic/detail/210635/家師父一體-3組簡單動作測試身體年齡-手肘並攏抬不高過下巴反映體齡超過50',
        'title1': '【家師父一體】3組簡單動作測試身體年齡 手肘並攏抬不高過下巴反映體齡超過50',
    }
    rank02 = {
        'link1': 'https://travel.ulifestyle.com.hk/news/detail/31572/馬爾代夫受恐怖襲擊-港口爆炸燒船-隨機刺傷遊客',
        'title1': '馬爾代夫受恐怖襲擊 港口爆炸燒船、隨機刺傷遊客',
    }
    rank03 = {
        'link1': 'https://food.ulifestyle.com.hk/restaurant/news/detail/2622516/羅宋湯起源-羅宋湯由來原來是與一場-紅白大戰-有關-細數羅宋湯鮮為人知的二三事',
        'title1': '【羅宋湯起源】羅宋湯由來原來是與一場「紅白大戰」有關？細數羅宋湯鮮為人知的二三事',
    }
    rank04 = {
        'link1': 'https://beauty.ulifestyle.com.hk/beauty/skincare/18438/防曬2020-紫外線對策-春夏人氣開架防曬15選-清爽凝膠-乳霜質地',
        'title1': '【防曬2020】紫外線對策！春夏人氣開架防曬15選！清爽凝膠、乳霜質地！',
    }
    ublog1 = {
        'index1': 'http://blog.ulifestyle.com.hk/travel_blogger/sammie/',
        'icon1': 'https://blog.ulifestyle.com.hk/travel_blogger/wp-content/uploads/avatars/40000/800000090/1495357286-bpfull.jpg',
        'link1': 'http://blog.ulifestyle.com.hk/travel_blogger/sammie/?p=7128',
        'title1': '【中部北陸】從名古屋出發玩日本中部 利用',
        'name1': '沙米旅行手帖 Somewhere Journ',
    }
    ublog2 = {
        'index1': 'https://blog.ulifestyle.com.hk/blogger/sang0728/',
        'icon1': 'https://blog.ulifestyle.com.hk/blogger/wp-content/uploads/avatars/5/110342/1411421009-bpfull.jpg',
        'link1': 'https://blog.ulifestyle.com.hk/blogger/sang0728/?p=3976147',
        'title1': '日本北海道遊記 攻略 輕旅遊 小樽 三角',
        'name1': '林公子生活遊記',
    }
    ublog3 = {
        'icon1': 'https://blog.ulifestyle.com.hk/travel_blogger/wp-content/uploads/avatars/40000/800000090/1495357286-bpfull.jpg',
        'link1': 'http://blog.ulifestyle.com.hk/travel_blogger/sammie/?p=7128',
        'comment1': 'S O L D 。 O U T',
    }
    return render_template('index.html', title="首頁", slides=slides, videos=videos, hk=hk, travel=travel, food=food, beauty=beauty, rank01=rank01, rank02=rank02, rank03=rank03, rank04=rank04, ublog1=ublog1, ublog2=ublog2, ublog3=ublog3)


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
    return render_template('reset_password.html', title="重設密碼", form=form)


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


@app.route('/edit_carousel')
def edit_carousel():
    return render_template('edit_carousel.html', title="編輯封面")


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title="個人檔案")


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = None
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
    return render_template('add_post.html', title="新增貼文", form=form)

if __name__ == '__main__':
    app.run()
