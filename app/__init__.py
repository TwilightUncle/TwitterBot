import os
from flask import Flask
from app.database import init_db
from app.const import ApplicationConst
import app.models

def create_app(config_name='default', db_path=None):
    # initialize application
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
    if db_path:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path

    # initialize database
    init_db(app)

    # register blueprints
    from app.views import common
    app.register_blueprint(common.app)
    from app.views import web
    app.register_blueprint(web.app)
    from app.views import api
    app.register_blueprint(api.app, url_prefix='/api')
    from app.views import auth
    app.register_blueprint(auth.app, url_prefix='/auth')

    app.add_url_rule('/', endpoint='index')
    
    # check exist instance directory
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
