from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Flask,
    make_response,
)
from flask_admin.contrib.sqla import ModelView
from nsetools import Nse
from sqlalchemy.exc import IntegrityError

from admin import admin
from db import db
from models.user import User

nse = Nse()

app = Flask(__name__)

app.config.from_pyfile('configs.py')

admin.init_app(app)

db.init_app(app)


admin.add_view(ModelView(User, db.session))


def user_search():
    found = User.query.filter(
        User.id == request.form['user_id'],
        User.pw == request.form['user_pw'],
    ).first()
    if found:
        return found
    else:
        return None


def cookie():
    have_cookie = request.cookies
    if have_cookie:
        return have_cookie
    else:
        return None


@app.errorhandler(404)
def not_found():
    return render_template('error.html'), 404


@app.route('/')
def index():
    if cookie():
        # stock_list = nse.get_index_list()
        q = nse.get_quote('infy')
        return render_template('index.html', nse=q)
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if user_search():
            usr = user_search()
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie('money', str(usr.money))
            resp.set_cookie('id', usr.id)
            return resp
        else:
            return 'Failed!'

    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if user_search():
            return render_template('login.html')
        else:
            new = User()
            new.id = request.form['user_id']
            new.pw = request.form['user_pw']
            db.session.add(new)
            try:
                db.session.commit()
            except IntegrityError:
                return '중복된 ID 입니다.', 400
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie('id', new.id)
            resp.set_cookie('money', new.money)
            return resp
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    if request.method == 'GET' and cookie():
        resp = make_response(redirect(url_for('login')))
        return resp
    else:
        return 'Error'


@app.route('/stock')
def stock():
    if request.method == 'POST':
        if request.form['mode'] == 'buy':
            return ''
        else:
            return ''
    else:
        return ''


@app.route("/search/<idx>/<pw>")
def search(idx, pw, is_web=True):
    found = User.query.filter(
        User.id == idx,
        User.pw == pw,
    ).first()
    if found:
        if is_web:
            return 'Success! %s' % (found.id, )
        else:
            return found
    if is_web:
        return 'failed'
    else:
        return None


@app.route("/delete/<name>/<idx>/<pw>")
def delete(name, idx, pw):
    found = search(name, idx, pw, is_web=False)
    db.session.delete(found)
    db.session.commit()
    return 'deleted!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
