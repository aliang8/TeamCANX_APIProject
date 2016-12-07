#Eventbrite
import os
import requests
import eventbrite
import datetime
#----------------------------------------
#Yelp
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import urllib2

#==========================YELP API=============================
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

'''
response2 = client.search_by_bounding_box(
    37.900000,
    -122.500000,
    37.788022,
    -122.399797,
    **params
)
'''

##response3 = client.search_by_coordinates(37.788022, -122.399797, **params)
'''
Params for query: term(string),limit(#),offset(#),sort(0-Best matched, 1-Distance, 2-Highest Rated,category_filter(string),radius_filter(#),deals_filter(bool)
'''
def get_search_params(term,limit,sort):
    params = {}
    params['term'] = term
    params['limit'] = limit
    params['sort'] = sort
    '''
    params['category_filter'] = category_filter
    params['radius_filter'] = radius_filter
    params['deals_filter'] = deals_filter
    '''
    return params

def yelp_lookup(params,location):
    params = params
    ret = {}
    response = client.search(location,**params)
    for business in response.businesses:
        name = business.name
        ret[name] = {}
        ret[name]['phone'] = business.phone
        ret[name]['url'] = business.url
        ret[name]['review_count'] = business.review_count
    return [ret]

params = get_search_params('pastry',5,0)
ret = yelp_lookup(params,'1946 76 Street Brooklyn New York 11214')
print(json.dumps(ret, indent=4, sort_keys=True))

def yelp_search_by_coordinates(params,lat,long):
    params = params
    response = client.search_by_coordinates(lat,long, **params)
    data = response.json()

def yelp_search_by_bounding_box(params,swlat,swlong,nelat,nelong):
    params = params
    response = client.search_by_bounding_box(swlat,swlong,nelat,nelong,**params)
    data = response.json()

#====Eventbrite================================================================
def getEvents(keywordInput, sortInput, addressInput, radiusInput, priceInput):
    response = requests.get(
        "https://www.eventbriteapi.com/v3/events/search/",
        headers = {
            "Authorization": "Bearer ZYHRGY7DXAKVKECEDYXY",
            "q": keywordInput, #Return events matching the given keywords.
            "sort_by": sortInput, # Options are "date", "distance" and "best"
            "location.address": addressInput,
            "location.within": radiusInput, # int followed by "mi" or "km"
            "price" : priceInput, # only "free" or "paid"
        },
        verify = True,  # Verify SSL certificate
    )
    d = response.json()['events'] # dictionary of all events Eventbrite returns
    for event in d:
        if (event["logo"]!= None):
            print event["logo"]["url"] # link to event's logo pic
        print event['name']['text'] # name of event
        print event["description"]["text"] # VERY MESSY description
        print event["url"] # url of event
        print formatTime(event["start"]["local"]) # start date & time in UTC
        print formatTime(event["end"]["local"])  # end date & time in UTC
        print "\n ------------------------------------------\n"

# Converts 2016-12-12T08:00:00Z -> month-day-year hour:minute
def formatTime(utc):
    month = utc[5:7]
    day = utc[8:10]
    year = utc[0:4]
    timeIndex = utc.index('T')
    time = utc[timeIndex+1:-3]
    return month + "-" + day + "-" + year + " " + time

# example call
getEvents("food", "best", "brooklyn", "10mi", "free")

#=============================================================================
