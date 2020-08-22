import urllib
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.views.common import set_session_message, getHttpErrorText, getAllErrorText
from app.views.auth import login_required, is_staff
from lib.twitter.oauth.request_token import oauthRequestToken


app = Blueprint('oauth', __name__)


@app.route("/redirect", methods=('GET', 'POST'))
@login_required
@is_staff
def redirect():
    if request.method == 'POST':
        error = []
        oauth_token_secret = ''
        redirect_url = ''

        try:
            response = oauthRequestToken(url_for('oauth.callback', _external=True), 'write')
        except urllib.request.HTTPError as err:
            text = getHttpErrorText(err)
            error.append(text)
        except Exception as err:
            error.append(getAllErrorText(err))
        else:
            oauth_token_secret = response.getOauthTokenSeacret()
            if oauth_token_secret is None:
                error.append('リクエストトークンシークレットを取得することができませんでした。')

            redirect_url = response.getOauthRedirectEveryTimeUrl()
            if redirect_url is None:
                error.append('リクエストトークンを取得することができませんでした。')
        
        if not error:
            session['oauth_token_secret'] = oauth_token_secret
            return redirect(redirect_url)

        flash('\n'.join(error))

    return render_template('oauth/redirect.html')


@app.route("/callback")
@login_required
@is_staff
def callback():
    if request.args.get('oauth_verifier', None):
        set_session_message('ツイッターアプリ連携を拒否しました。')
        return redirect(url_for('web.index'))
    
    oauth_token_secret = session.get('oauth_token_secret')
    if not oauth_token_secret:
        set_session_message('sessionが不正です。正しい手順でアクセスしてください。')
        return redirect(url_for('web.index'))

    error = []
    oauth_token = request.args.get('oauth_token')
    if not oauth_token:
        error.append('パラメータを取得できませんでした(t)')

    oauth_verifier = request.args.get('oauth_verifier')
    if not oauth_verifier:
        error.append('パラメータを取得できませんでした(v)')
    
    if not error:
        pass

    set_session_message('\n'.join(error))
    return redirect(url_for('oauth.redirect'))
