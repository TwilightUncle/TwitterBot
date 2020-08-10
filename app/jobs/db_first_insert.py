import click
from flask.cli import with_appcontext
from app.database import db
from app.models import User
from lib.utils import generateRandomString


@click.command('first_insert', help="db data first insert.")
@with_appcontext
def db_first_insert_run():
    try:
        password = generateRandomString(8)
        user = User.create('admin', password, 1)
        db.session.commit()
        print('初期データ挿入成功。\nuser_name : ' + user.name + '\npassword : ' + password)
    except:
        db.session.rollback()
        print('初期データ挿入失敗。')
