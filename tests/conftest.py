import sys
import os
import tempfile

import pytest
from app import create_app
from app.database import db
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app('testing', 'sqlite:///' + db_path)

    with app.app_context():
        db.create_all()
        user = User()
        user.name = 'test'
        user.password = generate_password_hash('test')
        db.session.add(user)
        user2 = User()
        user2.name = 'other'
        user2.password = generate_password_hash('other')
        db.session.add(user2)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
