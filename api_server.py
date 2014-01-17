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
    logging.info("Incoming %s" % request.args)
    callback_name = request.args.get('jsoncallback')
    result = search_index.search(request.args.get('query'),
                                 float(request.args.get('southWestLat')),
                                 float(request.args.get('southWestLng')),
                                 float(request.args.get('northEastLat')),
                                 float(request.args.get('northEastLng')))
    return Response('%s(%s)' % (callback_name, json.dumps(result)), content_type='application/javascript; charset=utf-8')