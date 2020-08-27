from flask import Blueprint


# 静的ファイル用のディレクトリを追加
app = Blueprint('uploads', __name__, static_folder='../../uploads', static_url_path='/uploads')
