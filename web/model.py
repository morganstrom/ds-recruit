from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

from config import BaseConfig

# Database configurations
app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

# create user class
class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.userid

    def __repr__(self):
        return '<User %r>' % self.email

# Create response class
class Response(db.Model):
    __tablename__ = 'responses'
    responseid = db.Column(db.Integer, primary_key=True)
    responsetime = db.Column(db.DateTime, nullable=False)
    response = db.Column(db.String(120), nullable=False)
    itemid = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'))

    def __init__(self, response, itemid, userid):
        self.responsetime = datetime.utcnow()
        self.response = response
        self.itemid = itemid
        self.userid = userid

    def __repr__(self):
        return '<Response %r>' % self.responseid


# Create tables
db.create_all()

# Initialize database
db.init_app(app)
