import requests
import json
import time
import xml.etree.ElementTree as ET
import os
gmapkey = os.environ.get("gmapkey")

# def search_places(address):
# 	endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&region=sg&key={}".format(address, gmapkey)
# 	res = requests.get(endpoint_url)
# 	results = json.loads(res.content).get('results')[0]
# 	return results.get('place_id')

def search_places_by_coordinate(location, radius, types, filename):
	endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
	places = []
	params = {
		'location': location,
		'radius': radius,
		'types': types,
		'key': gmapkey
	}
	res = requests.get(endpoint_url, params = params)
	results =  json.loads(res.content)

	# return results


	places.extend(results['results'])
	time.sleep(2)
	while "next_page_token" in results:
		params['pagetoken'] = results['next_page_token'],
		res = requests.get(endpoint_url, params = params)
		results = json.loads(res.content)
		places.extend(results['results'])
		time.sleep(2)

	with open(filename,"w",encoding='utf-8') as file:
		for idx in places:
			name = idx.get('name')
			print(name)

			rating = idx.get('rating')
			location = idx.get('geometry').get('location')
			lat = location.get('lat')
			lng = location.get('lng')

			file.write(str(name) + ", " + str(rating)+ ", " + str(lat)+ ", " + str(lng) + "\n")
			# print (idx)
			# print ('\n')
	return
	# return places

# def get_place_details(place_id, fields):
# 	endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
# 	params = {
# 		'placeid': place_id,
# 		'fields': ",".join(fields),
# 		'key': gmapkey
# 	}
# 	res = requests.get(endpoint_url, params = params)
# 	place_details =  json.loads(res.content)
# 	return place_details

places = search_places_by_coordinate("1.364304,103.866561", "600", "restaurant", "restaurants.txt")
places = search_places_by_coordinate("1.364304,103.866561", "600", "cafe", "cafes.txt")
places = search_places_by_coordinate("1.364304,103.866561", "600", "bar", "bars.txt")
# print (places)

# places = search_places("starbucks 12 marina boulevard")
# rating = get_place_details(places, ['name','rating'])
# print (rating)