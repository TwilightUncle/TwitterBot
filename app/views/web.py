from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.views.common import set_session_message
from app.views.auth import login_required


app = Blueprint('web', __name__)


@app.route("/")
@login_required
def index():
    return render_template('web/index.html')


@app.route("/hello")
def hello():
    '''test url
    '''
    return "Hello !"
