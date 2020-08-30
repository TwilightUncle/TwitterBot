import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db
from app.models import User
from app.const import constant
from app.views.common import set_session_message


app = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            set_session_message('ログインしてください。')
            session['login_redirect'] = request.url
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def is_administrator(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.permission > constant.PERMISSION_ADMIN:
            set_session_message('権限がないため、要求された画面は開けません。')
            return redirect(url_for('web.index'))
        return view(**kwargs)
    return wrapped_view


def is_staff(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.permission > constant.PERMISSION_BACKEND:
            set_session_message('権限がないため、要求された画面は開けません。')
            return redirect(url_for('web.index'))
        return view(**kwargs)
    return wrapped_view


@app.route('/register', methods=('GET', 'POST'))
@login_required
@is_staff
def register():
    if request.method == 'POST':
        # get input
        username = request.form['username']
        password = request.form['password']
        permission = request.form.get('permission')
        permission = permission or constant.PERMISSION_NOMAL

        # validate
        error = []
        if not username:
            error.append('Username is required.')
        if not password:
            error.append('Password is required.')
        if db.session.query(User).filter(User.name==username).first() is not None:
            error.append('User "{}" is already registered.'.format(username))

        # register
        if not error:
            user = User()
            user.name = username
            user.password = generate_password_hash(password)
            user.permission = permission
            db.session.add(user)
            db.session.commit()
            flash('新規ユーザーを登録しました。')
        else:
            flash('\n'.join(error))

    return render_template('auth/register.html', permissions=constant.PERMISSION_NAMES)


@app.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
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
        if not g.user.name == username and db.session.query(User).filter(User.name==username).first() is not None:
            error.append('User "{}" is already registered.'.format(username))

        # register
        if not error:
            user = g.user
            user.name = username
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('ユーザー情報を更新しました。')
        else:
            flash('\n'.join(error))

    return render_template('auth/edit.html')


@app.route('/sign-in', methods=['POST'])
def signIn():
    if request.method == 'POST':
        # get input
        username = request.json['user_name']
        password = request.json['password']

        # validate
        user = db.session.query(User).filter(User.name==username).first()
        error = []
        if user is None:
            error.append('Incorrect username.')
        elif not check_password_hash(user.password, password):
            error.append('Incorrect password.')
        
        # passed
        if not error:
            session.clear()
            session['user_id'] = user.id

            return jsonify({
                'is_login': 'true'
            })
    
    return jsonify({
        'is_login': 'false'
    })


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
            error.append('Incorrect password.')

        # passed
        if not error:
            # get redirect url
            redirect_url = session.get('login_redirect')
            if redirect_url is None:
                redirect_url = url_for('web.index')

            # login process
            session.clear()
            session['user_id'] = user.id
            set_session_message('You are now logged.')
            return redirect(redirect_url)

        flash('\n'.join(error))
        
    return render_template('auth/login.html')


@app.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id==user_id).first()
        # 変にセッションは残っていて、データがないとき
        if not g.user:
            return
            
        if g.user.permission == constant.PERMISSION_ADMIN:
            g.user.is_admin = 1
        if g.user.permission <= constant.PERMISSION_BACKEND:
            g.user.is_staff = 1


@app.route('/logout')
def logout():
    session.clear()
    set_session_message('Logged out.')
    return redirect(url_for('auth.login'))


@app.route('/delete')
@login_required
def delete():
    db.session.delete(g.user)
    db.session.commit()
    session.clear()
    set_session_message('User deleted.')
    return redirect(url_for('auth.login'))
