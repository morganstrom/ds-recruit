# app.py

from flask import Flask, render_template, json, request, redirect, url_for, session
from werkzeug import generate_password_hash, check_password_hash
from model import db, User

# initialize app
app = Flask(__name__)

# Try to create tables
db.create_all()
# admin = User(username='admin', email='morgan@clikrecruit.se')
# db.session.add(admin)
# db.session.commit()

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signup', methods=['GET'])
def showSignUp():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signUp():
    """Code for creating a user"""
    try:
        # Read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _name and _email and _password:
            password_hash = generate_password_hash(_password)

            newuser = User(name=_name,
                           email=_email,
                           password=password_hash)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('userHome'))
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/signin', methods=['GET'])
def showSignIn():
    return render_template('signin.html')

@app.route('/signin', methods=['POST'])
def validateLogin():
    """Code for validating user login"""
    pass

@app.route('/home')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main'))

@app.route('/prob/<int:item_nr>', methods=["GET"])
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
        return render_template('prob.html', data=item, item_nr=item_nr)

@app.route('/prob/<int:item_nr>', methods=["POST"])
def scoreItem(item_nr):
    # Score item - TBD

    # Decide what is the next item based on which button was pressed
    if "next" in request.form.to_dict():
        next_item = item_nr + 1
    else:
        if item_nr - 1 < 0:
            next_item = item_nr
        else:
            next_item = item_nr - 1

    return redirect(url_for("showItem", item_nr=next_item, _method="GET"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
