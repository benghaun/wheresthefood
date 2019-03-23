import json
import os
import urllib.parse
import requests
import time


GMAPKEY = os.environ.get('gmapkey')


def getLatLng(address):
    address = urllib.parse.quote(address)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&region=sg&key={}'.format(address,GMAPKEY)
    r = requests.get(url)
    return r.json()['results'][0]['geometry']['location']


def search_places_by_coordinate(location, radius, min_rating=0):
    json_obj = []
    types = ['restaurant', 'cafe', 'bar']
    for elem in types:
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': elem,
            'key': GMAPKEY
        }
        res = requests.get(endpoint_url, params=params)
        results = json.loads(res.content)

        # return results
        places.extend(results['results'])
        time.sleep(1)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params=params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(1)

        for idx in places:
            name = idx.get('name')
            # print(name)
            rating = idx.get('rating')
            if rating is None:
                rating = 0
            location = idx.get('geometry').get('location')
            lat = location.get('lat')
            lng = location.get('lng')
            if rating >= min_rating:
                json_obj.append({"name": str(name), "rating": str(rating), "latlongs": [[float(lat), float(lng)]]})
    return json_obj
