from flask import Flask,render_template,url_for
app = Flask(__name__)

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

