import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from werkzeug.utils import secure_filename
from app.database import db
from app.models import Bot
from app.views.common import set_session_message, getHttpErrorText, getAllErrorText
from app.views.auth import login_required, is_staff
from lib.twitter import usersShow


app = Blueprint('bot', __name__)


@app.route("/")
@login_required
@is_staff
def index():
    bot_list = db.session.query(Bot).filter(Bot.owner_id==g.user.id).all()
    return render_template('bot/index.html', bot_list=bot_list)


@app.route("/edit/<bot_id>")
@login_required
@is_staff
def edit(bot_id):
    bot = db.session.query(Bot).filter(Bot.id==bot_id).first()
    return render_template('bot/edit.html', bot=bot)
