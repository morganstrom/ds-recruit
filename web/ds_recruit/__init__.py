import os
from datetime import timedelta

from flask import Flask
from flask.ext.mysql import MySQL

# Initialize flask app
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
app.permanent_session_lifetime = timedelta(minutes=120)

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'morgan'
app.config['MYSQL_DATABASE_DB'] = 'ds_recruit'
app.config['MYSQL_DATABASE_HOST'] = 'mysql_1'
mysql.init_app(app)

import ds_recruit.main