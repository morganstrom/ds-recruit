# app.py

from flask import Flask, render_template, json, request, redirect, url_for, session, flash, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from model import db, User, Response, Question, Result
from config import BaseConfig
import irt

# Initialize app
app = Flask(__name__)
app.config.from_object(BaseConfig)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Batch upload questions from JSON
@app.before_first_request
def insert_questions():
    # Check if questions have not been inserted
    if (len(Question.query.all()) == 0):
        # Open json file
        with open("items/probability.json") as data_file:
            question_set = json.load(data_file)
            # Insert all questions into database
            for q in question_set:
                question = Question("prob", q, question_set[q])
                db.session.add(question)
            db.session.commit()

@app.route('/')
def main():
    if g.user.is_authenticated:
        return render_template('userhome.html')
    else:
        return render_template('index.html')

# Probability questionnaire

# Start
@app.route('/prob/')
@login_required
def show_questionnaire():
    # TODO: set g.current_question_nr at the start page for the questionnaire?

    # Get list of answered question ids
    answered_question_ids = list(map(lambda r: r.question_id, g.user.responses))

    # Get a list of question keys that the current user haven't responded to
    remaining_questions = Question.query \
        .filter(Question.question_id.notin_(answered_question_ids)) \
        .all()

    # If there are no remaining questions, test is over
    if (len(remaining_questions) == 0):
        return render_template('questionnaire_end.html',
                               reason='There are no more questions in the database.')

    # Show the first question on the remaining list
    first_question = remaining_questions[0].get_key()

    return render_template('questionnaire_start.html', first_question=first_question)

# Show question
@app.route('/prob/<question_key>', methods=['GET'])
@login_required
def show_question(question_key):
    # Load question
    question = Question.query.filter_by(question_key=question_key).first()

    # Check if the question exists
    if (question == None):
        return render_template('error.html', error='404: Question not found')

    # Get list of answered question ids
    answered_question_ids = list(map(lambda r: r.question_id, g.user.responses))

    # Check if the current user has already responded to this question
    if (question.get_id() in answered_question_ids):
        return render_template('error.html', error='You have already answered question %r' % question_key)

    # Get question data
    question_data = question.get_data()

    # Show current question
    return render_template('question.html',
                           skill_id=question.skill_id,
                           question_key=question_key,
                           question=question_data['question'],
                           options=question_data['options'])

# Process response
@app.route('/prob/<question_key>', methods=["POST"])
@login_required
def process_response(question_key):
    # Store response, if one is provided
    if ("option" in request.form.to_dict()):
        # Get response
        resp = request.form['option']

        # Load question
        question = Question.query.filter_by(question_key=question_key).first()

        # Check if the question exists
        if (question == None):
            return render_template('error.html', error='404: Question not found')

        # Get list of answered question ids
        answered_question_ids = list(map(lambda r: r.question_id, g.user.responses))

        # Check if the current user has already responded to this question
        if (question.get_id() in answered_question_ids):
            return render_template('error.html', error='You have already answered question %r' % question_key)

        # Score response
        score = question.score_response(resp)

        # Create new response object and commit to database
        response = Response(g.user.get_id(),
                            question.get_id(),
                            resp,
                            score)
        db.session.add(response)
        db.session.commit()

        # Update ability estimate
        # Set quadrature points for EAP estimation
        theta = irt.quadrature_points(33)

        # Look for existing records of ability estimate
        registered_result = Result.query \
            .filter(Result.user_id == g.user.get_id()) \
            .filter(Result.skill_id == 'prob') \
            .first()

        if (registered_result == None):
            # If no record exists, set prior to standard normal distribution
            prior = irt.quadrature_weights(theta, 0, 1)
            # Update EAP and PSD for ability estimate
            eap, psd = question.update_eap(score, theta, prior)
            # Create record
            result = Result('prob', g.user.get_id(), eap.item(), psd.item())
            db.session.add(result)
            db.session.commit()
        else:
            # Else, set prior using estimated eap and psd
            prior = irt.quadrature_weights(theta,
                                           registered_result.get_eap(),
                                           registered_result.get_psd())
            # Update EAP and PSD for ability estimate
            eap, psd = question.update_eap(score, theta, prior)
            # Update existing record
            registered_result.eap_estimate = eap.item()
            registered_result.psd_estimate = psd.item()
            db.session.commit()

    # Check if user has selected to end test
    if ("end" in request.form.to_dict()):
        return render_template('questionnaire_end.html')

    # Get list of answered question ids
    answered_question_ids = list(map(lambda r: r.question_id, g.user.responses))

    # Get a list of question keys that the current user haven't responded to
    remaining_questions = Question.query\
        .filter(Question.question_id.notin_(answered_question_ids))\
        .all()

    # If there are no remaining questions, test is over
    if (len(remaining_questions) == 0):
        return render_template('questionnaire_end.html',
                               reason='There are no more questions in the database.')

    # Todo: Quit the test if the respondent has answered 10 questions

    # Select the first question on the remaining list
    # Todo: randomize order of questions
    next_question = remaining_questions[0].get_key()

    return redirect(url_for("show_question", question_key=next_question, _method="GET"))

# Show results
@app.route('/results', methods=['GET'])
@login_required
def show_results():
    # Count number of responses for user
    n_questions = len(g.user.responses)

    # Count number of correct responses for user
    n_correct = sum(map(lambda r: r.score, g.user.responses))

    # Calculate percentage correct
    if (n_questions > 0):
        p_correct = round(n_correct / n_questions * 100, 0)
    else:
        p_correct = None

    # Todo: get average from all users
    avg_n_questions = 'Not enough data'
    avg_n_correct = 'Not enough data'
    avg_p_correct = 'Not enough data'

    # Get ability estimate from database
    registered_result = Result.query \
        .filter(Result.user_id == g.user.get_id()) \
        .filter(Result.skill_id == 'prob') \
        .first()

    # If no record is found, set to no data
    if (registered_result == None):
        eap_estimate = 'No data'
    else:
        eap_estimate = registered_result.get_eap() * 100 + 1000

    # Show results page
    return render_template('results.html',
                           n_questions=n_questions,
                           n_correct=n_correct,
                           p_correct=p_correct,
                           eap_estimate=eap_estimate,
                           avg_n_questions=avg_n_questions,
                           avg_n_correct=avg_n_correct,
                           avg_p_correct=avg_p_correct)

# login and logout
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # Get field values
    email = request.form['email']
    password = request.form['password']

    # Look up user in database
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is not None:
        flash('User with email %r already exist' % email, 'error')
        return redirect(url_for('signup'))
    else:
        # Add user
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Get field values
    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # Look up user in database
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Email is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))

    # Log in user
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('main'))

@app.route('/userhome')
@login_required
def user_home():
    # Todo: Add form for personal details
    # Todo: Add functionality to validate email
    # Todo: Add page with results summary
    # Todo: Add settings page for changing password & email
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
