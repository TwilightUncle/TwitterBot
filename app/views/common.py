import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


app = Blueprint('common', __name__)


# -----------------------------------------------
# session utils
# -----------------------------------------------


def set_session_message(message: str):
    session['message'] = message


@app.before_app_request
def display_session_message():
    message = session.get('message')
    if message is not None:
        flash(message)
        session['message'] = None
