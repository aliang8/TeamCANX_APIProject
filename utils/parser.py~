import collections
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


#Can be used to geolocate by using IP address
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
LAT = str(location["latitude"])
LNG = str(location["longitude"])


#----------------------------------------
#Google Maps
import urllib


def geoCode(location,key):

    url=('https://maps.googleapis.com/maps/api/geocode/json?'
         'address=%s'
         '&key=%s')%(location, key)
   # print url
    urlInfo = urllib.urlopen(url)
    jsonUntouched = urlInfo.read()
    jsonData = json.loads(jsonUntouched)

    latLong = []
   # print
    #print
    #print
    res = jsonData["results"][0]["geometry"]["location"]
    #print res
    #print
    #print
    #print
    latLong.append(res["lat"])
    latLong.append(res["lng"])
    #print latLong
    return latLong


def GooglPlacSear(lat, lng, radius, typeOfPlace,keyword, key):
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

def GooglPlacDet(ID,key):
    url = ('https://maps.googleapis.com/maps/api/place/details/json?'
           'placeid=%s'
           '&key=%s') %(ID, key)
   # print url

    urlInfo = urllib.urlopen(url)
    jsonUntouched = urlInfo.read()
    jsonData = json.loads(jsonUntouched)
   # print jsonData
    return jsonData



def crtLists(jsonData, maxPriceLevel,key):
   # print maxPriceLevel
    #must convert to int because form takes it in as a string
    maxPriceLevel = int(maxPriceLevel)
    #print maxPriceLevel
    resList = []
    res = jsonData["results"]
    for i in res:
        if maxPriceLevel == 0:
          #  print i["id"]
            details = GooglPlacDet(i["place_id"],key)
            details= details["result"]

            '''
            address = details["formatted_address"]
            number = details["formatted_phone_number"]
            rating = details["rating"]
            '''


            address = "N/A"
            if "formatted_address" in details:
                address = details["formatted_address"]
            number = "N/A"
            if "formatted_phone_number" in details:
                number = details["formatted_phone_number"]

            rating = "N/A"
            if "rating" in details:
                rating = details["rating"]

            if "price_level" in i:

                resList.append([i["name"],address,str(i["price_level"]),str(number),str(rating)])
            else:
                resList.append([i["name"],address,"N/A",str(number),str(rating)])
       # print i
        elif "price_level" in i:
          #THIS MEANS THAT WE MUST COMPLETELY IGNORE THE GOOGLE API RESULTS
          #THAT DON'T HAVE PRICE LEVELS :(
          if i["price_level"] <= maxPriceLevel:
              # took out  i["geometry"]["location"]....because the user probably won't care about the latitude/longitude

            #  print i["id"] + "-----THis is the id"
              details = GooglPlacDet(i["place_id"],key)

            #  print details
              details= details["result"]

              address = "N/A"
              if "formatted_address" in details:
                  address = details["formatted_address"]
              number = "N/A"
              if "formatted_phone_number" in details:
                  number = details["formatted_phone_number"]

              rating = "N/A"
              if "rating" in details:
                  rating = details["rating"]

              resList.append([i["name"],address,str(i["price_level"]),str(number),str(rating)])
   # print resList
    return resList




###This is the main function
    ###User inputs the latitude?, longitude?, radius, type of place, keyword, and minPricelevel----type of place and keyword must be strings
def allInOneFunc(location, radius, typeOfPlace,keyword, maxPriceLevel):

    #f = open("/Users/Flamingo/Documents/SoftDev/flask-intro/softdev/keys.txt","r")
    #f = open("C:\Users\Constantine\Desktop\Soft Dev\keys.txt","r")
    ## basepath = os.path.dirname("parser.py")
    # filepath = os.path.abspath(os.path.join(basepath, "..","..","keys.txt"))
    # f = open("/../../keys.txt","r")
    key = "AIzaSyDDsPeb49Cwld-euMdYU_F4WTTzBjpuSrk"
    #f.close()
    # print key


    latLong = geoCode(location,key)
    lat = latLong[0]
    lng = latLong[1]

    x = GooglPlacSear(lat, lng, radius, typeOfPlace,keyword, key)
    #x is the dictionary parsed from the json data

    y = crtLists(x,maxPriceLevel,key)
    #y is the list of places that fit the user's parameters

    return y


#test case
radius = 500
typeOfPlace = "restaurant"
keyword = "pizza"
maxPriceLevel = 1
##Lat and Lng are created at the top: they are the computer's ip address' location
#print allInOneFunc(LAT,LNG,radius, typeOfPlace, keyword, maxPriceLevel)


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
    if term:
        params['term'] = term
    if limit:
        params['limit'] = limit
    if sort:
        params['sort'] = sort
    if radius:
       params['radius_filter'] = radius
    if deals:
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
    ret = collections.OrderedDict()
    if coords[0] == '' and bounds[0] == '':
        response = client.search(loc,**params)
    elif loc == '' and bounds[0] == '':
        response = client.search_by_coordinates(coords[0],coords[1], **params)
    else:
        response = client.search_by_bounding_box(bounds[0],bounds[1],bounds[2],bounds[3],**params)
    for business in response.businesses:
        name = business.name
        ret[name] = collections.OrderedDict()
        ret[name]['name'] = name
        ret[name]['snippet_image_url'] = business.snippet_image_url
        ret[name]['snippet_text'] = business.snippet_text
        ret[name]['rating'] = business.rating
        ret[name]['display_phone'] = business.display_phone
        ret[name]['location_address'] = ' '.join(business.location.display_address)
        ret[name]['url'] = business.url
        #ret[name]['review_count'] = business.review_count
        #ret[name]['categories'] = business.categories
        #ret[name]['location_coordinate_latitude'] = business.location.coordinate.latitude
        #ret[name]['location_coordinate_longitude'] = business.location.coordinate.longitude
        ret[name]['deals'] = business.deals
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
-using google api to convert address -> lat,lng
-testing
'''
# returns list of (sub)dictionaries of each event's logo, name, description, url, start & end date & time
def getEvents(d):
    inputs = ""
    for key in d.keys():
        if d[key]: # if not empty
            if key == "location":
                latLong = geoCode(d["location"],"AIzaSyDDsPeb49Cwld-euMdYU_F4WTTzBjpuSrk")
                print latLong
                inputs += "&%s=%s"%("location.latitude", str(latLong[0]))
                inputs += "&%s=%s"%("location.longitude", str(latLong[1]))
            else:
                inputs += "&%s=%s"%(key, d[key])
    url = ("https://www.eventbriteapi.com/v3/events/search/?token=BV442UWQUREICGJW7V2A" + inputs)
    urlInfo = urllib.urlopen(url)
    jsonUntouched = urlInfo.read()
    eventsDict = json.loads(jsonUntouched)["events"]
    ret = [] # returned list
    ret.append(url)
    for event in eventsDict:
        holder = {} # sublist for each entry
        if (event["logo"]):
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

"""
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
"""

# example call
# start: 12/16 9AM
# end: 12/16 8 PM

#d1 = {"location.address":"345 chambers st"}
#getEvents(d1)
#print convertToUTC("2016", "12", "16", "09", "00")
#print convertToUTC("2016", "12", "16", "20", "00")

#=============================================================================
