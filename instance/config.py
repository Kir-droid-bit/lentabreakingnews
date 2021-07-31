import os

class Person(object):
    DEBUG = False
    HOST = '127.0.0.100'
    PORT = '80'
class CONF_DATABASE(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    # print(app.config['SECRET_KEY'])
