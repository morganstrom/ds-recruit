# config.py

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']

    MYSQL_USER = os.environ['MYSQL_USER']
    MYSQL_PASSWORD = os.environ['MYSQL_ROOT_PASSWORD']
    MYSQL_DB = os.environ['MYSQL_DATABASE']
    MYSQL_HOST = os.environ['MYSQL_HOST']
    MYSQL_PORT = os.environ['MYSQL_PORT']

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % \
                              (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
