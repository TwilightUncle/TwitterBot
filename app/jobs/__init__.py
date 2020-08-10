from flask.cli import AppGroup
from app.jobs.db_first_insert import db_first_insert_run

# グループを作成
job = AppGroup('job')

# task関連のコマンドを追加していく
job.add_command(db_first_insert_run)
