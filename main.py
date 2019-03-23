import os
import json
import sqlite3
import requests

from flask import Flask
from flask import request, jsonify, render_template, send_from_directory

app = Flask(__name__)

GMAPKEY=os.environ.get('gmapkey')

@app.route('/', methods=['GET'])
def home():
    url="https://maps.googleapis.com/maps/api/js?key={}&callback=initMap".format(GMAPKEY)
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
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&region=sg&key={}'.format(area,GMAPKEY)
    r = requests.get(url)
    viewport = r.json()['results'][0]['geometry']['viewport']
    response = jsonify(results=viewport)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
