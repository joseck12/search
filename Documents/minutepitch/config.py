import os
from flask import Flask

class Config:
    SECRET_KEY = 'grESrtgb284gvfnfd58437bhb'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("jogachi4@gmail.com")
    MAIL_PASSWORD = os.environ.get("fabianski")
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://joseck:newpassword@localhost/pitches"

    DEBUG = True


class DevConfig(Config):
    pass

class TestConfig(Config):
    pass


config_options = {
'development':DevConfig,
'production':ProdConfig


}
