from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, current_app
)
from werkzeug.utils import secure_filename
from app.database import db
from app.models import Bot
from app.views.common import set_session_message, getHttpErrorText, getAllErrorText, allowed_file, saveUploadedImage
from app.views.auth import login_required, is_staff
from lib.twitter import usersShow


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
    if request.method == 'POST':
        error = []

        profile_image = request.files.get('profile_image')
        profile_image_saved_filename = ''
        background_image = request.files.get('background_image')
        background_image_saved_filename = ''

        if profile_image and not allowed_file(profile_image):
            error.append('プロフィール画像に想定していない種類のファイルが送信されました。')
        if background_image and not allowed_file(background_image):
            error.append('プロフィール背景画像に想定していない種類のファイルが送信されました。')

        if not error:
            if profile_image:
                profile_image_saved_filename = saveUploadedImage(
                    profile_image, 
                    f"{current_app.config['UPLOAD_BOT_PROFILE_IMAGE_FOLDER']}/{bot_id}"
                )
            if background_image:
                background_image_saved_filename = saveUploadedImage(
                    background_image, 
                    f"{current_app.config['UPLOAD_BOT_PROFILE_BACKGROUND_IMAGE_FOLDER']}/{bot_id}"
                )
        
        if not error:
            pass
        else:
            flash('\n'.join(error))

    bot = db.session.query(Bot).filter(Bot.id==bot_id).first()
    return render_template('bot/edit.html', bot=bot)
