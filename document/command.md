# command list
## make sqlite file
```
$ FLASK_APP=run.py flask shell
>>> from app.database import db
>>> db.create_all()
>>> exit()
```
