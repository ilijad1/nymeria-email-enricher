import string
from datetime import datetime

from Crypto.Random import random
from flask_login import UserMixin
from nymeria_enricher import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def keygen(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Personal Information
    access_key = db.Column(db.String(32), unique=True, nullable=False, default=keygen())
    nymeria_api_key = db.Column(db.String(32), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
