import os
import logging.config
import yaml
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
    
    # initialize logger
    with open('config.yaml') as file:
        conf_dict = yaml.safe_load(file)
        logging.config.dictConfig(conf_dict)

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
    # from app.views import oauth
    # app.register_blueprint(oauth.app, url_prefix='/oauth')
    from app.views import user
    app.register_blueprint(user.app, url_prefix='/user')
    from app.views import bot
    app.register_blueprint(bot.app, url_prefix='/bot')

    app.add_url_rule('/', endpoint='index')

    # register cli commands
    from app.jobs import job
    app.cli.add_command(job)
    
    # check exist instance directory
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
