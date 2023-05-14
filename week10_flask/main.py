from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
import sqlite3


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)

#connect to the SQL Database
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


@app.route('/')
def home():
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
        return render_template("success.html", name=username)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route('/api/register', methods=['POST', 'GET'])
def register():
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        #let' hash the password to store it
        password_hashed = bcrypt.generate_password_hash(password)
        #the hashed password is a binary file, but we need to
        #turn it back into a string to store it in sql
        password_hashed_str = password_hashed.decode('utf-8')
        try:
            #get the cursor (a pointer to the DB)
            sql_query = "INSERT INTO User VALUES ('"
            sql_query += username + "','" + password_hashed_str + "')"
            #execute the query and commit the results
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute(sql_query)
            con.commit()
            flash("User successfully added")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists")
            return render_template('register.html')
    else:
        return render_template('register.html')
    
@app.route('/api/login', methods=['POST', 'GET'])
def login():
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
         #get the cursor (a pointer to the DB)
        sql_query = "SELECT username, password FROM USER WHERE "
        sql_query += "username = '" + username + "';"
        #execute the query and commit the results
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        if(len(rows) == 0):
            flash("No such user: " + username)
            return render_template("login.html")
        #rows[0] is the row containing the username/password
        #so rows[0][1] is the password value
        #now that it's hashed, we can't just use simple string comparison
        #elif(password != rows[0][1]):
        elif(not bcrypt.check_password_hash(rows[0][1],password)):
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
        
app.run(host='0.0.0.0', port=81, debug=True)
