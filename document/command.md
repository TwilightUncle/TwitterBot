# command list
## make sqlite file
```
$ FLASK_APP=run.py flask shell
>>> from app.database import db
>>> db.create_all()
>>> exit()
```

## migrate
flask-migrateをインストールしたので、db管理はこちらで。上記は忘れる。
```
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db downgrade
```

## pytest
以下コマンドで実行
```
$ pytest
```
