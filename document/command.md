# command list

# module install
'''
$ pipenv install xx
'''

## make sqlite file
```
$ FLASK_APP=run.py flask shell
>>> from app.database import db
>>> db.create_all()
>>> exit()

# or
$ flask job first_insert --twitter_screen_name [screen_name]
```

## migrate
flask-migrateをインストールしたので、db管理はこちらで。上記は忘れる。
```
# migration directri作成
$ flask db init

# migration スクリプト作成
$ flask db migrate

# migrationのスクリプトをDBに反映
$ flask db upgrade
$ flask db downgrade
```

## pytest
以下コマンドで実行
```
$ pytest

# 関数詳細つき
$ pytest -v
```

## dbについて
insert, update, deleteするときは必ず最後に以下を記述する事!
```
db.session.commit()
```
