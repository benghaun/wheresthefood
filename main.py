import os
import json
import random
import sqlite3

from flask import Flask
from flask import request, jsonify, render_template, send_from_directory, redirect
import requests

from utils import search_places_by_coordinate


app = Flask(__name__)

GMAPKEY = os.environ.get('gmapkey')


@app.before_request
def before_request():
    if request.url.startswith('http://') and '127.0.0.1' not in request.url:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/', methods=['GET'])
def home():
    url = "https://maps.googleapis.com/maps/api/js?key={}&callback=initMap".format(GMAPKEY)
    return render_template('index.html', gmapsurl=url)


@app.route('/list', methods=['GET'])
def deal_list():
    return render_template('list.html')


@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('templates/scripts', path)


@app.route('/styles/<path:path>')
def send_css(path):
    return send_from_directory('templates/styles', path)


@app.route('/getdeals', methods=['GET'])
def getdeals():
    conn = sqlite3.connect('deals.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.execute('SELECT * FROM DEALS')
    rows = cur.fetchall()
    output = []
    for row in rows:
        addresses = None
        days = None
        if row[2] is not None:
            addresses = json.loads(row[2])
        if row[5] is not None:
            days = json.loads(row[5])
        output.append({"name": row[0],
                       "enddate": row[1],
                       "address_txt": row[3],
                       "address_url": row[4],
                       "addresses": addresses,
                       "days": days,
                       "timing": row[7],
                       "timeinfo": row[8],
                       "latlongs": json.loads(row[9])})
    response = jsonify(output)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/viewport', methods=['GET'])
def viewport():
    area = request.args.get('search')
    minrating = request.args.get('minrating')
    if minrating is not None:
        minrating = int(minrating)
    else:
        minrating = 0
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&region=sg&key={}'.format(area, GMAPKEY)
    r = requests.get(url)
    if len(r.json()['results']) == 0:
        response = jsonify({'error': 'location not found'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400
    result = r.json()['results'][0]['geometry']['viewport']
    lat = str(r.json()['results'][0]['geometry']['location']['lat'])
    lng = str(r.json()['results'][0]['geometry']['location']['lng'])
    result['nearby'] = search_places_by_coordinate(lat + "," + lng, "600", minrating)
    if len(result['nearby']) > 0:
        chosen = random.choice(result['nearby'])
        result['chosen'] = chosen
    response = jsonify(results=result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/viewportcoords', methods=['GET'])
def viewport_coords():
    coords = request.args.get('coords')
    lat = float(coords.split(',')[0])
    lng = float(coords.split(',')[1])
    result = {'southwest': {"lat": lat-0.0013, "lng": lng-0.0015},
              'northeast': {"lat": lat+0.0013, "lng": lng+0.0015}}
    result['nearby'] = search_places_by_coordinate(str(lat) + "," + str(lng), "600")
    chosen = random.choice(result['nearby'])
    result['chosen'] = chosen
    response = jsonify(results=result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
