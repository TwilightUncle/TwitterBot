import pytest
from flask import g, session
from app.database import db
from app.models import User


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('a', 'test', b'Incorrect username.'),
        ('test', 'a', b'Incorrect password.')
    )
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session


@pytest.mark.parametrize(
    'path',
    (
        'auth/register',
        'auth/delete'
    )
)
def test_login_required_auth_get(client, auth, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/' + path


def test_register(client, app, auth):
    auth.login()

    # check GET request
    assert client.get('/auth/register').status_code == 200
    # check POST request
    response = client.post(
        '/auth/register',
        data={'username' : 'testregister', 'password' : 'testpassword'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert db.session.query(User).filter(User.name=='testregister').first() is not None


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        (''             , 'aaaa'    , 'Username is required.'),
        (''             , ''        , 'Username is required.\nPassword is required.'),
        ('testregister' , ''        , 'Password is required.'),
        ('test'         , 'test'    , 'already registered.')
    )
)
def test_register_validate_input(client, auth, username, password, message):
    auth.login()
    response = client.post(
        '/auth/register',
        data={'username' : username, 'password' : password}
    )
    assert message in response.data.decode('utf-8')


def test_delete(client, app, auth):
    auth.login()
    response = client.get('auth/delete')
    assert response.headers['Location'] == 'http://localhost/auth/login'

    with app.app_context():
        assert db.session.query(User).filter(User.name=='test').first() is None
