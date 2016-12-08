from flask import Flask, redirect, request, render_template, url_for, session
from utils import dumbbell as functions
from utils import parser as api 
import hashlib, sqlite3, random
import urllib2
import json

# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
LAT = str(location["latitude"])
LNG = str(location["longitude"])


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

@app.route("/results/", methods=['POST','GET'])
def results():
    '''
    Yelp API results
    Gets information from user form
    Output is stored in a list with sublists that represent each business and its information
    For now, the user is required to enter a radius and location
    Output format: [[business1],[business2]]
    business1 = [[key,value],[key,value],...]
    '''
    radius = request.form['radius']
    place = request.form['place']
    search = request.form['search']
    price = request.form['price']
    location = request.form['location']
    date = request.form['date']
    output = []

    params = api.get_search_params(search,1,0,place,radius,False)
    ret = api.yelp_lookup(location,["",""],["","","",""],params)
    for business in ret:
        for key, value in business.iteritems():
            info = []
            for key, val in value.iteritems():
                info.append([key.title(),val])
            output.append(info)

    return render_template("results.html", output = output)

if __name__ == '__main__':
    app.debug = True
    functions.initializeTables()
    app.run()
