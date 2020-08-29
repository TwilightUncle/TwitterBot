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

# migrationのスクリプトをDBに反映(db未作成の時もこちらを利用)
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

dbを新規作成した場合、下記を実行し、初期ユーザー名やパスワードを任意のものに変更しに行く
```
$ flask job first_insert --twitter_screen_name [screen_name]
```

# 本番・デバッグ環境について
.envのFLASK_DEBUGを0にすると本番、1にするとテスト環境

# vueのビルド
```
$ npm run build
```
