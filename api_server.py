# Copyright (C) 2014 Abhay Vardhan. All Rights Reserved.
"""
Author: abhay.vardhan@gmail.com

Provides the api endpoints
"""

__author__ = 'abhay'

from flask import Response, request
from globals import app
import logging
import json
import search_index

@app.route('/search')
def search():
    """
    Search for food truck locations given a query and a rectangular area defined by coordinates of the south west
    and north east corners:
    query: String to search for
    southWestLat: Latitude of the south west corner
    southWestLng: Longitude of the south west corner
    northEastLat: Latitude of the north east corner
    northEastLng: Longitude of the north east corner
    jsoncallback: Name of the JSONP callback function wrapper

    :return: JSONP encoded result in the following format:
    jsoncallback({'success': true, 'data': [
    <food_truck_data_1>,
    <food_truck_data_2>
    ]})

    Where food_truck_data is a JSON object with info fields described in http://data.sfgov.org/resource/rqzj-sfat.json
    """
    logging.debug("Incoming %s" % request.args)
    callback_name = request.args.get('jsoncallback')
    results = search_index.search(request.args.get('query'),
                                 float(request.args.get('southWestLat')),
                                 float(request.args.get('southWestLng')),
                                 float(request.args.get('northEastLat')),
                                 float(request.args.get('northEastLng')))
    return Response('%s(%s)' % (callback_name, json.dumps({'success': True, 'data': results})),
                    content_type='application/javascript; charset=utf-8')