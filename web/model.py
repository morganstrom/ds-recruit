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
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
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
        return self.user_id

    def __repr__(self):
        return '<User %r>' % self.user_name

# Create question class
class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question_key = db.Column(db.String(16), nullable=False)
    question_data = db.Column(db.JSON, nullable=False)
    question_solution = db.Column(db.String(64), nullable=False)

    def __init__(self, question_key, question_data, question_solution):
        self.question_key = question_key
        self.question_data = question_data
        self.question_solution = question_solution

    def get_key(self):
        return self.question_key

    def get_data(self):
        return self.question_data

    def score_response(self, response):
        if eval(self.question_solution):
            return 1
        else:
            return 0

    def __repr__(self):
        return '<Question %r' % self.question_key

# Create response class
class Response(db.Model):
    __tablename__ = 'responses'
    response_id = db.Column(db.Integer, primary_key=True)
    response_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    question_key = db.Column(db.String(16), nullable=False)
    response = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, question_key, response, score):
        self.user_id = user_id
        self.question_key = question_key
        self.response = response
        self.score = score
        self.response_time = datetime.utcnow()


    def __repr__(self):
        return '<Response %r>' % self.response_id


# Create tables
db.create_all()

# Initialize database
db.init_app(app)
