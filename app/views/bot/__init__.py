import os
import urllib
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from werkzeug.utils import secure_filename
from app.database import db
from app.models import Bot, ProfileImageHistory
from app.views.common import set_session_message, getHttpErrorText, allowed_file
from app.views.auth import login_required, is_staff
from lib.twitter import usersShow

from app.views.bot.edit import saveImage, sendProfileImageForTwitter, sendProfileDataForTwitter


app = Blueprint('bot', __name__)


@app.route("/")
@login_required
@is_staff
def index():
    bot_list = db.session.query(Bot).filter(Bot.owner_id==g.user.id).all()
    return render_template('bot/index.html', bot_list=bot_list)


@app.route("/edit/<bot_id>", methods=('GET', 'POST'))
@login_required
@is_staff
def edit(bot_id:int):
    # post, get共通データ取得
    bot = db.session.query(Bot).filter(Bot.id==bot_id).first()

    if request.method == 'POST':
        error = []

        # get params
        profile_name                    = request.form.get('profile_name')
        url                             = request.form.get('url')
        location                        = request.form.get('location')
        description                     = request.form.get('description')

        # get files
        profile_image                   = request.files.get('profile_image')
        profile_image_saved_filename    = ''
        background_image                = request.files.get('background_image')
        background_image_saved_filename = ''

        # パラメータチェック
        max_len = 20
        if profile_name and len(profile_name) > max_len:
            error.append(f'プロフィール名の入力文字数は{max_len}文字以内にしてください。')
        max_len = 100
        if url and len(url) > max_len:
            error.append(f'プロフィールに関連付けるurlの入力文字数は{max_len}文字以内にしてください。')
        max_len = 30
        if location and len(location) > max_len:
            error.append(f'ロケーションの入力文字数は{max_len}文字以内にしてください')
        max_len = 160
        if description and len(description) > max_len:
            error.append(f'自己紹介欄の入力文字数は{max_len}文字以内にしてください')

        # アップロードファイルチェック
        if profile_image and not allowed_file(profile_image):
            error.append('プロフィール画像に想定していない種類のファイルが送信されました。')
        if background_image and not allowed_file(background_image):
            error.append('プロフィール背景画像に想定していない種類のファイルが送信されました。')

        if not error:
            # プロフィール情報をツイッターへ送信
            error = sendProfileDataForTwitter(bot, error, profile_name, url, location, description)

            # アップロードファイル保存
            profile_image_saved_filename, background_image_saved_filename = saveImage(bot_id, profile_image, background_image)

            # アップロードファイルをツイッターへ送信
            error = sendProfileImageForTwitter(bot, error, profile_image_saved_filename, background_image_saved_filename)
        

        if not error:
            # ファイルパスがすでに設定されていたら、Historyのほうへ移す
            if bot.profile_image_path:
                profile_image_history = ProfileImageHistory()
                profile_image_history.create(bot_id, bot.profile_image_path)
            bot.profile_image_path = profile_image_saved_filename
            db.session.commit()
            flash('設定を変更しました。')
        else:
            # ゴミが残らないように画像削除
            if profile_image_saved_filename != '':
                os.remove(profile_image_saved_filename)
            if background_image_saved_filename != '':
                os.remove(background_image_saved_filename)
            db.session.rollback()
            flash('\n'.join(error))
        
    # ツイッターの情報と同期をかける
    syncTwitterBotData(bot)

    return render_template('bot/edit.html', bot=bot)


def syncTwitterBotData(bot:Bot):
    error_text = 'データの同期に失敗しました。表示されている情報はtwitterで閲覧できる情報と相違がある可能性があります。'
    try:
        response = usersShow(user_id=bot.twitter_user_id)
    except urllib.error.HTTPError as err:
        text = getHttpErrorText(err)
        flash(error_text)
    except Exception as err:
        flash(error_text)
    else:
        # 同期した内容でDBを更新
        twitter_user_data = response.getUser()
        profile_image_url = twitter_user_data.getProfileImageUrlHttps().replace('_normal', '')
        bot.update(
            screen_name=twitter_user_data.getScreenName(),
            profile_name=twitter_user_data.getUserName(),
            url=twitter_user_data.getUrl(),
            location=twitter_user_data.getLocation(),
            description=twitter_user_data.getDescription(),
            profile_image_url=profile_image_url
        )
        db.session.commit()
