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
    message = "EDIT YOUR PREFERENCES FOR BETTER RESULTS"
    return render_template("form.html", message = message)

@app.route("/form/events")
def form_e():
    return render_template("form_events.html")

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
    if request.method == 'POST':
        radius = request.form['radius']
        #print "Radius: " + radius
        category = request.form['category']
        #print "Place: " + category
        search = request.form['search']
        #print "Search: " + search
        price = request.form['price']
        #print "Price: " + price
        location = request.form['location']
        #print "Location: " + location
        date = request.form['date']
        #print "Date: " + date
        if 'search' in request.form:
            print "hi"
            message = "SUCCESSFULLY UPDATED PREFERENCES"
            functions.changePrefs(radius,category,search,price,location,date,session['username'])
            return render_template("form.html", message = message)
        else:
            output = []
            params = api.get_search_params(search,2,0,category,radius,False)
            ret = api.yelp_lookup(location,["",""],["","","",""],params)
            for business in ret:
                for key, value in business.iteritems():
                    info = []
                    for key, val in value.iteritems():
                        info.append([key.title(),val])
                    output.append(info)
                    
            return render_template("results.html", output = output)
    
    '''
    #test case
    radius = 500
    typeOfPlace = "restaurant"
    keyword = "pizza"
    minPriceLevel = 1
   
    typeOfPlace = place
    keyword = search
    minPriceLevel = price

    rsltList = api.allInOneFunc(LAT,LNG,radius, typeOfPlace, keyword, minPriceLevel)
    return render_template("results.html", results = rsltList)
    '''
    

@app.route("/results/events", methods=['POST','GET'])
def results_events():
    d = {}
    d["keyword"] = request.form['search']
    return render_template("results_events.html", events = api.getEvents(d))

if __name__ == '__main__':
    app.debug = True
    functions.initializeTables()
    app.run()
