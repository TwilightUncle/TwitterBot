import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from app.models import User


app = Blueprint('auth', __name__)


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # get input
        username = request.form['username']
        password = request.form['password']
        # validate
        error = []
        if not username:
            error.append('Username is required.')
        if not password:
            error.append('Password is required.')
        if db.session.query(User).filter(User.name==username).first() is not None:
            error.append('User {} is already registered.'.format(username))
        # register
        if not error:
            user = User()
            user.name = username
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        flash('\n'.join(error))
    return render_template('auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # get input
        username = request.form['username']
        password = request.form['password']
        # validate
        user = db.session.query(User).filter(User.name==username).first()
        error = []
        if user is None:
            error.append('Incorrect username.')
        elif not check_password_hash(user.password, password):
            error.append('Incorrect password')
        # passed
        if not error:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('web.index'))
        flash('\n'.join(error))
    return render_template('auth/login.html')


@app.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id==user_id).first()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
