import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)


app = Blueprint('common', __name__)


def getHttpErrorText(err, ext={}) -> str:
    logger = current_app.logger
    logger.error(f'[{err.__class__.__name__}]{err}')
    texts = {
        404 : 'リソースが見つかりませんでした。',
        'server_error' : '通信先でサーバーエラーが発生しています。時間をおいて再度お試しください。'
    }
    texts.update(ext)
    code = err.code if err.code < 500 else 'server_error'
    return texts.get(code, 'エラーが発生しました。しばらくお待ちください。')


def getAllErrorText(err) -> str:
    logger = current_app.logger
    logger.error(f'[{err.__class__.__name__}]{err}')
    return 'エラーが発生しました。しばらくお待ちください。'


# -----------------------------------------------
# session utils
# -----------------------------------------------


def set_session_message(message: str):
    '''リダイレクト先でメッセージを表示させたいときこの関数を利用。
    \n ただ、その画面に表示させたいときはflashを使うこと。
    '''
    session['message'] = message


@app.before_app_request
def display_session_message():
    message = session.get('message')
    if message is not None:
        flash(message)
        session['message'] = None
