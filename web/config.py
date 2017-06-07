# config.py

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    MYSQL_DATABASE_DB = os.environ['DB_NAME']
    MYSQL_DATABASE_USER = os.environ['DB_USER']
    MYSQL_DATABASE_PASSWORD = os.environ['DB_PASS']
    MYSQL_DATABASE_HOST = os.environ['DB_HOST']
    # DB_PORT = os.environ['DB_PORT']