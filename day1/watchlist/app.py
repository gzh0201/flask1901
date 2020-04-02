import os
import sys

from flask import Flask,render_template,url_for
import click
from flask_sqlalchemy import SQLAlchemy  #导入扩展类

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

#linux
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.path.join(app.root_path,'data.db')
#window
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭了对模型修改的监控
db = SQLAlchemy(app)#初始化扩展，传入程序实例app

#models
class User(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String(20))
    year = db.Column(db.String(4))

#views
@app.route('/')
def index():
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
    return render_template('index.html',name=name,movies=movies)
    # return "<h1>Hello,Flask 中国<h1>"

#动态url
# @app.route('/index/<name>')
# def home(name):
#     print(url_for("home",name="Bruce"))
#     return "<h1>Hello,%s<h1>"%name



#自定义命令
@app.cli.command()  #装饰器，注册命令
@click.option('--drop',is_flag=True,help="删除后再创建")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")