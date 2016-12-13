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
    prefs = functions.getUserPrefs(session['username'])
    return render_template("form.html", message = message, prefs = prefs)

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
        if 'places' in request.form:
            radius = request.form['radius']
            #print "Radius: " + radius
            category = request.form['category']
            #print "Place: " + category
            search = request.form['search']
            #print "Search: " + search
            price =  request.form['price']
            #print "Price: " + price
            location = request.form['location']
            #print "Location: " + location
            limit = request.form.get('limit')
            #print "Limit: " + limit
            data = []
            params = api.get_search_params(search,limit,0,category,radius,False)
            ret = api.yelp_lookup(location,["",""],["","","",""],params)
            for business in ret:
                for key, value in business.iteritems():
                    info = []
                    for key, val in value.iteritems():
                        info.append([key.title(),val])
                    data.append(info)
            typeOfPlace = search
            keyword = search
            if price == "":
                maxPriceLevel = "0"
            else:
                maxPriceLevel = price
            rsltList = api.allInOneFunc(LAT,LNG,radius, typeOfPlace, keyword, maxPriceLevel)
            return render_template("results.html",data = data, results = rsltList)
        elif "events" in request.form:
            d = {}
            d["q"] = request.form["search"]
            d["location.address"] = request.form['location']
            d["location.within"] = request.form['radius']
            d["sort_by"] = request.form['sort_by']
            d["start_date.keyword"] = request.form["startKey"]
            #d["price"] = request.form['price']
            #d["start_date.keyword"] = request.form['startKey']
            #print d
            return render_template("results_events.html", events = api.getEvents(d), URL = api.getEvents(d)[0])
        else:
            message = "SUCCESSFULLY UPDATED PREFERENCES"
            functions.changePrefs(radius,category,search,price,location,date,session['username'])
            return render_template("form.html", message = message)

@app.route("/events-list")
def events_list():
    return render_template("events-list.html");

@app.route("/results/events", methods=['POST','GET'])
def results_events():
    if request.method == 'POST':
        d = {}
        d["q"] = request.form['keyword']
        d["location.address"] = request.form['address']
        d["location.within"] = request.form['radius']
        d["sort_by"] = request.form['sort_by']
        d["price"] = request.form['price']
        d["start_date.keyword"] = request.form['startKey']
        # DATE & TIME
        d["year_start"] = request.form['year_start']
        d["month_start"] = request.form['month_start']
        d["day_start"] = request.form['day_start']
        d["hour_start"] = request.form['hour_start']
        d["minute_start"] = request.form['minute_start']
        d["year_end"] = request.form['year_end']
        d["month_end"] = request.form['month_end']
        d["day_end"] = request.form['day_end']
        d["hour_end"] = request.form['hour_end']
        d["minute_end"] = request.form['minute_end']
        #print d
        return render_template("results_events.html", events = api.getEvents(d), URL = api.getEvents(d)[0])

if __name__ == '__main__':
    app.debug = True
    functions.initializeTables()
    app.run()
