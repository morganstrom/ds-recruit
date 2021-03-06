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
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime)

    responses = db.relationship('Response', backref='user', lazy=True)
    results = db.relationship('Result', backref='user', lazy=True)

    def __init__(self, email, password):
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
        return '<User %r>' % self.email

# Create question class
class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.String(16), nullable=False)
    question_key = db.Column(db.String(16), unique=True, nullable=False)
    question_data = db.Column(db.JSON, nullable=False)

    responses = db.relationship('Response', backref='question', lazy=True)

    def __init__(self, skill_id, question_key, question_data):
        self.skill_id = skill_id
        self.question_key = question_key
        self.question_data = question_data

    def get_id(self):
        return self.question_id

    def get_key(self):
        return self.question_key

    def get_data(self):
        return self.question_data

    def score_response(self, response):
        if eval(self.question_data['solution']):
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
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'), nullable=False)
    response = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, question_id, response, score):
        self.user_id = user_id
        self.question_id = question_id
        self.response = response
        self.score = score
        self.response_time = datetime.utcnow()

    def __repr__(self):
        return '<Response %r>' % self.response_id

# Create result class
class Result(db.Model):
    __tablename__ = 'results'
    result_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    total_score = db.Column(db.Numeric)

    def __init__(self, skill_id, user_id, total_score):
        self.skill_id = skill_id
        self.user_id = user_id
        self.total_score = total_score

    def __repr__(self):
        return '<Result %r>' % self.result_id

# Create tables
db.create_all()

# Initialize database
db.init_app(app)
