from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, url_for, redirect, session
from flask import render_template
from werkzeug.utils import secure_filename
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
def index():
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
            return render_template('register.html', errors=errors)
        else:
            sql1 = "insert into Users(userName, firstName, lastName, email, phone, passWord) values ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(
                _username, _firstname, _lastname, _email, _phone, _hashpassword)
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
                return redirect(url_for('index'))
            else:
                errors = 'Wrong Username or Password'
                return render_template('login.html', errors=errors)
    except Exception as e:
        raise (e)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'])
def getProfile():
    try:
        _username = session['username']
        sql0 = "select * from Users where userName = '{0}'".format(_username)
        curs.execute(sql0)
        rows = curs.fetchall()
        if rows:
            return render_template('profile.html', profiledata=rows)
    except Exception as e:
        raise (e)


@app.route('/profile', methods=['POST'])
def postProfile():
    return render_template('profile.html')


@app.route('/profile/editprofile', methods=['GET'])
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


@app.route('/profile/editprofile', methods=['POST'])
def postEditProfile():
    try:
        errors = []
        _username = session['username']
        _firstname = request.form.get('inputFirstname', None)
        _lastname = request.form.get('inputLastname', None)
        _gender = request.form.get('inputGender', None)
        _birthday = request.form.get('inputBirhday', None)
        _email = request.form.get('inputEmail', None)
        _phone = request.form.get('inputPhone', None)
        _address = request.form.get('inputAddress', None)
        _job = request.form.get('inputJob', None)
        _about = request.form.get('inputAbout', None)
        _changepassword = request.form.get('inputChangePassword', None)
        _currentpassword = request.form.get('inputCurrentPassword', None)
        _newpassword = request.form.get('inputNewPassword', None)
        _newhashpassword = generate_password_hash(_newpassword)
        sql0 = "select passWord from Users where userName = '{0}'".format(_username)
        curs.execute(sql0)
        rows = curs.fetchone()
        _hashpassword = rows[0]
        if check_password_hash(_hashpassword, _currentpassword):
            if _changepassword == "change":
                sql1 = "update Users set firstName = '{0}', lastName = '{1}', gender = '{2}', birthDay = '{3}', email = '{4}', phone = '{5}', address = '{6}', job = '{7}', about = '{8}', passWord = '{9}' where userName = '{10}'".format(
                    _firstname, _lastname, _gender, _birthday, _email, _phone, _address, _job, _about, _newhashpassword,
                    _username)
                curs.execute(sql1)
                conn.commit()
                return redirect(url_for('getProfile'))
            else:
                sql2 = "update Users set firstName = '{0}', lastName = '{1}', gender = '{2}', birthDay = '{3}', email = '{4}', phone = '{5}', address = '{6}', job = '{7}', about = '{8}' where userName = '{9}'".format(
                    _firstname, _lastname, _gender, _birthday, _email, _phone, _address, _job, _about, _username)
                curs.execute(sql2)
                conn.commit()
                return redirect(url_for('getProfile'))

        else:
            errors = 'Wrong password'
            return redirect(url_for('getEditProfile'), errors=errors)
    except Exception as e:
        raise (e)

def changeAvatar():
    try:
        _username = session['username']
        _avatar = request.form.get('inputAvatar')
        f = request.files['inputAvatar']
        f.save(secure_filename(f.filename))
        sql = "update Users set avatar = '{0}' where userName = '{1}'".format(_avatar, _username)
        curs.execute(sql)
        conn.commit()
        sql1 = "select avatar from Users where userName = '{0}'".format(_username)
        curs.execute(sql1)
        rows = curs.fetchone()
        _anh = rows[0]
        print(_anh)
        return redirect(url_for('getEditProfile'), anh = _anh)
    except Exception as e:
        raise (e)

if __name__ == '__main__':
    app.run()
