# app.py

from flask import Flask, render_template, json, request, redirect, url_for, session, flash, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from model import db, User, Response
from config import BaseConfig

# initialize app
app = Flask(__name__)
app.config.from_object(BaseConfig)

# setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def main():
    return render_template('index.html')

# questionnaire
@app.route('/prob/<int:item_nr>', methods=['GET'])
@login_required
def showItem(item_nr):
    # Load items
    with open("items/probability.json") as data_file:
        item_set = json.load(data_file)
    # Check for end of test
    if item_nr >= len(item_set):
        return "test over!"
    else:
        # Show current item
        item = item_set[item_nr]
        return render_template('prob.html', question=item['question'], options=item['options'], item_nr=item_nr)

@app.route('/prob/<int:item_nr>', methods=["POST"])
@login_required
def scoreItem(item_nr):
    # Store response, if one is provided
    if "option" in request.form.to_dict():
        # TODO: Score response

        # Create new response object and commit to database
        new_response = Response(request.form['option'], item_nr, g.user.get_id())
        db.session.add(new_response)
        db.session.commit()

    # Decide what is the next item based on which button was pressed
    if "next" in request.form.to_dict():
        next_item = item_nr + 1
    else:
        if item_nr - 1 < 0:
            next_item = item_nr
        else:
            next_item = item_nr - 1

    return redirect(url_for("showItem", item_nr=next_item, _method="GET"))

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
