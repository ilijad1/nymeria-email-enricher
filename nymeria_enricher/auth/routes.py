from flask_login import current_user, login_user

from flask import Blueprint, flash, render_template, request, url_for
from flask_login import current_user, login_user
from werkzeug.utils import redirect

from nymeria_enricher import Config, db
from nymeria_enricher.models import User

auth_blueprint = Blueprint('auth', __name__)

users = []
user1 = {
    'access_key': 'test1',
    'nymeria_api_key': Config.NYMERIA_API_KEY
}
user2 = {
    'access_key': 'test2',
    'nymeria_api_key': Config.NYMERIA_API_KEY
}
user3 = {
    'access_key': 'test3',
    'nymeria_api_key': Config.NYMERIA_API_KEY
}

users.append(user3)
users.append(user2)
users.append(user1)

def create_users():
    for user in users:
        exists = db.session.query(db.exists().where(User.access_key == user['access_key'])).scalar()
        if not exists:
            _user = User(
                access_key=user['access_key'],
                nymeria_api_key=user['nymeria_api_key']
                         )
            db.session.add(_user)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

@auth_blueprint.route("/", methods=['GET', 'POST'])
@auth_blueprint.route("/auth", methods=['POST', 'GET'])
def auth():
    _users_created = create_users()
    if _users_created:
        pass

    if current_user.is_authenticated:
        return redirect(url_for('csv_enrich.upload'))

    if request.method == 'POST':
        key = request.form.get('access_key')
        remember_me = True if request.form.get('remember_me') == 'on' else False

        try:
            user = User.query.filter_by(access_key=key).first()
        except Exception as e:
            flash("Invalid Key, please try again...", 'danger')
            return render_template('auth.html')

        if len(key) == 5 and user is not None:
            login_user(user, remember=remember_me)
            flash("Login Successful", 'success')
            return redirect(url_for('csv_enrich.upload'))
        else:
            flash("Invalid Key, please try again...", 'danger')
            return render_template('auth.html')
    elif request.method == "GET":
        return render_template('auth.html')
    else:
        flash("Invalid Request, please try again...", 'danger')
        return render_template('auth.html')



