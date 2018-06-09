"""Input a list CSV of ZIP codes, return JSON of geocoded lat/lon for each ZIP."""

import csv
import json
import time
import requests

def read_csv():
    """Create a list of ZIPs from source CSV file."""
    with open('zips.csv', 'rb') as csvfile:
        zipcodes = []

        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            zips = ', '.join(row)
            zipcodes.append(zips)

    return zipcodes

zip_list = read_csv()


def geocode_zips(zip_list):
    """Get lat/lng + place name from Google Maps for each ZIP."""
    # Note: requires Google Maps API key to run. Not storing this in source.
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    zipcode = ''
    geocoded_results = []

    zip_index = 0
    while zip_index < len(zip_list):
        for z in zip_list:
            zipcode = z
            params = {'sensor': 'false', 'address': zipcode, 'key': key}
            api_request = requests.get(url, params=params)
            results = api_request.json()['results']
            loc = results[0]['geometry']['location']
            lat = loc['lat']
            lng = loc['lng']
            place_name = results[0]['formatted_address']
            data = {'zip': zipcode, 'lat': lat, 'lng': lng, 'place_name': place_name}
            geocoded_results.append(data)
            time.sleep(1.5)
            zip_index += 1

    with open('zipcodes.json', 'w') as outfile:
        json.dump(geocoded_results, outfile)

geocode_zips(zip_list)
