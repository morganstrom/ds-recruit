# app.py

from flask import Flask, render_template, json, request, redirect, url_for, session, flash, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from model import db, User, Response, Question
from config import BaseConfig

# Initialize app
app = Flask(__name__)
app.config.from_object(BaseConfig)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Batch upload questions from JSON
with open("items/probability.json") as data_file:
    question_set = json.load(data_file)
    for q in question_set:
        question = Question(q, question_set[q])
        db.session.add(question)
    db.session.commit()


@app.route('/')
def main():
    return render_template('index.html')

# Questionnaire
@app.route('/prob/')
@login_required
def show_questionnaire():
    # TODO: set g.current_question at the start page for the questionnaire?
    # TODO: Create starting page for questionnaire
    return render_template('error.html')

@app.route('/prob/<question_key>', methods=['GET'])
@login_required
def show_question(question_key):
    # Load question
    question = Question.query.filter_by(question_key=question_key).first()

    # TODO: Check for end of test

    # Show current item
    question_data = question.get_data()
    return render_template('prob.html',
                           question_key=question_key,
                           question=question_data['question'],
                           options=question_data['options'])

@app.route('/prob/<question_key>', methods=["POST"])
@login_required
def process_response(question_key):
    # Store response, if one is provided
    if "option" in request.form.to_dict():
        # TODO: Score response

        # Create new response object and commit to database
        response = Response(request.form['option'],
                            question_key,
                            g.user.get_id())
        db.session.add(response)
        db.session.commit()

    # TODO: Decide what is the next item based on which button was pressed
    next_question = question_key

    return redirect(url_for("show_question", question_key=next_question, _method="GET"))

# login and logout
@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['user_name'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user_name = request.form['user_name']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(user_name=user_name).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('main'))

@app.route('/userhome')
@login_required
def user_home():
    return render_template('userhome.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
