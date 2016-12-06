import os
import requests
import eventbrite

# Eventbrite
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
    d = response.json()['events']
    for e in d:
        print e['name']['text']

getEvents("food", "best", "brooklyn", "10mi", "free")
