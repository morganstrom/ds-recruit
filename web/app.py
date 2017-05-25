from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'morgan'
app.config['MYSQL_DATABASE_DB'] = 'ds_recruit'
app.config['MYSQL_DATABASE_HOST'] = 'mysql_1'
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

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})

    finally:
        cursor.close()
        conn.close()

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
                    return redirect('/userHome')
                else:
                    return render_template('error.html', error='Wrong Email address or Password.')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userhome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/item_mc')
def showItem():
    item_data = {
        'question': 'Which web framework do you use?',
        'fields': ['Flask', 'Django', 'TurboGears', 'web2py', 'pylonsproject']
    }
    return render_template('item_mc.html', data=item_data)

@app.route('/response')
def showResponse():
    vote = request.args.get('field')
    return vote

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
