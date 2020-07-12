import pytest
from flask import g, session
from app.database import db
from app.models import User


def test_register(client, app):
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
        (''             , ''        , 'Username is required.\nPassword is required.'),
        ('testregister' , ''        , 'Password is required.'),
        ('test'         , 'test'    , 'already registered.')
    )
)
def test_register_validate_input(client, app, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username' : username, 'password' : password}
    )
    assert message in response.data.decode('utf-8')
