from distutils.command import register
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, url_for, redirect, session
from flask import render_template
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = 'kiradeptrai'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '@mevivucom@123'
app.config['MYSQL_DATABASE_DB'] = 'flaskproject'
app.config['MYSQL_DATABASE_Host'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
curs = conn.cursor()

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def getRegister():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def postRegister():
    try:
        errors = []
        _username = request.form.get('inputUsername', None)
        _firstname = request.form.get('inputFirstname', None)
        _lastname = request.form.get('inputLastname', None)
        _email = request.form.get('inputEmail', None)
        _phone = request.form.get('inputPhone', None)
        _password = request.form.get('inputPassword', None)
        _hashpassword = generate_password_hash(_password)
        sql0 = "select count(*) from Users where userName = '{0}'".format(_username)
        curs.execute(sql0)
        rows = curs.fetchone()
        if rows and rows[0] > 0:
            errors = 'Username already exits!'
            return render_template('register.html', errors = errors)
            sql1 = "insert into Users(userName, firstName, lastName, email, phone, passWord) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(_username, _firstname, _lastname, _email, _phone, _hashpassword)
            curs.execute(sql1)
            conn.commit()
            return redirect(url_for('getLogin'))
    except Exception as e:
        raise (e)

@app.route('/login', methods=['GET'])
def getLogin():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def postLogin():
    try:
        errors = []
        _username = request.form.get('inputUsername', None)
        _password = request.form.get('inputPassword', None)
        sql0 = "select passWord from Users where userName = '{0}'".format(_username)
        curs.execute(sql0)
        rows = curs.fetchone()
        _hashpassword = rows[0]

        if rows:
            if check_password_hash(_hashpassword, _password):
                session['username'] = _username
                return redirect(url_for('Index'))
            else:
                errors = 'Wrong Username or Password'
                return render_template('login.html', errors = errors)
    except Exception as e:
        raise (e)

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('Index'))

@app.route('/profile', methods=['GET'])
def getProfile():
    try:
        _username = session['username']
        sql0 = "select * from Users where userName = '{0}'".format(_username)
        curs.execute(sql0)
        rows = curs.fetchall()
        if rows:
            return render_template('profile.html', profiledata = rows)
    except Exception as e:
        raise (e)

@app.route('/profile', methods=['POST'])
def postProfile():
    return render_template('profile.html')

@app.route('/editprofile', methods=['GET'])
def getEditProfile():
    try:
        _username = session['username']
        sql0 = "select * from Users where userName = '{0}'".format(_username)
        curs.execute(sql0)
        rows = curs.fetchall()
        if rows:
            return render_template('editprofile.html', profiledata = rows)
    except Exception as e:
        raise (e)

@app.route('/editprofile', methods=['POST'])
def postEditProfile():
    try:
        _firstname = request.form.get('inputFirstname', None)
        _lastname = request.form.get('inputLastname', None)
        _email = request.form.get('inputEmail', None)
        _phone = request.form.get('inputPhone',None)
        sql0 = "update Users set firstName = '{0}', lastName = '{1}', email = '{2}', phone = '{3}'".format(_firstname, _lastname, _email, _phone)
        curs.execute(sql0)
        return redirect(url_for('getEditProfile'))
    except Exception as e:
        raise (e)

if __name__ == '__main__':
    app.run()
