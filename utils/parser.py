import datetime
import os.path
import sys
#----------------------------------------
#Yelp
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
#---------------------------------------
#Geolocation
import urllib
import urllib2


# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
LAT = str(location["latitude"])
LNG = str(location["longitude"])


#----------------------------------------
#Google Maps
import urllib


def GooglPlac(lat, lng, radius, typeOfPlace,keyword, key):
    Latitude = str(lat)
    Longitude = str(lng)
    User_Location = Latitude + "," + Longitude


    #We can also do types---aka specify more than one type of place
    #Additionally, we can have min/max prices for input
    #I believe it's possible to have more than one keyword


   # print User_Location
   # print keyword
    if keyword == "":
        url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
               'location=%s'
               '&radius=%s'
               '&type=%s'
               '&key=%s') % (User_Location, radius, typeOfPlace, key)
    else:
        url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
               'location=%s'
               '&radius=%s'
               '&type=%s'
               '&keyword=%s'
               '&key=%s') % (User_Location, radius, typeOfPlace,keyword, key)
  #  print url
    #Getting Json data
    urlInfo = urllib.urlopen(url)
    jsonUntouched = urlInfo.read()
    jsonData = json.loads(jsonUntouched)
   # print jsonData
    return jsonData




def crtLists(jsonData, minPriceLevel):
   # print minPriceLevel
    #must convert to int because form takes it in as a string
    minPriceLevel = int(minPriceLevel)
    resList = []
    res = jsonData["results"]
    for i in res:
       # print i
        if "price_level" in i:
          #THIS MEANS THAT WE MUST COMPLETELY IGNORE THE GOOGLE API RESULTS
          #THAT DON'T HAVE PRICE LEVELS :(
          if i["price_level"] >= minPriceLevel:
              # took out  i["geometry"]["location"]....because the user probably won't care about the latitude/longitude
              resList.append([i["name"]+",",i["vicinity"], "Price Level: "+str(i["price_level"])])
   # print resList
    return resList




###This is the main function
###User inputs the latitude?, longitude?, radius, type of place, keyword, and minPricelevel----type of place and keyword must be strings
def allInOneFunc(lat, lng, radius, typeOfPlace,keyword, minPriceLevel):

    f = open("/Users/Flamingo/Documents/SoftDev/flask-intro/softdev/keys.txt","r")
    # f = open("C:\Users\Constantine\Desktop\Soft Dev\keys.txt","r")
   ## basepath = os.path.dirname("parser.py")
   # filepath = os.path.abspath(os.path.join(basepath, "..","..","keys.txt"))
   # f = open("/../../keys.txt","r")
    key = f.readline()
    f.close()
    print key
    x = GooglPlac(lat, lng, radius, typeOfPlace,keyword, key)
    #x is the dictionary parsed from the json data

    y = crtLists(x,minPriceLevel)
    #y is the list of places that fit the user's parameters

    return y


#test case
radius = 500
typeOfPlace = "restaurant"
keyword = "pizza"
minPriceLevel = 1
##Lat and Lng are created at the top: they are the computer's ip address' location
#print allInOneFunc(LAT,LNG,radius, typeOfPlace, keyword, minPriceLevel)


#==========================================YELP API============================================
with open('utils/config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)
'''
Params for query: term(string), limit(#), offset(#), sort(0-Best matched, 1-Distance,
2-Highest Rated, category_filter(string), radius_filter(#), deals_filter(bool)
'''

def get_search_params(term,limit,sort,category,radius,deals):
    params = {}
    params['term'] = term
    params['limit'] = limit
    params['sort'] = sort
    params['category_filter'] = category
    params['radius_filter'] = radius
    params['deals_filter'] = deals
    return params

'''
Usage: 3 types of searches: By location (words), by coordinates, by setting bounds
ret = yelp_lookup(loc,coords,bounds,params)
loc : string
coords : [latitude,longitude]
bounds : [SWlatitude,SWlongitude,NElatitude,NElongitude]
params: params

Outputs from query: A list of dictionaries
Name of the business is the key
Properties outputted include: display phone, url, review count, categories,
rating, snippet_text, location_address, location_coordinates, deals, snippet_image_url,
menu_provider, reservation_url, eat24_url
'''

def yelp_lookup(loc,coords,bounds,params):
    params = params
    ret = {}
    if coords[0] == '' and bounds[0] == '':
        response = client.search(loc,**params)
    elif loc == '' and bounds[0] == '':
        response = client.search_by_coordinates(coords[0],coords[1], **params)
    else:
        response = client.search_by_bounding_box(bounds[0],bounds[1],bounds[2],bounds[3],**params)
    for business in response.businesses:
        name = business.name
        ret[name] = {}
        ret[name]['display_phone'] = business.display_phone
        ret[name]['url'] = business.url
        ret[name]['review_count'] = business.review_count
        ret[name]['categories'] = business.categories
        ret[name]['rating'] = business.rating
        ret[name]['snippet_text'] = business.snippet_text
        ret[name]['location_address'] = business.location.display_address
        ret[name]['location_coordinate_latitude'] = business.location.coordinate.latitude
        ret[name]['location_coordinate_longitude'] = business.location.coordinate.longitude
        ret[name]['deals'] = business.deals
        ret[name]['snippet_image_url'] = business.snippet_image_url
        ret[name]['menu_provider'] = business.menu_provider
        ret[name]['reservation_url'] = business.reservation_url
        ret[name]['eat24_url'] = business.eat24_url
    return [ret]
'''
#Test Queries
params = get_search_params('food',5,0,'food',1000,False)
ret = yelp_lookup('1946 76 Street Brooklyn New York 11214',["",""],["","","",""],params)
ret = yelp_lookup('',[37.77493,-122.419415],["","","",""],params)
#neat formatted json print
print(json.dumps(ret, indent=4, sort_keys=True))

'''

#====Eventbrite================================================================

'''
Todo:
-start_date.keyword
-using google api to convert address -> lat,lng
-testing
'''
# returns list of (sub)dictionaries of each event's logo, name, description, url, start & end date & time
def getEvents(d):
    keyword = sort_by = dateKey = location_address = location_within = price = lat = lng = startRange = endRange = ""
    if ("year_start" in d) and ("month_start" in d) and ("day_start" in d) and ("hour_start" in d) and ("minute_start" in d):
        startRange = toUTC_start(d["year_start"], d["month_start"], d["day_start"], d["hour_start"], d["minute_start"])
    if ("year_end" in d) and ("month_end" in d) and ("day_end" in d) and ("hour_end" in d) and ("minute_end" in d):
        endRange = toUTC_end(d["year_end"], d["month_end"], d["day_end"], d["hour_end"], d["minute_end"])
    if "keyword" in d:
        keyword = "&q=" + d["keyword"]
    if "sort" in d:
        sort_by = "&sort_by=" + d["sort"]
    if "dateKey" in d:
        dateKey = "&start_date.keyword=" + d["dateKey"]
    if "address" in d:
        location_address = "&location.address=" + d["address"]
    if "radius" in d:
        location_within = "&location.within=" + d["radius"]
    if "price" in d:
        price = "&price=" + d["price"]
    if "lat" in d:
        lat = "&location.latitude=" + d["lat"]
    if "long" in d:
        lat = "&location.longitude=" + d["long"]
    url = ('https://www.eventbriteapi.com/v3/events/search/?token=BV442UWQUREICGJW7V2A' + \
            keyword + sort_by + location_address + location_within + startKey + price + lat + lng + startRange + endRange)
    '''
    # RIP requests code
    response = requests.get(
        "https://www.eventbriteapi.com/v3/events/search/",
        headers = {
            "Authorization": "Bearer BV442UWQUREICGJW7V2A",
            "q": d["keyword"], #Return events matching the given keywords.
            "sort_by": d["sort"], # Options are "date", "distance" and "best"
            "location.address": d["address"],
            "location.within": d["radius"], # int followed by "mi" or "km"
            "price" : d["price"], # only "free" or "paid"
            "start_date.keyword" : d["startKey"], # this_week, next_week, this_weekend, next_month, this_month, tomorrow, today
            "start_date.range_start" : startRange, # local datetime format
            "start_date.range_end" : endRange,
            "location.latitude": d["lat"],
            "location.longitude": d["long"],
        },
        verify = True,  # Verify SSL certificate
    )
    '''
    urlInfo = urllib.urlopen(url)
    jsonUntouched = urlInfo.read()
    d = json.loads(jsonUntouched)["events"]
    #d = response.json()['events'] # dictionary of all events Eventbrite returns
    ret = [] # returned list
    i = 0
    for event in d:
        holder = {} # sublist for each entry
        if (event["logo"]!= None):
            holder["logo"] = event["logo"]["url"] # link to event's logo pic
        holder["name"] = event['name']['text'] # name of event
        holder["description"] = event["description"]["text"] # VERY MESSY description
        holder["url"] = event["url"] # url of event
        #print event["start"]["local"]
        holder["start"] = formatTime(event["start"]["local"]) # start date & time in UTC
        #print event["end"]["local"]
        holder["end"] = formatTime(event["end"]["local"])  # end date & time in UTC
        ret.append(holder)
    return ret

# Converts 2016-12-12T08:00:00 -> month-day-year hour:minute
def formatTime(utc):
    month = utc[5:7]
    day = utc[8:10]
    year = utc[0:4]
    timeIndex = utc.index('T')
    time = utc[timeIndex+1:-3]
    return "%s/%s/%s %s"%(month, day, year, time)

def toUTC_start(year, month, day, hour, minute):
    return "&start_date.range_start=" + "%s-%s-%sT%s:%s:00"%(year, month, day, hour, minute)

def toUTC_end(year, month, day, hour, minute):
    return "&start_date.range_end=" + "%s-%s-%sT%s:%s:00"%(year, month, day, hour, minute)

def getResponses():
    d = {}
    if request.method == 'POST':
        d["radius"]= request.form['radius']
    return d

# example call
# start: 12/16 9AM
# end: 12/16 8 PM
d1 = { "keyword":"food", "sort":"best", "address":"united states", "radius":"10mi", \
"lat":LAT, "long":LNG, "price":"", "startKey":"", \
"year_start":"2016", "month_start":"12", "day_start":"16", "hour_start":"00", "minute_start":"00", \
"year_end":"2016", "month_end":"12", "day_end":"16", "hour_end":"20", "minute_end":"00"}

d2 = { "keyword":"", "sort":"", "address":"united states",  \
"lat":LAT, "long":LNG, "price":"", \
"year_start":"2016", "month_start":"12", "day_start":"16", "hour_start":"00", "minute_start":"00", \
"year_end":"2016", "month_end":"12", "day_end":"16", "hour_end":"20", "minute_end":"00"}

#print getEvents(d2)
#print convertToUTC("2016", "12", "16", "09", "00")
#print convertToUTC("2016", "12", "16", "20", "00")

#=============================================================================
