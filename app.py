from flask import Flask, redirect, request, render_template, url_for, session
from utils import dumbbell as functions
import hashlib, sqlite3, random

app = Flask(__name__)
app.secret_key = "canx"

@app.route("/", methods=['POST','GET'])
def new():
    return render_template('home.html')

@app.route("/<message>", methods=['POST','GET'])
def home(message):
    return render_template('home.html',message=message)

@app.route("/authenticate/", methods = ['POST','GET'])
def authenticate():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        hashpass = hashlib.sha224(password).hexdigest()
        if 'login' in request.form:
            if functions.login(username,password):
                session['username'] = username
                return redirect(url_for("form"))
            else:
                return redirect(url_for("home",message = "Login failed"))
        else:
            if functions.register(username,password):
                return redirect(url_for("home",message = "Registration successful"))
            else:
                return redirect(url_for("home",message = "Registration failed"))

@app.route("/form/")
def form():
    return render_template("form.html")

@app.route("/logout/")
def logout():
    session.pop('username')
    return redirect(url_for("home",message = "Logout successful"))


if __name__ == '__main__':
    app.debug = True
    functions.initializeTables()
    app.run()
