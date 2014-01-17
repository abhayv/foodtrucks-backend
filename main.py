# Copyright (C) 2014 Abhay Vardhan. All Rights Reserved.
"""
Author: abhay.vardhan@gmail.com
 main.py is the top level script.
"""

from globals import app
import api_server
import logging
import urllib2
import json
import search_index

FOOD_DATA_URL = 'http://data.sfgov.org/resource/rqzj-sfat.json'

@app.route('/build-index')
def buildIndex():
    """
    This request is called from cron daily to refresh the index
    :return:
    """
    response = urllib2.urlopen(FOOD_DATA_URL)
    raw = response.read()
    results = json.loads(raw)
    logging.debug("results %s" % results)
    search_index.buildIndex(results)
    return 'ok'