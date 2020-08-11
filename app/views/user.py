import urllib
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.database import db
from app.views.common import set_session_message
from app.views.auth import login_required
from lib.twitter.users.show import TwitterApiUsersShowInput, TwitterApiUsersShowClient


app = Blueprint('user', __name__)


@app.route("/twitter_account", methods=('GET', 'POST'))
@login_required
def twitter_account():
    if request.method == 'POST':
        twitter_account_name = request.form['twitter_account_name']

        error = []
        code = 200
        if not twitter_account_name:
            error.append('入力してください。')
        try:
            inp                 = TwitterApiUsersShowInput()
            inp.setScreenName(twitter_account_name)
            client              = TwitterApiUsersShowClient()
            response            = client.exec(inp)
        except urllib.error.HTTPError as e:
            code = e.code
        else:
            twitter_user_id     = response.getUser().getUserId()
        
        if code == 404:
                error.append('ツイッターアカウントが見つかりませんでした。')
        
        if not error:
            g.user.twitter_user_id = twitter_user_id
            db.session.commit()
            set_session_message('ツイッターアカウントを登録しました。')
            return redirect(url_for('web.index'))

        flash('\n'.join(error))

    return render_template('user/twitter_account.html')
