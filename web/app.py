# app.py

from flask import Flask, render_template, json, request, redirect, url_for, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
mysql = MySQL()
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    """Code for creating a user"""

    try:
        # Read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # Validate the received values
        if _name and _email and _password:
            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})

            cursor.close()
            conn.close()

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _username and _password:

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_validateLogin', (_username,))
            data = cursor.fetchall()

            # If the username exists, match with stored password
            if len(data) > 0:
                if check_password_hash(str(data[0][3]), _password):
                    session['user'] = data[0][0]
                    return redirect(url_for('userHome'))
                else:
                    return render_template('error.html', error='Wrong Email address or Password.')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')

            cursor.close()
            conn.close()

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/userHome')
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
    app.run(debug=True, host='0.0.0.0')
