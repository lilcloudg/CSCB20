from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
#import sqlite3 #<-- we won't need this anymore
from flask_sqlalchemy import SQLAlchemy #<-- this is an easier/safer way to do SQL back-end
from sqlalchemy import exc



app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)

#we need to point flask to our SQLAlchemy database and
#then instantiate it
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


#Let's get rid of our "hard coded" SQL connection and replace
#it with something that looks more like objects we're used to using

#connect to the SQL Database
'''
con = sqlite3.connect("database.db")
cur = con.cursor()
# Creates the User table
sql_query = """
    CREATE TABLE IF NOT EXISTS User 
    (
        username TEXT PRIMARY KEY, 
        password TEXT 
    )
"""
#cur.execute(sql_query)
'''


class User(db.Model):
    __tablename__ = 'User'
    user_name = db.Column(db.String(20), primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.user_name + ":" + self.full_name

with app.app_context():
    db.create_all()

def add_user(user_name, full_name, email, password):
    new_user = User(user_name=user_name, full_name=full_name, email=email,password=password)
    db.session.add(new_user)
    db.session.commit()


@app.route('/')
def home():
        # we can try just hard-coding some people to test... but be
        #careful... this will mess with integrity constraints
        #add_user("alice", "Alice Aliceson", "alice@alice.net", "alice123")
        #add_user("bob", "Bob Bobington", "bob@bobsoft.bob", "bob123")
        user_data = User.query.all()
        print(user_data)
        return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/api/formpost', methods=['POST'])
def formpost():
    print(request.form['user-text'])
    return "You said: " + str(request.form['user-text'])

@app.route('/success/<username>')
def success(username):
    #we only want the user to be able to see this if they're 
    #logged in (i.e., if they have a user value in the session)
    if("user" not in session):
        flash("must log in before you can access this page")
        return redirect(url_for('login'))
    elif(session['user'] != username):
        flash("Hey... that's not your page")
        return redirect(url_for('login'))
    else:
        #we now have a full person object, and can easily access all their attributes:
        user = User.query.filter_by(user_name = username).first()
        return render_template("success.html", name=user.full_name)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route('/api/register', methods=['POST', 'GET'])
def register():
    if(request.method == "POST"):
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        #let' hash the password to store it
        password_hashed = bcrypt.generate_password_hash(password)
        #the hashed password is a binary file, but we need to
        #turn it back into a string to store it in sql
        password_hashed_str = password_hashed.decode('utf-8')
        try:
            """
            #get the cursor (a pointer to the DB)
            sql_query = "INSERT INTO User VALUES ('"
            sql_query += username + "','" + password_hashed_str + "')"
            #execute the query and commit the results
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute(sql_query)
            con.commit()
            """
            #isn't this much easier than messing with SQL queries?
            add_user(username, fullname, email, password_hashed_str)
            flash("User successfully added")
            return redirect(url_for('login'))
        except exc.IntegrityError:
            flash("Username already exists")
            return render_template('register.html')
    else:
        return render_template('register.html')
    
@app.route('/api/login', methods=['POST', 'GET'])
def login():
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        #old SQLLite way
        '''
         #get the cursor (a pointer to the DB)
        sql_query = "SELECT username, password FROM USER WHERE "
        sql_query += "username = '" + username + "';"
        #execute the query and commit the results
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        '''
        #new SQLAlchemy way
        #get the first (and presumably only) user with this name
        user = User.query.filter_by(user_name = username).first()
        if(not user):
            flash("No such user: " + username)
            return render_template("login.html")
        elif(not bcrypt.check_password_hash(user.password,password)):
            flash("Sorry, wrong password")
            return render_template("login.html")
        else:
            #the user has properly logged in... so store
            #their username for this session
            session["user"] = username
            return redirect(url_for('success', username=username))
        
    else:
        return render_template("login.html")


@app.route("/passwords")
def passwords():
    #I hope this goes without saying but please NEVER do this
    #on a real web app
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    sql_query = "SELECT * FROM USER"
    rows = cur.execute(sql_query).fetchall()
    output = "<html>USERNAME   PASSWORD<br><ul>"
    for next_user in rows:
        output += "<li>" + str(next_user[0]) + " - " + str(next_user[1]) + "</li>"
    output += "</ul></html>"
    return output
        
@app.route('/bootstrap')
def bootstrap():
    return render_template('bootstrap.html')

app.run(host='0.0.0.0', port=81, debug=True)
