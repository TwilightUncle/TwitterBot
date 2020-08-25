import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'dev'
    API_KEY = os.getenv('API_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # upload
    UPLOAD_BOT_PROFILE_IMAGE_FOLDER = './uploads/image/bot/profile'
    UPLOAD_BOT_PROFILE_BACKGROUND_IMAGE_FOLDER = './uploads/image/bot/profile_background'
    ALLOWED_MIMETYPES = set(['image/jpeg', 'image/png', 'image/gif'])

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    SERVER_NAME = "127.0.0.1:5000"
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
