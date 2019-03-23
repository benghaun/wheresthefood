import os
import urllib.parse
import requests

GMAPKEY=os.environ.get('gmapkey')

def getLatLng(address):
    address = urllib.parse.quote(address)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&region=sg&key={}'.format(address,GMAPKEY)
    r = requests.get(url)
    return r.json()['results'][0]['geometry']['location']