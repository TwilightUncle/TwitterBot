import click
import urllib
from flask.cli import with_appcontext
from app.database import db, init_db
from app.models import User, Bot
from lib.utils import generateRandomString
from lib.twitter.users.show import usersShow


@click.command('first_insert', help="db data first insert. インターネット接続必須(twitter apiを利用するため)")
@click.option('--twitter_screen_name', type=click.STRING)
@with_appcontext
def db_first_insert_run(twitter_screen_name):
    if not twitter_screen_name:
        print('--twitter_screen_nameオプションを指定し実行してください。@以下のユーザー名です。')
        return

    try:
        # user
        password = generateRandomString(8)
        user = User.create('admin', password, 1)

        # bot
        twitter_user = usersShow(screen_name=twitter_screen_name)
        bot = Bot.create(
            owner_id=user.id,
            twitter_user_id=twitter_user.getUser().getUserId(),
            screen_name=twitter_screen_name
        )

        # commit
        db.session.commit()
        print('初期データ挿入成功。\nuser_name : ' + user.name + '\npassword : ' + password)

    except urllib.error.HTTPError as err:
        print(f'APIアクセスでHTTPErrorが発生しました。エラーコード:{err.code}')
        raise err

    except Exception as exce:
        db.session.rollback()
        print(exce)
        print('初期データ挿入失敗。')
