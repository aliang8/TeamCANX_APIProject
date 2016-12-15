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
            search = request.form['search']
            #print "Search: " + search
            price =  request.form['price']
            #print "Price: " + price
            location = request.form['location']
            #print "Location: " + location
            limit = request.form.get('limit')
            #print "Limit: " + limit
            date = request.form.get('startKey')

            '''
            data = []
            params = api.get_search_params(search,limit,0,radius,False)
            ret = api.yelp_lookup(location,["",""],["","","",""],params)
            for business in ret:
                for key, value in business.iteritems():
                    info = []
                    for key, val in value.iteritems():
                        info.append([key.title(),val])
                    data.append(info)
            '''
            typeOfPlace = search
            keyword = search
            if price == "":
                maxPriceLevel = "0"
            else:
                maxPriceLevel = price
            rsltList = api.allInOneFunc(location,radius, typeOfPlace, keyword, maxPriceLevel, limit)
            if rsltList == []:
                message = "Sorry, GoogleMaps API doesn't recognize that location. Try again."
                prefs = functions.getUserPrefs(session['username'])
                return render_template("form.html", message = message, prefs = prefs)

            else:
                return render_template("results.html", results = rsltList)
        elif "events" in request.form:
            d = {}
            d["q"] = request.form["search"]
            d["location"] = request.form['location']
            d["location.within"] = request.form['radius'] + "km"
            d["sort_by"] = request.form['sort_by']
            d["start_date.keyword"] = request.form["startKey"]
            d["limit"] = request.form.get('limit')
            price = request.form["price"]
            if (price):
                if price == "1":
                    d["price"] = "free"
                else:
                    d["price"] = "paid"
            #d["price"] = request.form['price']
            #d["start_date.keyword"] = request.form['startKey']
            #print d
            return render_template("results_events.html", events = api.getEvents(d), URL = api.getEvents(d)[0])
        else:
            radius = request.form['radius']
            search = request.form['search']
            price =  request.form['price']
            location = request.form['location']
            limit = request.form.get('limit')
            date = request.form.get('startKey')

            message = "SUCCESSFULLY UPDATED PREFERENCES"
            functions.changePrefs(radius,search,price,location,date,session['username'])
            prefs = functions.getUserPrefs(session['username'])
            return render_template("form.html", message = message, prefs = prefs)

@app.route("/events-list", methods=['GET'])
def events_list():
    if request.method == 'GET':
        if 'Add to Calendar' in request.args.values():
            args = request.args.keys()[0]
            words = args.split("|")
            url = words[0]
            name = words[1]
            start = words[2]
            end = words[3]
            description = words[4]
            functions.addEvent(url,name,start,end,description,session['username'])
            events = functions.getEvent(session['username'])
            return render_template("events-list.html", events = events);
        elif 'Remove Event' in request.args.values():
            args = request.args.keys()[0]
            words = args.split("|")
            name = words[0]
            userID = words[1]
            functions.removeEvent(name,userID)
            events = functions.getEvent(session['username'])
            return render_template("events-list.html", events = events);

@app.route("/results/events", methods=['POST','GET'])
def results_events():
    if request.method == 'POST':
        d = {}
        d["q"] = request.form['keyword']
        d["location"] = request.form['location']
        d["location.within"] = request.form['radius']+"km"
        d["sort_by"] = request.form['sort_by']
        d["price"] = request.form['price']
        d["start_date.keyword"] = request.form['startKey']
        """
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
        """
        #print d
        return render_template("results_events.html", events = api.getEvents(d), URL = api.getEvents(d)[0])

if __name__ == '__main__':
    app.debug = True
    functions.initializeTables()
    app.run()
