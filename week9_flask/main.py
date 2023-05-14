from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dkf3sldkjfDF23fLJ3b'

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
    return render_template("success.html", name=username)


@app.route('/api/register', methods=['POST', 'GET'])
def register():
    if(request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        #print(username + ":" + password)
        try:
            #get the cursor (a pointer to the DB)
            sql_query = "INSERT INTO User VALUES ('"
            sql_query += username + "','" + password + "')"
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
        elif(password != rows[0][1]):
            flash("Sorry, wrong password")
            return render_template("login.html")
        else:    
            return redirect(url_for('success', username=username))
        
    else:
        return render_template("login.html")

"""
#This is a TERRIBLE login system that uses plain files
#to store usernames... but it shows how we can
#store & access files on the server
@app.route('/api/login', methods=['POST', 'GET'])
def login():
    if(request.method == "POST"):
        username = request.form['username']
        #run through the list of users to see if this is
        #a legit user
        user_found = False
        file_handle = open('static/files/users.txt','r')
        for next_user in file_handle:
            next_user = next_user.strip()
            if(next_user == username):
                user_found = True
        file_handle.close()
        #if we found the user, send them to the success page
        #otherwise let them know they made a mistake and ask
        #them to try again
        if(user_found):
            return redirect(url_for('success', username=username))
        else:
            flash("No user named " + username + ": Try again")
            return render_template("login.html")
        
    else:
        return render_template("login.html")
"""


app.run(host='0.0.0.0', port=81, debug=True)
