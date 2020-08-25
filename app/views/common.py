import os
import pathlib
import imghdr
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from app.database import db
from lib.utils import generateRandomString


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


def allowed_file(file):
    # mimetypeで判定
    if not file.mimetype in current_app.config['ALLOWED_MIMETYPES']:
        return False
    return True


def saveUploadedImage(uploaded_file, save_dir_path) -> str:
    '''アップロード画像保存。ファイル名を返す
    '''
    def generateFilename():
        r_str = generateRandomString(32)
        r_str += '.' + imghdr.what(uploaded_file.stream)
        return os.path.join(save_dir_path, r_str)
    
    # ディレクトリがなければディレクトリ作成
    if not os.path.isdir(save_dir_path):
        os.makedirs(save_dir_path)

    file_name = generateFilename()
    # ファイル名のダブり回避のため、ダブるときは生成し直す
    while os.path.isfile(file_name):
        file_name = generateFilename()

    # 保存
    uploaded_file.save(file_name)
    return file_name


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
