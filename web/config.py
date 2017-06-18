# config.py

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    MYSQL_DATABASE_DB = os.environ['MYSQL_DATABASE']
    MYSQL_DATABASE_USER = os.environ['MYSQL_USER']
    MYSQL_DATABASE_PASSWORD = os.environ['MYSQL_ROOT_PASSWORD']
    MYSQL_DATABASE_HOST = os.environ['DB_HOST']
    # DB_PORT = os.environ['DB_PORT']