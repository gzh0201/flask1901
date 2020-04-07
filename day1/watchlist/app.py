import os
import sys

from flask import Flask,render_template,url_for,redirect,request,flash
import click
#数据库
from flask_sqlalchemy import SQLAlchemy  #导入扩展类
#生成密码 验证密码
from werkzeug.security import generate_password_hash, check_password_hash
#登录
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user


# 得到当前平台
WIN = sys.platform.startswith('win')
if WIN:
    #请求头
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

# 配置要在实例化之前linux
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path,'data.db')
#window
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭了对模型修改的监控
app.config['SECRET_KEY'] = 'watchlist_dev'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
#初始化扩展，传入程序实例app 在配置之后
db = SQLAlchemy(app)

#实例化登录扩展类
login_manager = LoginManager(app) 
# 用户加载的函数
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user
login_manager.login_view='login'
login_manager.login_manage="您未登录"

#models
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    #生成密码
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    #验证密码
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

#模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user=user)

#表单添加
@app.route('/',methods=['GET','POST'])
#views
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash("不能为空或者超过最大长度")
            return redirect(url_for('index'))
        #报错表单数据
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("创建成功")
        return redirect(url_for('index'))
#     return render_template('index.html',name=name,movies=movies)
    # return "<h1>Hello,Flask 中国<h1>"
    # user = User.query.first()
    movies = Movie.query.all()
    # return render_template('index.html',user=user,movies=movies)
    return render_template('index.html',movies=movies)


#动态url
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name="Bruce"))
#     return "<h1>Hello,%s<h1>"%name

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash("不能为空或者超过最大长度")
            return redirect(url_for('index'),movie_id=movie_id)
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('更新完成')
        return redirect(url_for('index'))

    return render_template('edit.html',movie=movie)

#删除电影信息
@app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for("index"))

#登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # request在请求触发的时候才会包含数据
        username = request.form['username']
        password = request.form['password']
         # 验证数据
        if not username or not password:
            flash('输入错误')
            return redirect(url_for('index'))
        user = User.query.first()
        print(user.username)
        #验证用户和密码是否一致
        if user.username==username and user.validate_password(password):
            login_user(user)
            flash('登录成功')
            return redirect(url_for('index'))
        flash('用户名或密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')
    
#登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for("index"))

#自定义命令
#新建data.db的数据库初始化命令
@app.cli.command()  #装饰器，注册命令
@click.option('--drop',is_flag=True,help="删除后再创建")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")


#向data.db中写入数据的命令
@app.cli.command()
def forge():
    name='Bruce'
    movies = [
        {"title":"大赢家","year":"2020"},
        {"title":"囧架架","year":"2020"},
        {"title":"战狼","year":"2020"},
        {"title":"速度与激情","year":"2018"},
        {"title":"心花怒放","year":"2012"},
        {"title":"我的父亲母亲","year":"1995"},
        {"title":"战狼","year":"2020"},
        {"title":"速度与激情","year":"2018"},
        {"title":"心花怒放","year":"2012"},
        {"title":"我的父亲母亲","year":"1995"},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo("插入数据成功")

#生成管理员账号
@app.cli.command()
@click.option('--username',prompt=True,help='管理员账号')
@click.option('--password',prompt=True,help='管理员密码',hide_input=True,confirmation_prompt=True)
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户信息')
        user.username = username
        user.password_hash = password
    else:
        click.echo('创建用户信息')
        user = User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo("管理员创建完成")


#错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    # user = User.query.first()
    #返回模板和状态码
    # return render_template('404.html',user=user),404
    return render_template('404.html')


