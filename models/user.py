from datetime import datetime

from db import db


class User(db.Model):
    """
    from test import db
    db.create_all()
    """
    __tablename__ = "user"

    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(30), unique=True)
    pw = db.Column(db.String(30))
    money = db.Column(db.Integer, default=10000000)
    created = db.Column(db.DateTime, default=datetime.now)

    # no __init__()
