import urllib
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.database import db
from app.views.common import set_session_message, getHttpErrorText, getAllErrorText
from app.views.auth import login_required
from lib.twitter import usersShow


app = Blueprint('user', __name__)


@app.route("/twitter_account", methods=('GET', 'POST'))
@login_required
def twitter_account():
    if request.method == 'POST':
        twitter_account_name = request.form['twitter_account_name']

        error = []
        if not twitter_account_name:
            error.append('入力してください。')

        try:
            response    = usersShow(screen_name=twitter_account_name)

        except urllib.error.HTTPError as e:
            error_texts = {
                404 : 'ツイッターアカウントが見つかりませんでした。',
                'server_error' : 'ツイッターのサーバーエラーが発生しています。時間をおいて再度お試しください。'
            }
            text = getHttpErrorText(e, error_texts)
            error.append(text)

        except Exception as e:
            error.append(getAllErrorText(e))
            
        else:
            twitter_user_id     = response.getUser().getUserId()
        
        if not error:
            g.user.twitter_user_id = twitter_user_id
            db.session.commit()
            set_session_message('ツイッターアカウントを登録しました。')
            return redirect(url_for('web.index'))

        flash('\n'.join(error))

    return render_template('user/twitter_account.html')
