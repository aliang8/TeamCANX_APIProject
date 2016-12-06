import os
import requests
import eventbrite
import datetime

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
