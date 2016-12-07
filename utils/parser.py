#Eventbrite
import os
import requests
#import eventbrite
import datetime
#----------------------------------------
#Yelp
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json

#==========================================YELP API============================================
with open('config_secret.json') as cred:
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
Outputs from query: A list of dictionaries
Name of the business is the key
Properties outputted include: display phone, url, review count, categories,
rating, snippet_text, location_address, location_coordinates, deals, snippet_image_url,
menu_provider, reservation_url, eat24_url
''' 
def yelp_lookup(loc,coords,bounds,params):
    params = params
    ret = {}
    if lat == '' and swlat == '':
        response = client.search(loc,**params)
    elif loc == '' and swlat == '':
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

#Test Queries
params = get_search_params('food',5,0,'food',1000,False)
ret = yelp_lookup('1946 76 Street Brooklyn New York 11214','','','','','','',params)
#neat formatted json print
print(json.dumps(ret, indent=4, sort_keys=True))


#yelp_search_by_coordinates(37.77493,-122.419415,params)

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
#getEvents("food", "best", "brooklyn", "10mi", "free")

#=============================================================================
