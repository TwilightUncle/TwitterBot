import os
from flask import Flask
from app.database import init_db
from app.const import ApplicationConst
import app.models

def create_app(config_name='default'):

    DEV_CONF = 'config.DevelopmentConfig'
    config = {
        'production'    : 'config.ProductionConfig',
        'development'   : DEV_CONF,
        'testing'       : 'config.TestingConfig',

        'default'       : DEV_CONF
        }

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.get(config_name, DEV_CONF))
    app.config.from_pyfile('sensitive_data.cfg')

    init_db(app)

    # 設定値確認
    # print(app.config)
    
    # instanceフォルダがあるか確認
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
