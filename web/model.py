from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import irt

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
    #a = db.Column(db.Numeric, nullable=False)
    #b = db.Column(db.Numeric, nullable=False)

    responses = db.relationship('Response', backref='question', lazy=True)

    def __init__(self, skill_id, question_key, question_data):
        self.skill_id = skill_id
        self.question_key = question_key
        self.question_data = question_data
        # Todo: Set difficulty and discrimination parameters while creating database
        #self.a = 1.0
        #self.b = 0.0

    def get_id(self):
        return self.question_id

    def get_key(self):
        return self.question_key

    def get_data(self):
        return self.question_data

    def score_response(self, response):
        # Evaluate scoring function defined in the solution field
        # as a function of response, returning true or false
        if eval(self.question_data['solution']):
            return 1
        else:
            return 0

    def update_eap(self, score, theta, theta_w):
        # Todo: use a and b variables, not constants
        L = irt.likelihood(theta, 1.0, 0.0, score)
        eap = irt.eap(theta, L, theta_w)
        psd = irt.eap_psd(eap, theta, L, theta_w)
        return eap, psd

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
    eap_estimate = db.Column(db.Float, nullable=False)
    psd_estimate = db.Column(db.Float, nullable=False)

    def __init__(self, skill_id, user_id, eap, psd):
        self.skill_id = skill_id
        self.user_id = user_id
        self.eap_estimate = eap
        self.psd_estimate = psd

    def get_eap(self):
        return self.eap_estimate

    def get_psd(self):
        return self.psd_estimate

    def __repr__(self):
        return '<Result %r>' % self.result_id

# Create tables
db.create_all()

# Initialize database
db.init_app(app)
