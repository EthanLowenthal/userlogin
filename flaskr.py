# all the imports
import smtplib, random, sqlite3
from flask import Flask, request, session, redirect, url_for, render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

server = smtplib.SMTP('smtp.gmail.com', 587)  # port 465 or 587
server.ehlo()
server.starttls()
server.ehlo()
server.login('logmeinpassrecovery@gmail.com', 'logmeinmail')

user_db = sqlite3.connect('users.db')
db = user_db.cursor()

db.execute('''CREATE TABLE if not exists user (username text primary key, password text, email text)''')
try:
    db.execute('''INSERT INTO user VALUES ('admin', 'default', 'ethanmlowenthal@gmail.com')''')
except:
    pass
user_db.commit()
user_db.close()

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', user = session['user'][0])




@app.route('/settings', methods=['GET', 'POST'])
def user_settings():
    if request.method == 'POST':
        if request.form['username'] == '':
            username = session['user'][0]
        else:
            username = request.form['username']
            flash('Username Changed')
        if request.form['password'] == '':
            password = session['user'][1]
        else:
            password = request.form['password']
            password2 = request.form['password2']
            if password != password2:
                flash('Passwords do not Match')
                password = session['user'][1]
            else:
                flash('Password Changed')
        if request.form['email'] == '':
            email = session['user'][2]
        else:
            email = request.form['email']
            flash('Email Changed')

        local_user_db = sqlite3.connect('users.db')
        curs = local_user_db.cursor()
        curs.execute('''UPDATE user SET username = ?, password = ?, email = ? WHERE username = ?''', [(username), (password), (email), (session['user'][0])])
        local_user_db.commit()
        local_user_db.close()
        session['user'] = (username, password, email)
    return render_template('settings.html')


@app.route('/settings/delete')
def delete_account():
    delete_acc_db = sqlite3.connect('users.db')
    curs = delete_acc_db.cursor()
    curs.execute('''DELETE FROM user WHERE username = ?''', [(session['user'][0])])
    delete_acc_db.commit()
    delete_acc_db.close()
    flash('Account Deleted')
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':

        local_user_db = sqlite3.connect('users.db')
        curs = local_user_db.cursor()
        curs.execute('select * from user where username = ? and password = ?', [(request.form['username']), (request.form['password'])])
        session['user'] = curs.fetchone()
        if session['user'] == None:
            flash('Invalid Credentials')
            session.pop('user', None)
            local_user_db.close()
        else:
            request.form['password'], curs.execute('select email from user where username = ?', [(request.form['username'])])
            session['user'] = (request.form['username'], request.form['password'], curs.fetchone()[0])
            flash('You logged in as %s' % session['user'][0])
            local_user_db.close()
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/new', methods=['GET', 'POST'])
def new_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        confirm_email = request.form['email']
        global username, password, confirm_email
        if password != password2:
            flash('Passwords do not Match')
        else:
            return redirect(url_for('confirm_account'))
    return render_template('new_account.html')


comfirm_code = random.randint(1000, 10000)


@app.route('/new/confirm', methods=['GET', 'POST'])
def confirm_account():
    global username, password, confirm_email
    message = 'Subject: %s\n\n%s' % ('Account Confirmation', str(comfirm_code))
    server.sendmail('logmeinpassrecovery@gmail.com', confirm_email, message)
    flash('A confirmation email was sent')
    if request.method == 'POST':
        code = request.form['code']
        if code == str(comfirm_code):
            confirm_db = sqlite3.connect('users.db')
            curs = confirm_db.cursor()
            curs.execute('''INSERT INTO user (username, password, email) VALUES (?, ?, ?)''',
                         [(username), (password), (confirm_email)])
            confirm_db.commit()
            confirm_db.close()
            flash('Account Created')
            return redirect(url_for('login'))
        else:
            flash('Wrong Code')
    return render_template('confirm.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/recovery', methods=['GET', 'POST'])
def forgot_pass():
    if request.method == 'POST':
        email = request.form['email']
        local_user_db = sqlite3.connect('users.db')
        curs = local_user_db.cursor()
        curs.execute('select * from user where email = ?', [(email)])
        user = curs.fetchone()
        local_user_db.close()
        if user == None:
            flash('Email not found')
        else:
            text = 'Hello, ' + user[0] + '\nYour password is ' + user[1]
            message = 'Subject: %s\n\n%s' % ('Account Recovery', text)
            server.sendmail('logmeinpassrecovery@gmail.com', email, message)
            flash('Email Sent!')
    return render_template('recovery.html')

# @app.route('/manage/user')
# def manage_user():
#     return render_template('manage_user.html', user='Ethan')

@app.route('/manage', methods=['GET', 'POST'])
def manage_users():
    manage_db = sqlite3.connect('users.db')
    curs = manage_db.cursor()
    curs.execute('''SELECT * from user''')
    accounts = curs.fetchall()
    for i in range(len(accounts)):
        accounts[i] = str(accounts[i])
    if request.method == 'POST':
        create_user_db = sqlite3.connect('users.db')
        curs = create_user_db.cursor()
        curs.execute('''INSERT INTO user (username, password, email) VALUES (?, ?, ?)''', [(request.form['username']), (request.form['password']), (request.form['email'])])
        create_user_db.commit()
        create_user_db.close()
    return render_template('manage.html', users=accounts)
