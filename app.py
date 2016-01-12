from datetime import datetime
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Flask,
    jsonify,
    make_response,
)

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'asldjalkaonsjdklasd'
admin = Admin(app)
db = SQLAlchemy(app)


class User(db.Model):
    """
    from test import db
    db.create_all()
    """
    __tablename__ = "user"

    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(30), unique=True)
    pw = db.Column(db.String(30))
    money = db.Column(db.Integer, default=10000000)  # User default money = 1000만
    created = db.Column(db.DateTime, default=datetime.now)

    # no __init__()


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
    username = request.cookies.get('id')
    if username:
        return username
    else:
        return None


@app.route('/')
def index():
    if cookie():
        return render_template('index.html')
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
                return 'failed', 400
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie('id', new.id)
            resp.set_cookie('money', new.money)
            return resp
    else:
        return render_template('register.html')


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
