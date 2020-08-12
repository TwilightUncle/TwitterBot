import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)


app = Blueprint('common', __name__)


def getHttpErrorText(err, ext={}) -> str:
    logger = current_app.logger
    logger.error(f'{err}')
    texts = {
        404 : 'リソースが見つかりませんでした。',
        'server_error' : '通信先でサーバーエラーが発生しています。時間をおいて再度お試しください。'
    }
    texts.update(ext)
    code = err.code if err.code < 500 else 'server_error'
    return texts.get(code, f'エラーが発生しました。サイト管理者にエラーコードと発生したURLをお知らせください。エラーコード:{err.code}')


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
